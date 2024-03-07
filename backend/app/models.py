from app import db
from datetime import datetime


class Status(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)

    def __repr__(self):
        return f"Status('{self.name}')"


class Storage_Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)

    def __repr__(self):
        return f"Storage_Location('{self.name}')"
    

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)

    def __repr__(self):
        return f"Category('{self.name}')"
    
class Unit_Of_Measure(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)

    def __repr__(self):
        return f"Unit_Of_Measure('{self.name}')"    
    

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    category = db.relationship('Category', backref=db.backref('items', lazy=True))
    unit_of_measure_id = db.Column(db.Integer, db.ForeignKey('unit_of_measure.id'), nullable=False)
    unit_of_measure = db.relationship('Unit_Of_Measure', backref=db.backref('items', lazy=True))
    days_to_expiration = db.Column(db.Integer, nullable=False)
    
    def __repr__(self):
        return f"Item('{self.name}', '{self.category}')"


class Supplier(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)

    def __repr__(self):
        return f"Supplier('{self.name}')"
    

class Inventory_Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False)
    item = db.relationship('Item', backref=db.backref('inventory_items', lazy=True))
    storage_location_id = db.Column(db.Integer, db.ForeignKey('storage_location.id'), nullable=False)
    storage_location = db.relationship('Storage_Location', backref=db.backref('inventory_items', lazy=True))
    added_date = db.Column(db.Date)
    quantity = db.Column(db.Integer, nullable=False)
    supplier_id = db.Column(db.Integer, db.ForeignKey('supplier.id'), nullable=False)
    supplier = db.relationship('Supplier', backref=db.backref('inventory_items', lazy=True))
    expiration_date = db.Column(db.Date)
    gone = db.Column(db.Boolean)
    
    def __repr__(self):
        return f"Inventory_Item('{self.item.name}', '{self.item.category.name}', '{self.storage_location}')"
    

class TransactionHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    inventory_item_id = db.Column(db.Integer, db.ForeignKey('inventory_item.id'), nullable=False)
    inventory_item = db.relationship('Inventory_Item', backref=db.backref('transactions', lazy=True))
    transaction_type = db.Column(db.String(50), nullable=False)
    new_status_id = db.Column(db.Integer, db.ForeignKey('status.id'), nullable=False)
    new_status = db.relationship('Status', backref=db.backref('transactions', lazy=True))
    quantity = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"TransactionHistory('{self.item.name}', '{self.transaction_type}', '{self.quantity}', '{self.timestamp}')"
