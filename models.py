from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Property(db.Model):
    """Модель объекта недвижимости"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    address = db.Column(db.String(300), nullable=False)
    property_type = db.Column(db.String(50), nullable=False)  # Квартира, Дом, Коммерческая
    rooms = db.Column(db.Integer)
    area = db.Column(db.Float)  # площадь в м²
    floor = db.Column(db.Integer)
    total_floors = db.Column(db.Integer)
    image_url = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Property {self.title}>'
    
    def format_price(self):
        """Форматирует цену с разделителями"""
        return f"${self.price:,.0f}"
