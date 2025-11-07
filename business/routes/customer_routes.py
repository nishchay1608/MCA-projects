# routes/customer_routes.py
from flask import jsonify, request, render_template

def init_customer_routes(app, db):
    """Initialize customer routes"""
    
    @app.route('/customers')
    def manage_customers():
        """Customer management page"""
        return render_template('customers.html')

    @app.route('/api/customers', methods=['GET'])
    def api_get_customers():
        """Get all customers"""
        try:
            customers = db.execute_query("SELECT * FROM customers ORDER BY customer_id DESC", fetch=True)
            return jsonify({'success': True, 'customers': customers})
        except Exception as e:
            return jsonify({'success': False, 'message': str(e)})

    @app.route('/api/customers', methods=['POST'])
    def api_add_customer():
        """Add new customer"""
        try:
            data = request.json
            query = """
                INSERT INTO customers (name, email, phone, city, country, customer_type, registration_date)
                VALUES (%s, %s, %s, %s, %s, %s, CURDATE())
            """
            db.execute_query(query, (
                data['name'],
                data.get('email'),
                data.get('phone'),
                data.get('city'),
                data.get('country'),
                data.get('customer_type', 'Regular')
            ))
            return jsonify({'success': True, 'message': 'Customer added successfully'})
        except Exception as e:
            return jsonify({'success': False, 'message': str(e)})

    @app.route('/api/customers/<int:customer_id>', methods=['GET'])
    def api_get_customer(customer_id):
        """Get single customer"""
        try:
            customer = db.execute_query(
                "SELECT * FROM customers WHERE customer_id = %s", 
                (customer_id,), 
                fetch=True
            )
            if customer:
                return jsonify({'success': True, 'customer': customer[0]})
            else:
                return jsonify({'success': False, 'message': 'Customer not found'})
        except Exception as e:
            return jsonify({'success': False, 'message': str(e)})

    @app.route('/api/customers/<int:customer_id>', methods=['PUT'])
    def api_update_customer(customer_id):
        """Update customer"""
        try:
            data = request.json
            query = """
                UPDATE customers 
                SET name = %s, email = %s, phone = %s, city = %s, country = %s, customer_type = %s
                WHERE customer_id = %s
            """
            db.execute_query(query, (
                data['name'],
                data.get('email'),
                data.get('phone'),
                data.get('city'),
                data.get('country'),
                data.get('customer_type', 'Regular'),
                customer_id
            ))
            return jsonify({'success': True, 'message': 'Customer updated successfully'})
        except Exception as e:
            return jsonify({'success': False, 'message': str(e)})

    @app.route('/api/customers/<int:customer_id>', methods=['DELETE'])
    def api_delete_customer(customer_id):
        """Delete customer"""
        try:
            db.execute_query("DELETE FROM customers WHERE customer_id = %s", (customer_id,))
            return jsonify({'success': True, 'message': 'Customer deleted successfully'})
        except Exception as e:
            return jsonify({'success': False, 'message': str(e)})

    @app.route('/api/customer_stats')
    def api_customer_stats():
        """Get customer statistics"""
        try:
            total_customers = db.execute_query("SELECT COUNT(*) as count FROM customers", fetch=True)[0]['count']
            premium_customers = db.execute_query("SELECT COUNT(*) as count FROM customers WHERE customer_type = 'Premium'", fetch=True)[0]['count']
            regular_customers = db.execute_query("SELECT COUNT(*) as count FROM customers WHERE customer_type = 'Regular'", fetch=True)[0]['count']
            vip_customers = db.execute_query("SELECT COUNT(*) as count FROM customers WHERE customer_type = 'VIP'", fetch=True)[0]['count']
            
            return jsonify({
                'success': True,
                'total_customers': total_customers,
                'premium_customers': premium_customers,
                'regular_customers': regular_customers,
                'vip_customers': vip_customers
            })
        except Exception as e:
            return jsonify({'success': False, 'message': str(e)})