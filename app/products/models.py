from datetime import datetime
from sqlalchemy import ForeignKey, Boolean, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app import db

class Category(db.Model):
    __tablename__ = 'category'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(100), nullable=False)
    
    # Зв'язок 1:N з Product
    products: Mapped[list['Product']] = relationship('Product', back_populates='category', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Category {self.name}>'

class Product(db.Model):
    __tablename__ = 'product'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(200), nullable=False)
    price: Mapped[float] = mapped_column(db.Float, nullable=False)
    active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
    
    # Зовнішній ключ для зв'язку з Category
    category_id: Mapped[int] = mapped_column(ForeignKey('category.id'), nullable=True)
    
    # Зв'язок N:1 з Category
    category: Mapped['Category'] = relationship('Category', back_populates='products')
    
    def __repr__(self):
        return f'<Product {self.name} - {self.price}>'

