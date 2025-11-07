# routes/analytics_routes.py
from flask import jsonify, request, render_template

def init_analytics_routes(app, db):
    """Initialize analytics routes"""
    
    @app.route('/analytics')
    def view_analytics():
        """Analytics dashboard"""
        return render_template('analytics.html')

    @app.route('/api/analytics/sales_over_time')
    def api_sales_over_time():
        """Get sales data over time for charts"""
        try:
            # Sales by month
            monthly_sales = db.execute_query("""
                SELECT DATE_FORMAT(sale_date, '%%Y-%%m') as month, 
                       SUM(total_amount) as total_sales,
                       COUNT(*) as transaction_count
                FROM sales 
                GROUP BY DATE_FORMAT(sale_date, '%%Y-%%m')
                ORDER BY month DESC
                LIMIT 12
            """, fetch=True)
            
            return jsonify({
                'success': True,
                'monthly_sales': monthly_sales[::-1]
            })
        except Exception as e:
            return jsonify({'success': False, 'message': str(e)})

    @app.route('/api/analytics/top_products')
    def api_top_products():
        """Get top selling products"""
        try:
            top_products = db.execute_query("""
                SELECT p.product_name, 
                       SUM(si.quantity) as total_sold,
                       SUM(si.quantity * si.unit_price) as total_revenue
                FROM sales_items si
                JOIN products p ON si.product_id = p.product_id
                GROUP BY p.product_id, p.product_name
                ORDER BY total_sold DESC
                LIMIT 10
            """, fetch=True)
            
            return jsonify({
                'success': True,
                'top_products': top_products
            })
        except Exception as e:
            return jsonify({'success': False, 'message': str(e)})

    @app.route('/api/analytics/expense_trends')
    def api_expense_trends():
        """Get expense trends over time"""
        try:
            monthly_expenses = db.execute_query("""
                SELECT DATE_FORMAT(expense_date, '%%Y-%%m') as month,
                       SUM(amount) as total_expenses,
                       COUNT(*) as expense_count
                FROM expenses
                GROUP BY DATE_FORMAT(expense_date, '%%Y-%%m')
                ORDER BY month DESC
                LIMIT 12
            """, fetch=True)
            
            return jsonify({
                'success': True,
                'monthly_expenses': monthly_expenses[::-1]
            })
        except Exception as e:
            return jsonify({'success': False, 'message': str(e)})

    @app.route('/api/analytics/profitability')
    def api_profitability():
        """Get profitability data"""
        try:
            # Monthly profit/loss
            monthly_data = db.execute_query("""
                SELECT 
                    months.month,
                    COALESCE(sales.total_sales, 0) as revenue,
                    COALESCE(expenses.total_expenses, 0) as expenses,
                    (COALESCE(sales.total_sales, 0) - COALESCE(expenses.total_expenses, 0)) as net_profit
                FROM (
                    SELECT DATE_FORMAT(DATE_SUB(CURDATE(), INTERVAL n MONTH), '%%Y-%%m') as month
                    FROM (SELECT 0 as n UNION SELECT 1 UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 
                          UNION SELECT 5 UNION SELECT 6 UNION SELECT 7 UNION SELECT 8 
                          UNION SELECT 9 UNION SELECT 10 UNION SELECT 11) months
                ) months
                LEFT JOIN (
                    SELECT DATE_FORMAT(sale_date, '%%Y-%%m') as month, 
                           SUM(total_amount) as total_sales
                    FROM sales 
                    GROUP BY DATE_FORMAT(sale_date, '%%Y-%%m')
                ) sales ON months.month = sales.month
                LEFT JOIN (
                    SELECT DATE_FORMAT(expense_date, '%%Y-%%m') as month,
                           SUM(amount) as total_expenses
                    FROM expenses
                    GROUP BY DATE_FORMAT(expense_date, '%%Y-%%m')
                ) expenses ON months.month = expenses.month
                WHERE months.month <= DATE_FORMAT(CURDATE(), '%%Y-%%m')
                ORDER BY months.month DESC
                LIMIT 12
            """, fetch=True)
            
            return jsonify({
                'success': True,
                'monthly_data': monthly_data[::-1]
            })
        except Exception as e:
            return jsonify({'success': False, 'message': str(e)})

    @app.route('/api/analytics/customer_insights')
    def api_customer_insights():
        """Get customer analytics"""
        try:
            # Top customers
            top_customers = db.execute_query("""
                SELECT c.customer_name, 
                       COUNT(s.sale_id) as purchase_count,
                       SUM(s.total_amount) as total_spent
                FROM customers c
                LEFT JOIN sales s ON c.customer_id = s.customer_id
                GROUP BY c.customer_id, c.customer_name
                HAVING total_spent > 0
                ORDER BY total_spent DESC
                LIMIT 10
            """, fetch=True)
            
            # Customer growth
            customer_growth = db.execute_query("""
                SELECT DATE_FORMAT(created_at, '%%Y-%%m') as month,
                       COUNT(*) as new_customers
                FROM customers
                GROUP BY DATE_FORMAT(created_at, '%%Y-%%m')
                ORDER BY month DESC
                LIMIT 12
            """, fetch=True)
            
            return jsonify({
                'success': True,
                'top_customers': top_customers,
                'customer_growth': customer_growth[::-1]
            })
        except Exception as e:
            return jsonify({'success': False, 'message': str(e)})

    @app.route('/api/analytics/overview_metrics')
    def api_overview_metrics():
        """Get overview metrics for dashboard"""
        try:
            # Total metrics
            total_revenue = db.execute_query("SELECT SUM(total_amount) as total FROM sales", fetch=True)[0]['total'] or 0
            total_expenses = db.execute_query("SELECT SUM(amount) as total FROM expenses", fetch=True)[0]['total'] or 0
            total_customers = db.execute_query("SELECT COUNT(*) as count FROM customers", fetch=True)[0]['count']
            total_products = db.execute_query("SELECT COUNT(*) as count FROM products", fetch=True)[0]['count']
            
            # This month metrics
            current_month_revenue = db.execute_query("""
                SELECT SUM(total_amount) as total FROM sales 
                WHERE DATE_FORMAT(sale_date, '%%Y-%%m') = DATE_FORMAT(CURDATE(), '%%Y-%%m')
            """, fetch=True)[0]['total'] or 0
            
            current_month_expenses = db.execute_query("""
                SELECT SUM(amount) as total FROM expenses 
                WHERE DATE_FORMAT(expense_date, '%%Y-%%m') = DATE_FORMAT(CURDATE(), '%%Y-%%m')
            """, fetch=True)[0]['total'] or 0
            
            # Today's metrics
            today_revenue = db.execute_query("""
                SELECT SUM(total_amount) as total FROM sales 
                WHERE DATE(sale_date) = CURDATE()
            """, fetch=True)[0]['total'] or 0
            
            net_profit = total_revenue - total_expenses
            current_month_profit = current_month_revenue - current_month_expenses
            
            return jsonify({
                'success': True,
                'metrics': {
                    'total_revenue': float(total_revenue),
                    'total_expenses': float(total_expenses),
                    'net_profit': float(net_profit),
                    'total_customers': total_customers,
                    'total_products': total_products,
                    'current_month_revenue': float(current_month_revenue),
                    'current_month_expenses': float(current_month_expenses),
                    'current_month_profit': float(current_month_profit),
                    'today_revenue': float(today_revenue)
                }
            })
        except Exception as e:
            return jsonify({'success': False, 'message': str(e)})