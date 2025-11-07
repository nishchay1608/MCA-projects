# routes/product_routes.py
from flask import jsonify, request, render_template

def init_product_routes(app, db):
    """Initialize product routes"""
    
    @app.route('/products')
    def manage_products():
        """Product management page"""
        return render_template('products.html')

    @app.route('/api/products', methods=['GET'])
    def api_get_products():
        """Get all products"""
        try:
            products = db.execute_query("SELECT * FROM products ORDER BY product_id DESC", fetch=True)
            return jsonify({'success': True, 'products': products})
        except Exception as e:
            return jsonify({'success': False, 'message': str(e)})

    @app.route('/api/products', methods=['POST'])
    def api_add_product():
        """Add new product"""
        try:
            data = request.json
            query = """
                INSERT INTO products (product_name, category, subcategory, price, cost_price, stock_quantity, supplier)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            db.execute_query(query, (
                data['product_name'],
                data['category'],
                data.get('subcategory'),
                data['price'],
                data.get('cost_price', 0),
                data.get('stock_quantity', 0),
                data.get('supplier')
            ))
            return jsonify({'success': True, 'message': 'Product added successfully'})
        except Exception as e:
            return jsonify({'success': False, 'message': str(e)})

    @app.route('/api/products/<int:product_id>', methods=['GET'])
    def api_get_product(product_id):
        """Get single product"""
        try:
            product = db.execute_query(
                "SELECT * FROM products WHERE product_id = %s", 
                (product_id,), 
                fetch=True
            )
            if product:
                return jsonify({'success': True, 'product': product[0]})
            else:
                return jsonify({'success': False, 'message': 'Product not found'})
        except Exception as e:
            return jsonify({'success': False, 'message': str(e)})

    @app.route('/api/products/<int:product_id>', methods=['PUT'])
    def api_update_product(product_id):
        """Update product"""
        try:
            data = request.json
            query = """
                UPDATE products 
                SET product_name = %s, category = %s, subcategory = %s, price = %s, 
                    cost_price = %s, stock_quantity = %s, supplier = %s
                WHERE product_id = %s
            """
            db.execute_query(query, (
                data['product_name'],
                data['category'],
                data.get('subcategory'),
                data['price'],
                data.get('cost_price', 0),
                data.get('stock_quantity', 0),
                data.get('supplier'),
                product_id
            ))
            return jsonify({'success': True, 'message': 'Product updated successfully'})
        except Exception as e:
            return jsonify({'success': False, 'message': str(e)})

    @app.route('/api/products/<int:product_id>', methods=['DELETE'])
    def api_delete_product(product_id):
        """Delete product"""
        try:
            db.execute_query("DELETE FROM products WHERE product_id = %s", (product_id,))
            return jsonify({'success': True, 'message': 'Product deleted successfully'})
        except Exception as e:
            return jsonify({'success': False, 'message': str(e)})

    @app.route('/api/product_stats')
    def api_product_stats():
        """Get product statistics"""
        try:
            total_products = db.execute_query("SELECT COUNT(*) as count FROM products", fetch=True)[0]['count']
            low_stock = db.execute_query("SELECT COUNT(*) as count FROM products WHERE stock_quantity < 10 AND stock_quantity > 0", fetch=True)[0]['count']
            out_of_stock = db.execute_query("SELECT COUNT(*) as count FROM products WHERE stock_quantity = 0", fetch=True)[0]['count']
            categories = db.execute_query("SELECT COUNT(DISTINCT category) as count FROM products", fetch=True)[0]['count']
            
            return jsonify({
                'success': True,
                'total_products': total_products,
                'low_stock': low_stock,
                'out_of_stock': out_of_stock,
                'categories': categories
            })
        except Exception as e:
            return jsonify({'success': False, 'message': str(e)})