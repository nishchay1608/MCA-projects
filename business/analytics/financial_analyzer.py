class FinancialAnalyzer:
    def __init__(self, db):
        self.db = db
    
    def get_profit_analysis(self):
        """Calculate profit margins"""
        query = """
        SELECT 
            p.category,
            SUM(s.quantity) as units_sold,
            SUM(s.total_amount) as revenue,
            SUM(s.quantity * p.cost_price) as total_cost,
            SUM(s.total_amount - (s.quantity * p.cost_price)) as profit,
            (SUM(s.total_amount - (s.quantity * p.cost_price)) / SUM(s.total_amount)) * 100 as profit_margin
        FROM sales s
        JOIN products p ON s.product_id = p.product_id
        GROUP BY p.category
        ORDER BY profit DESC
        """
        return self.db.execute_query(query, fetch=True)
    
    def get_expense_analysis(self):
        """Analyze expenses by category"""
        query = """
        SELECT 
            category,
            SUM(amount) as total_amount,
            COUNT(*) as transaction_count,
            AVG(amount) as average_expense
        FROM expenses
        GROUP BY category
        ORDER BY total_amount DESC
        """
        return self.db.execute_query(query, fetch=True)
    
    def get_cash_flow(self):
        """Get monthly cash flow"""
        query = """
        SELECT 
            'Revenue' as type,
            DATE_FORMAT(sale_date, '%Y-%m') as month,
            SUM(total_amount) as amount
        FROM sales
        GROUP BY DATE_FORMAT(sale_date, '%Y-%m')
        
        UNION ALL
        
        SELECT 
            'Expense' as type,
            DATE_FORMAT(expense_date, '%Y-%m') as month,
            -SUM(amount) as amount
        FROM expenses
        GROUP BY DATE_FORMAT(expense_date, '%Y-%m')
        
        ORDER BY month, type
        """
        return self.db.execute_query(query, fetch=True)