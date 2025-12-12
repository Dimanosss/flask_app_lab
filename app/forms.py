from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField, BooleanField, SubmitField, EmailField
from wtforms.validators import DataRequired, Email, Length

class ContactForm(FlaskForm):
    name = StringField("Ім'я", validators=[DataRequired(message="Вкажіть ім'я"), Length(min=2, max=50)])
    email = EmailField("Email", validators=[DataRequired(message="Вкажіть email"), Email(message="Некоректний email")])
    message = TextAreaField("Повідомлення", validators=[DataRequired(message="Вкажіть повідомлення"), Length(min=5, max=2000)])
    submit = SubmitField("Надіслати")

class LoginForm(FlaskForm):
    username = StringField("Username або Email", validators=[DataRequired(message="Вкажіть username або email")])
    password = PasswordField("Пароль", validators=[DataRequired(), Length(min=4, max=10, message="Довжина 4–10 символів")])
    remember = BooleanField("Запам'ятати мене")
    submit = SubmitField("Увійти")
