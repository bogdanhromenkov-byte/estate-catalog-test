from flask import Blueprint, jsonify, request
from models import db, Property

api = Blueprint('api', __name__, url_prefix='/api')

@api.route('/properties', methods=['GET'])
def get_properties():
    """Получить все объекты недвижимости"""
    properties = Property.query.all()
    return jsonify([{
        'id': p.id,
        'title': p.title,
        'description': p.description,
        'price': p.price,
        'address': p.address,
        'property_type': p.property_type,
        'rooms': p.rooms,
        'area': p.area,
        'floor': p.floor,
        'total_floors': p.total_floors,
        'image_url': p.image_url,
        'created_at': p.created_at.isoformat() if p.created_at else None
    } for p in properties])

@api.route('/properties/<int:id>', methods=['GET'])
def get_property(id):
    """Получить один объект"""
    property_item = Property.query.get_or_404(id)
    return jsonify({
        'id': property_item.id,
        'title': property_item.title,
        'description': property_item.description,
        'price': property_item.price,
        'address': property_item.address,
        'property_type': property_item.property_type,
        'rooms': property_item.rooms,
        'area': property_item.area,
        'floor': property_item.floor,
        'total_floors': property_item.total_floors,
        'image_url': property_item.image_url,
        'created_at': property_item.created_at.isoformat() if property_item.created_at else None
    })

@api.route('/properties', methods=['POST'])
def create_property():
    """Создать новый объект (для Bitrix)"""
    data = request.get_json()
    
    property_item = Property(
        title=data['title'],
        description=data.get('description', ''),
        price=float(data['price']),
        address=data.get('address', ''),
        property_type=data.get('property_type', 'Apartment'),
        rooms=data.get('rooms'),
        area=data.get('area'),
        floor=data.get('floor'),
        total_floors=data.get('total_floors'),
        image_url=data.get('image_url')
    )
    
    db.session.add(property_item)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'id': property_item.id,
        'message': 'Property created successfully'
    }), 201

@api.route('/properties/<int:id>', methods=['PUT'])
def update_property(id):
    """Обновить объект"""
    property_item = Property.query.get_or_404(id)
    data = request.get_json()
    
    if 'title' in data:
        property_item.title = data['title']
    if 'description' in data:
        property_item.description = data['description']
    if 'price' in data:
        property_item.price = float(data['price'])
    if 'address' in data:
        property_item.address = data['address']
    if 'property_type' in data:
        property_item.property_type = data['property_type']
    if 'rooms' in data:
        property_item.rooms = data['rooms']
    if 'area' in data:
        property_item.area = data['area']
    if 'floor' in data:
        property_item.floor = data['floor']
    if 'total_floors' in data:
        property_item.total_floors = data['total_floors']
    if 'image_url' in data:
        property_item.image_url = data['image_url']
    
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'Property updated successfully'
    })

@api.route('/properties/<int:id>', methods=['DELETE'])
def delete_property(id):
    """Удалить объект"""
    property_item = Property.query.get_or_404(id)
    db.session.delete(property_item)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'Property deleted successfully'
    })

@api.route('/health', methods=['GET'])
def health():
    """Проверка работоспособности API"""
    return jsonify({
        'status': 'ok',
        'properties_count': Property.query.count()
    })
