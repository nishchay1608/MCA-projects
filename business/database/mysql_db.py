import pymysql
from flask import Flask
import pandas as pd

class BusinessDB:
    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)
    
    def init_app(self, app):
        self.host = app.config['MYSQL_HOST']
        self.user = app.config['MYSQL_USER']
        self.password = app.config['MYSQL_PASSWORD']
        self.db = app.config['MYSQL_DB']
        self.create_database()
    
    def get_connection(self):
        return pymysql.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.db,
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
    
    def create_database(self):
        """Create database and tables without sample data"""
        # First connect without specific database
        conn = pymysql.connect(
            host=self.host,
            user=self.user,
            password=self.password
        )
        
        try:
            with conn.cursor() as cursor:
                cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.db}")
                cursor.execute(f"USE {self.db}")
                
                # Customers table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS customers (
                        customer_id INT AUTO_INCREMENT PRIMARY KEY,
                        name VARCHAR(100) NOT NULL,
                        email VARCHAR(150),
                        phone VARCHAR(20),
                        city VARCHAR(50),
                        country VARCHAR(50),
                        registration_date DATE,
                        customer_type ENUM('Regular', 'Premium', 'VIP') DEFAULT 'Regular',
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                
                # Products table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS products (
                        product_id INT AUTO_INCREMENT PRIMARY KEY,
                        product_name VARCHAR(200) NOT NULL,
                        category VARCHAR(100),
                        subcategory VARCHAR(100),
                        price DECIMAL(10,2),
                        cost_price DECIMAL(10,2),
                        stock_quantity INT DEFAULT 0,
                        supplier VARCHAR(100),
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                
                # Sales table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS sales (
                        sale_id INT AUTO_INCREMENT PRIMARY KEY,
                        customer_id INT,
                        product_id INT,
                        sale_date DATE,
                        quantity INT,
                        unit_price DECIMAL(10,2),
                        total_amount DECIMAL(10,2),
                        payment_method ENUM('Cash', 'Credit Card', 'Digital Wallet', 'Bank Transfer') DEFAULT 'Cash',
                        region VARCHAR(50),
                        sales_person VARCHAR(100),
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
                        FOREIGN KEY (product_id) REFERENCES products(product_id)
                    )
                """)
                
                # Expenses table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS expenses (
                        expense_id INT AUTO_INCREMENT PRIMARY KEY,
                        expense_date DATE,
                        category VARCHAR(100),
                        description TEXT,
                        amount DECIMAL(10,2),
                        payment_method VARCHAR(50),
                        receipt_info VARCHAR(255),
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                
            conn.commit()
            print("Database and tables created successfully!")
            print("Tables created: customers, products, sales, expenses")
                
        except Exception as e:
            print(f"Error creating database: {e}")
            raise
        finally:
            conn.close()
    
    def execute_query(self, query, params=None, fetch=False):
        """Execute SQL query and return results"""
        conn = self.get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(query, params or ())
                
                if fetch:
                    if query.strip().upper().startswith('SELECT') or query.strip().upper().startswith('SHOW'):
                        result = cursor.fetchall()
                    else:
                        result = cursor.fetchone()
                    return result
                else:
                    conn.commit()
                    return cursor.rowcount
        except Exception as e:
            conn.rollback()
            print(f"Query error: {e}")
            raise e
        finally:
            conn.close()
    
    def get_dataframe(self, query, params=None):
        """Execute query and return pandas DataFrame"""
        conn = self.get_connection()
        try:
            return pd.read_sql(query, conn, params=params)
        except Exception as e:
            print(f"DataFrame error: {e}")
            raise
        finally:
            conn.close()
    
    def check_connection(self):
        """Check if database connection is working"""
        try:
            conn = self.get_connection()
            with conn.cursor() as cursor:
                cursor.execute("SELECT 1 as test")
                result = cursor.fetchone()
            conn.close()
            return result['test'] == 1
        except Exception as e:
            print(f"Connection check failed: {e}")
            return False
    
    def get_table_info(self):
        """Get information about all tables"""
        try:
            tables = self.execute_query("SHOW TABLES", fetch=True)
            table_info = {}
            
            for table in tables:
                table_name = list(table.values())[0]
                columns = self.execute_query(f"DESCRIBE {table_name}", fetch=True)
                table_info[table_name] = columns
            
            return table_info
        except Exception as e:
            print(f"Error getting table info: {e}")
            return {}