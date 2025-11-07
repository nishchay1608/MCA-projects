import pandas as pd
import numpy as np
from datetime import datetime, timedelta

class SalesAnalyzer:
    def __init__(self, db):
        self.db = db
    
    def get_sales_summary(self):
        """Get overall sales summary"""
        query = """
        SELECT 
            COUNT(*) as total_sales,
            SUM(total_amount) as total_revenue,
            AVG(total_amount) as average_sale,
            SUM(quantity) as total_units_sold,
            COUNT(DISTINCT customer_id) as unique_customers
        FROM sales
        """
        return self.db.execute_query(query, fetch=True)[0]
    
    def get_sales_trend(self, period='monthly'):
        """Get sales trend over time"""
        if period == 'monthly':
            group_by = "DATE_FORMAT(sale_date, '%Y-%m')"
        else:  # weekly
            group_by = "YEARWEEK(sale_date)"
        
        query = f"""
        SELECT 
            {group_by} as period,
            SUM(total_amount) as revenue,
            COUNT(*) as sales_count,
            SUM(quantity) as units_sold
        FROM sales
        GROUP BY {group_by}
        ORDER BY period
        """
        return self.db.execute_query(query, fetch=True)
    
    def get_top_products(self, limit=10):
        """Get top selling products"""
        query = """
        SELECT 
            p.product_name,
            p.category,
            SUM(s.quantity) as total_units,
            SUM(s.total_amount) as total_revenue,
            COUNT(*) as sales_count
        FROM sales s
        JOIN products p ON s.product_id = p.product_id
        GROUP BY p.product_id, p.product_name, p.category
        ORDER BY total_revenue DESC
        LIMIT %s
        """
        return self.db.execute_query(query, (limit,), fetch=True)
    
    def get_sales_by_region(self):
        """Get sales distribution by region"""
        query = """
        SELECT 
            region,
            SUM(total_amount) as revenue,
            COUNT(*) as sales_count,
            SUM(quantity) as units_sold
        FROM sales
        GROUP BY region
        ORDER BY revenue DESC
        """
        return self.db.execute_query(query, fetch=True)
    
    def get_payment_method_analysis(self):
        """Analyze payment method preferences"""
        query = """
        SELECT 
            payment_method,
            COUNT(*) as transaction_count,
            SUM(total_amount) as total_amount,
            AVG(total_amount) as average_transaction
        FROM sales
        GROUP BY payment_method
        ORDER BY total_amount DESC
        """
        return self.db.execute_query(query, fetch=True)