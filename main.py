from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, Property
from api import api
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///estate.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
app.register_blueprint(api)

# Разрешить отображение в iframe (для Bitrix24)
@app.after_request
def add_header(response):
    # Разрешить отображение в iframe
    response.headers['X-Frame-Options'] = 'ALLOWALL'
    # Или можно указать конкретный домен Bitrix:
    # response.headers['Content-Security-Policy'] = "frame-ancestors 'self' https://ваш-домен.bitrix24.ru"
    
    # CORS заголовки
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response

@app.route('/')
def index():
    """Главная страница со списком объектов"""
    properties = Property.query.order_by(Property.created_at.desc()).all()
    return render_template('index.html', properties=properties)

@app.route('/property/<int:id>')
def property_detail(id):
    """Детальная страница объекта"""
    property_item = Property.query.get_or_404(id)
    return render_template('property_detail.html', property=property_item)

@app.route('/add', methods=['GET', 'POST'])
def add_property():
    """Форма добавления нового объекта"""
    if request.method == 'POST':
        property_item = Property(
            title=request.form['title'],
            description=request.form['description'],
            price=float(request.form['price']),
            address=request.form['address'],
            property_type=request.form['property_type'],
            rooms=int(request.form['rooms']) if request.form['rooms'] else None,
            area=float(request.form['area']) if request.form['area'] else None,
            floor=int(request.form['floor']) if request.form['floor'] else None,
            total_floors=int(request.form['total_floors']) if request.form['total_floors'] else None,
            image_url=request.form['image_url']
        )
        db.session.add(property_item)
        db.session.commit()
        flash('Объект успешно добавлен!', 'success')
        return redirect(url_for('index'))
    
    return render_template('add_property.html')

@app.route('/search')
def search():
    """Поиск объектов"""
    query = request.args.get('q', '')
    property_type = request.args.get('type', '')
    min_price = request.args.get('min_price', type=float)
    max_price = request.args.get('max_price', type=float)
    
    properties = Property.query
    
    if query:
        properties = properties.filter(
            (Property.title.contains(query)) | 
            (Property.address.contains(query)) |
            (Property.description.contains(query))
        )
    
    if property_type:
        properties = properties.filter(Property.property_type == property_type)
    
    if min_price:
        properties = properties.filter(Property.price >= min_price)
    
    if max_price:
        properties = properties.filter(Property.price <= max_price)
    
    properties = properties.order_by(Property.created_at.desc()).all()
    return render_template('index.html', properties=properties, search_query=query)

def init_db():
    """Инициализация базы данных с тестовыми данными"""
    with app.app_context():
        db.create_all()
        
        # Проверяем, есть ли уже данные
        if Property.query.count() == 0:
            # Добавляем тестовые объекты
            test_properties = [
                Property(
                    title='Modern Downtown Apartment',
                    description='Spacious 3-bedroom apartment with modern renovation in the city center. Close to metro, parks, and schools.',
                    price=325000,
                    address='New York, 5th Avenue, 123',
                    property_type='Apartment',
                    rooms=3,
                    area=85.5,
                    floor=7,
                    total_floors=16,
                    image_url='https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?w=800'
                ),
                Property(
                    title='Suburban Villa with Land',
                    description='Cozy 200 sqm house on 1500 sqm land. Gated community, security, all utilities included.',
                    price=780000,
                    address='Los Angeles, Beverly Hills, Oak Street 45',
                    property_type='House',
                    rooms=5,
                    area=200,
                    floor=2,
                    total_floors=2,
                    image_url='https://images.unsplash.com/photo-1568605114967-8130f3a36994?w=800'
                ),
                Property(
                    title='Studio Near Subway',
                    description='Compact 28 sqm studio with excellent renovation. Perfect for young couple or student.',
                    price=145000,
                    address='Chicago, Michigan Avenue, 789',
                    property_type='Apartment',
                    rooms=1,
                    area=28,
                    floor=3,
                    total_floors=9,
                    image_url='https://images.unsplash.com/photo-1502672260066-6bc05365a9be?w=800'
                ),
                Property(
                    title='Office Space Downtown',
                    description='Modern office in Class A business center. Panoramic windows, AC, parking included.',
                    price=520000,
                    address='San Francisco, Market Street, 234',
                    property_type='Commercial',
                    rooms=None,
                    area=120,
                    floor=15,
                    total_floors=35,
                    image_url='https://images.unsplash.com/photo-1497366216548-37526070297c?w=800'
                ),
                Property(
                    title='Two Bedroom Near Park',
                    description='Bright apartment near Central Park. Quiet courtyard, playground available.',
                    price=285000,
                    address='New York, Central Park West, 567',
                    property_type='Apartment',
                    rooms=2,
                    area=56,
                    floor=5,
                    total_floors=12,
                    image_url='https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?w=800'
                ),
            ]
            
            for prop in test_properties:
                db.session.add(prop)
            
            db.session.commit()
            print("✅ База данных создана и заполнена тестовыми данными!")

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5001)
