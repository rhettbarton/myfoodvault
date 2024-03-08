from app import db
from datetime import datetime
from enum import Enum


class Category(Enum):
    DAIRY = 'Dairy'
    PRODUCE = 'Produce'
    MEAT = 'Meat'
    SEAFOOD = 'Seafood'
    BAKERY = 'Bakery'
    BEVERAGES = 'Beverages'
    FROZEN_FOODS = 'Frozen Foods'
    BREAD = 'Bread'
    CANNED_GOODS = 'Canned Goods'
    GRAINS_AND_PASTA = 'Grains and Pasta'
    CONDIMENTS_AND_SAUCES = 'Condiments and Sauces'
    SNACKS_AND_CHIPS = 'Snacks and Chips'
    BEVERAGES = 'Beverages'
    FROZEN_FOODS = 'Frozen Foods'
    DELI_AND_PREPARED_FOODS = 'Deli and Prepared Foods'
    BREAKFAST_FOODS = 'Breakfast Foods'
    BAKING_SUPPLIES = 'Baking Supplies'
    SPICES_AND_SEASONINGS = 'Spices and Seasonings'
    COOKING_OILS_AND_VINEGARS = 'Cooking Oils and Vinegars'
    HEALTH_AND_WELLNESS_PRODUCTS = 'Health and Wellness Products'
    MISCELLANEOUS_ITEMS = 'Miscellaneous Items'


class Status(Enum):
    AVAILABLE = 'Available'
    DISCARDED = 'Discarded'
    CONSUMED = 'Consumed'


class Storage_Location(Enum):
    FRIDGE = 'Fridge'
    INSIDE_FREEZER = 'Inside Freezer'
    OUTSIDE_FREEZER = 'Outside Freezer'
    PANTRY = 'Pantry'
    STORAGE_ROOM = 'Storage Room'
    CABINETS = 'Cabinets'

    
class Unit_Of_Measure(Enum):
    CONTAINER = 'Container(s)'
    PIECE = 'Piece(s)'
    

class Supplier(db.Model):
    WALMART = 'Walmart'
    ALBERTSONS = 'Albertsons'
    WINCO = 'WinCo'
    COSTCO = 'Costco'
    AMAZON = 'Amazon'
    FRED_MEYER = 'Fred Meyer'


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.Enum(Category), nullable=False)
    unit_of_measure = db.Column(db.Enum(Unit_Of_Measure), nullable=False)
    days_to_expiration = db.Column(db.Integer, nullable=False)
    
    def __repr__(self):
        return f"Item('{self.name}', '{self.category}')"


class Inventory_Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False)
    item = db.relationship('Item', backref=db.backref('inventory_items', lazy=True))
    storage_location = db.Column(db.Enum(Storage_Location), nullable=False)
    added_date = db.Column(db.Date)
    quantity = db.Column(db.Integer, nullable=False)
    supplier = db.Column(db.Enum(Supplier), nullable=False)
    expiration_date = db.Column(db.Date)
    status = db.Column(db.Enum(Status), nullable=False)
    
    def __repr__(self):
        return f"Inventory_Item('{self.item.name}', '{self.item.category.name}', '{self.storage_location}')"


class Inventory_History(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    inventory_item_id = db.Column(db.Integer, db.ForeignKey('inventory_item.id'), nullable=False)
    inventory_item = db.relationship('Inventory_Item', backref=db.backref('history', lazy=True))
    update_status = db.Column(db.Boolean)
    update_quantity = db.Column(db.Boolean)
    status = db.Column(db.Enum(Status), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"Inventory_History('{self.item.name}', '{self.transaction_type}', '{self.quantity}', '{self.timestamp}')"