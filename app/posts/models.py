from datetime import datetime
from enum import Enum as PyEnum
from app import db
from sqlalchemy import Enum

class CategoryEnum(PyEnum):
    NEWS="news"
    PUBLICATION="publication"
    TECH="tech"
    OTHER="other"

class Post(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    title=db.Column(db.String(150), nullable=False)
    content=db.Column(db.Text, nullable=False)
    posted=db.Column(db.DateTime, default=datetime.utcnow)
    category=db.Column(Enum(CategoryEnum), nullable=False, default=CategoryEnum.NEWS)
    is_active=db.Column(db.Boolean, default=True)
    author=db.Column(db.String(20), default="Anonymous")
