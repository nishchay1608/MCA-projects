class CustomerAnalyzer:
    def __init__(self, db):
        self.db = db
    
    def get_customer_segmentation(self):
        """Segment customers by value"""
        query = """
        SELECT 
            c.customer_type,
            COUNT(DISTINCT c.customer_id) as customer_count,
            SUM(s.total_amount) as total_revenue,
            AVG(s.total_amount) as avg_revenue_per_customer,
            COUNT(s.sale_id) as total_transactions
        FROM customers c
        LEFT JOIN sales s ON c.customer_id = s.customer_id
        GROUP BY c.customer_type
        ORDER BY total_revenue DESC
        """
        return self.db.execute_query(query, fetch=True)
    
    def get_top_customers(self, limit=10):
        """Get top customers by revenue"""
        query = """
        SELECT 
            c.name,
            c.customer_type,
            c.city,
            COUNT(s.sale_id) as purchase_count,
            SUM(s.total_amount) as total_spent,
            MAX(s.sale_date) as last_purchase
        FROM customers c
        JOIN sales s ON c.customer_id = s.customer_id
        GROUP BY c.customer_id, c.name, c.customer_type, c.city
        ORDER BY total_spent DESC
        LIMIT %s
        """
        return self.db.execute_query(query, (limit,), fetch=True)
    
    def get_customer_acquisition_trend(self):
        """Track customer acquisition over time"""
        query = """
        SELECT 
            DATE_FORMAT(registration_date, '%Y-%m') as month,
            COUNT(*) as new_customers,
            customer_type
        FROM customers
        GROUP BY DATE_FORMAT(registration_date, '%Y-%m'), customer_type
        ORDER BY month
        """
        return self.db.execute_query(query, fetch=True)