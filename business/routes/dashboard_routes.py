# routes/dashboard_routes.py
from flask import jsonify,render_template
from database.mysql_db import BusinessDB
from analytics.sales_analyzer import SalesAnalyzer

def init_dashboard_routes(app, db, sales_analyzer):
    """Initialize dashboard routes"""
    
    @app.route('/')
    def dashboard():
        """Main dashboard"""
        return render_template('dashboard.html')

    @app.route('/api/dashboard_stats')
    def api_dashboard_stats():
        """Get dashboard statistics"""
        try:
            # Get sales summary
            sales_summary = sales_analyzer.get_sales_summary()
            
            # Get recent sales (last 5)
            recent_sales = db.execute_query("""
                SELECT s.sale_id, s.total_amount, s.quantity, s.sale_date, p.product_name
                FROM sales s
                JOIN products p ON s.product_id = p.product_id
                ORDER BY s.sale_date DESC
                LIMIT 5
            """, fetch=True)
            
            # Get top products
            top_products = sales_analyzer.get_top_products(5)
            
            # Get total customers and products
            total_customers = db.execute_query("SELECT COUNT(*) as count FROM customers", fetch=True)[0]['count']
            total_products = db.execute_query("SELECT COUNT(*) as count FROM products", fetch=True)[0]['count']
            
            return jsonify({
                'success': True,
                'total_revenue': float(sales_summary['total_revenue']) if sales_summary['total_revenue'] else 0,
                'total_sales': sales_summary['total_sales'],
                'total_customers': total_customers,
                'total_products': total_products,
                'recent_sales': recent_sales,
                'top_products': top_products
            })
        except Exception as e:
            return jsonify({'success': False, 'message': str(e)})