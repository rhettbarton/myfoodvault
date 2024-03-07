from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
# Import routes (importing here to avoid circular imports)
from app import routes

# Create Flask app instance
app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY')
app.config['ENVIRONMENT'] = os.environ.get('FLASK_ENV')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/food_inventory.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Conditionally initialize and create database tables
if app.config['ENVIRONMENT'] == 'dev':
    # Import models
    from app import models
    # Initialize database
    db = SQLAlchemy(app)
    # Create database tables
    db.create_all()
