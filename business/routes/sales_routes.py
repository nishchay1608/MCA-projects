# routes/sales_routes.py
from flask import jsonify, request, render_template

def init_sales_routes(app, db):
    """Initialize sales routes"""
    
    @app.route('/sales')
    def manage_sales():
        """Sales management page"""
        return render_template('sales.html')

    @app.route('/api/sales', methods=['GET'])
    def api_get_sales():
        """Get all sales with customer and product info"""
        try:
            date_filter = request.args.get('date')
            
            if date_filter:
                query = """
                    SELECT s.*, c.name as customer_name, p.product_name, p.category
                    FROM sales s
                    LEFT JOIN customers c ON s.customer_id = c.customer_id
                    JOIN products p ON s.product_id = p.product_id
                    WHERE s.sale_date = %s
                    ORDER BY s.sale_date DESC, s.sale_id DESC
                """
                sales = db.execute_query(query, (date_filter,), fetch=True)
            else:
                query = """
                    SELECT s.*, c.name as customer_name, p.product_name, p.category
                    FROM sales s
                    LEFT JOIN customers c ON s.customer_id = c.customer_id
                    JOIN products p ON s.product_id = p.product_id
                    ORDER BY s.sale_date DESC, s.sale_id DESC
                """
                sales = db.execute_query(query, fetch=True)
                
            return jsonify({'success': True, 'sales': sales})
        except Exception as e:
            return jsonify({'success': False, 'message': str(e)})

    @app.route('/api/sales', methods=['POST'])
    def api_add_sale():
        """Add new sale"""
        try:
            data = request.json
            
            # Check product stock
            product = db.execute_query(
                "SELECT stock_quantity FROM products WHERE product_id = %s", 
                (data['product_id'],), 
                fetch=True
            )[0]
            
            if product['stock_quantity'] < data['quantity']:
                return jsonify({'success': False, 'message': f'Insufficient stock. Only {product["stock_quantity"]} units available.'})
            
            # Insert sale
            query = """
                INSERT INTO sales (customer_id, product_id, sale_date, quantity, unit_price, 
                                total_amount, payment_method, region, sales_person)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            db.execute_query(query, (
                data['customer_id'],
                data['product_id'],
                data['sale_date'],
                data['quantity'],
                data['unit_price'],
                data['total_amount'],
                data['payment_method'],
                data.get('region'),
                data.get('sales_person')
            ))
            
            # Update product stock
            db.execute_query(
                "UPDATE products SET stock_quantity = stock_quantity - %s WHERE product_id = %s",
                (data['quantity'], data['product_id'])
            )
            
            return jsonify({'success': True, 'message': 'Sale recorded successfully'})
        except Exception as e:
            return jsonify({'success': False, 'message': str(e)})

    @app.route('/api/sales/<int:sale_id>', methods=['GET'])
    def api_get_sale(sale_id):
        """Get single sale"""
        try:
            sale = db.execute_query(
                "SELECT * FROM sales WHERE sale_id = %s", 
                (sale_id,), 
                fetch=True
            )
            if sale:
                return jsonify({'success': True, 'sale': sale[0]})
            else:
                return jsonify({'success': False, 'message': 'Sale not found'})
        except Exception as e:
            return jsonify({'success': False, 'message': str(e)})

    @app.route('/api/sales/<int:sale_id>', methods=['PUT'])
    def api_update_sale(sale_id):
        """Update sale"""
        try:
            data = request.json
            
            # Get old sale data to adjust stock
            old_sale = db.execute_query(
                "SELECT product_id, quantity FROM sales WHERE sale_id = %s", 
                (sale_id,), 
                fetch=True
            )[0]
            
            # Update sale
            query = """
                UPDATE sales 
                SET customer_id = %s, product_id = %s, sale_date = %s, quantity = %s, 
                    unit_price = %s, total_amount = %s, payment_method = %s, 
                    region = %s, sales_person = %s
                WHERE sale_id = %s
            """
            db.execute_query(query, (
                data['customer_id'],
                data['product_id'],
                data['sale_date'],
                data['quantity'],
                data['unit_price'],
                data['total_amount'],
                data['payment_method'],
                data.get('region'),
                data.get('sales_person'),
                sale_id
            ))
            
            # Adjust product stock if product or quantity changed
            if old_sale['product_id'] != data['product_id'] or old_sale['quantity'] != data['quantity']:
                # Restore old product stock
                db.execute_query(
                    "UPDATE products SET stock_quantity = stock_quantity + %s WHERE product_id = %s",
                    (old_sale['quantity'], old_sale['product_id'])
                )
                # Deduct new product stock
                db.execute_query(
                    "UPDATE products SET stock_quantity = stock_quantity - %s WHERE product_id = %s",
                    (data['quantity'], data['product_id'])
                )
            
            return jsonify({'success': True, 'message': 'Sale updated successfully'})
        except Exception as e:
            return jsonify({'success': False, 'message': str(e)})

    @app.route('/api/sales/<int:sale_id>', methods=['DELETE'])
    def api_delete_sale(sale_id):
        """Delete sale"""
        try:
            # Get sale data to restore stock
            sale = db.execute_query(
                "SELECT product_id, quantity FROM sales WHERE sale_id = %s", 
                (sale_id,), 
                fetch=True
            )[0]
            
            # Restore product stock
            db.execute_query(
                "UPDATE products SET stock_quantity = stock_quantity + %s WHERE product_id = %s",
                (sale['quantity'], sale['product_id'])
            )
            
            # Delete sale
            db.execute_query("DELETE FROM sales WHERE sale_id = %s", (sale_id,))
            
            return jsonify({'success': True, 'message': 'Sale deleted successfully'})
        except Exception as e:
            return jsonify({'success': False, 'message': str(e)})

    @app.route('/api/sales_stats')
    def api_sales_stats():
        """Get sales statistics"""
        try:
            total_revenue = db.execute_query("SELECT SUM(total_amount) as total FROM sales", fetch=True)[0]['total'] or 0
            total_sales = db.execute_query("SELECT COUNT(*) as count FROM sales", fetch=True)[0]['count']
            avg_sale_value = db.execute_query("SELECT AVG(total_amount) as avg FROM sales", fetch=True)[0]['avg'] or 0
            
            # Today's sales
            today_sales = db.execute_query(
                "SELECT COUNT(*) as count FROM sales WHERE sale_date = CURDATE()", 
                fetch=True
            )[0]['count']
            
            # Top payment method
            top_payment = db.execute_query("""
                SELECT payment_method, COUNT(*) as count 
                FROM sales 
                GROUP BY payment_method 
                ORDER BY count DESC 
                LIMIT 1
            """, fetch=True)
            top_payment_method = top_payment[0]['payment_method'] if top_payment else 'N/A'
            
            return jsonify({
                'success': True,
                'total_revenue': float(total_revenue),
                'total_sales': total_sales,
                'avg_sale_value': f"${float(avg_sale_value):.2f}",
                'today_sales': today_sales,
                'top_payment_method': top_payment_method
            })
        except Exception as e:
            return jsonify({'success': False, 'message': str(e)})