# app/routes.py

from flask import jsonify, request
from app import app, db
from app.models import Item

# Define routes
@app.route('/api/items', methods=['GET'])
def get_items():
    items = Item.query.all()
    items_json = [{'id': item.id, 'name': item.name, 'category': item.category, 'storage_location': item.storage_location, 'expiration_date': str(item.expiration_date), 'used': item.used} for item in items]
    return jsonify({'items': items_json})

@app.route('/api/items', methods=['POST'])
def add_item():
    data = request.json
    item = Item(name=data['name'], category=data['category'], storage_location=data['storage_location'], expiration_date=data.get('expiration_date'), used=False)
    db.session.add(item)
    db.session.commit()
    return jsonify({'message': 'Item added successfully'})

@app.route('/api/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    data = request.json
    item = Item.query.get_or_404(item_id)
    item.name = data['name']
    item.category = data['category']
    item.storage_location = data['storage_location']
    item.expiration_date = data.get('expiration_date')
    db.session.commit()
    return jsonify({'message': 'Item updated successfully'})

@app.route('/api/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    item = Item.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    return jsonify({'message': 'Item deleted successfully'})
