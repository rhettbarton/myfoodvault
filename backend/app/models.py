from app import db
from datetime import datetime
from enum import Enum

#Should match backend\webscrape\data\stilltasty_food_categories.csv
class Category(Enum):
    FRUITS = 'Fruits'
    VEGETABLES = 'Vegetables'
    DAIRY_AND_EGGS = 'Dairy & Eggs'
    MEAT_AND_POULTRY = 'Meat & Poultry'
    FISH_AND_SHELLFISH = 'Fish & Shellfish'
    NUTS,_GRAINS_AND_PASTA = 'Nuts, Grains & Pasta'
    CONDIMENTS_AND_OILS = 'Condiments & Oils'
    SNACKS_AND_BAKED_GOODS = 'Snacks & Baked Goods'
    HERBS_AND_SPICES = 'Herbs & Spices'
    BEVERAGES = 'Beverages'


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
    FARMERS_MARKET = 'Farmers Market'
    OTHER = 'Other'


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.Enum(Category), nullable=False)
    food_tips = db.Column(db.String(1000), nullable=False)
    url = db.Column(db.String(100), nullable=False)
    refrigerator_min_shelf_life = db.Column(db.Integer, nullable=False)
    refrigerator_max_shelf_life = db.Column(db.Integer, nullable=False)
    pantry_min_shelf_life = db.Column(db.Integer, nullable=False)
    pantry_max_shelf_life = db.Column(db.Integer, nullable=False)
    freezer_min_shelf_life = db.Column(db.Integer, nullable=False)
    freezer_max_shelf_life = db.Column(db.Integer, nullable=False)
    storage_locations = db.Column(db.String(100), nullable=False)
    unit_of_measure = db.Column(db.Enum(Unit_Of_Measure), nullable=False)

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
    note = db.Column(db.String(1000))
    
    def __repr__(self):
        return f"Inventory_Item('{self.item.name}', '{self.item.category.name}', '{self.storage_location}')"


class Inventory_History(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    inventory_item_id = db.Column(db.Integer, db.ForeignKey('inventory_item.id'), nullable=False)
    inventory_item = db.relationship('Inventory_Item', backref=db.backref('history', lazy=True))
    update_status = db.Column(db.Boolean)
    update_quantity = db.Column(db.Boolean)
    update_location = db.Column(db.Boolean)
    status = db.Column(db.Enum(Status))
    quantity = db.Column(db.Integer)
    storage_location = db.Column(db.Enum(Storage_Location))
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"Inventory_History('{self.item.name}', '{self.transaction_type}', '{self.quantity}', '{self.timestamp}')"