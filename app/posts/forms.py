from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SubmitField, SelectField, DateTimeLocalField
from wtforms.validators import DataRequired, Length
from .models import CategoryEnum

class PostForm(FlaskForm):
    title=StringField('Title', validators=[DataRequired(), Length(max=150)])
    content=TextAreaField('Content', validators=[DataRequired()])
    enabled=BooleanField('Active', default=True)
    publish_date=DateTimeLocalField('Publish date', format='%Y-%m-%dT%H:%M', default=datetime.utcnow)
    category=SelectField('Category', choices=[
        (CategoryEnum.NEWS.value,"News"),
        (CategoryEnum.PUBLICATION.value,"Publication"),
        (CategoryEnum.TECH.value,"Tech"),
        (CategoryEnum.OTHER.value,"Other"),
    ])
    submit=SubmitField('Save')
