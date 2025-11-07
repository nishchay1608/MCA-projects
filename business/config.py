import os

class Config:
    SECRET_KEY = 'business-analytics-secret-key-2024'
    
    # MySQL Configuration
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = 'Gautam@1234'  # Change to your MySQL password
    MYSQL_DB = 'business_analytics'
    MYSQL_CURSORCLASS = 'DictCursor'

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False