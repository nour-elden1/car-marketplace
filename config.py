import os

class Config:
    """Base configuration"""
    SECRET_KEY = 'your-secret-key-here-change-in-production'
    
    # MySQL Database Configuration
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:123456@127.0.0.1/car_marketplace'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Upload configuration
    UPLOAD_FOLDER = 'static/uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    
    # Session configuration
    PERMANENT_SESSION_LIFETIME = 3600  # 1 hour
