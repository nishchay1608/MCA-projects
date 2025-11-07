# app.py
from flask import Flask, render_template
from config import DevelopmentConfig
from database.mysql_db import BusinessDB
from analytics.sales_analyzer import SalesAnalyzer
from analytics.customer_analyzer import CustomerAnalyzer
from analytics.financial_analyzer import FinancialAnalyzer

# Import route modules
from routes.dashboard_routes import init_dashboard_routes
from routes.customer_routes import init_customer_routes
from routes.product_routes import init_product_routes
from routes.sales_routes import init_sales_routes
from routes.expense_routes import init_expense_routes
from routes.analytics_routes import init_analytics_routes

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)

# Initialize database and analyzers
db = BusinessDB(app)
sales_analyzer = SalesAnalyzer(db)
customer_analyzer = CustomerAnalyzer(db)
financial_analyzer = FinancialAnalyzer(db)

# Initialize all routes
init_dashboard_routes(app, db, sales_analyzer)
init_customer_routes(app, db)
init_product_routes(app, db)
init_sales_routes(app, db)
init_expense_routes(app, db)
init_analytics_routes(app, db)

if __name__ == '__main__':
    app.run(debug=True, port=5001)