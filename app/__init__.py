import logging
from logging.handlers import RotatingFileHandler
from flask import Flask
from flask_wtf import CSRFProtect

app = Flask(__name__)
app.config["SECRET_KEY"] = "change_this_secret_in_prod"

csrf = CSRFProtect(app)

file_handler = RotatingFileHandler("logs/app.log", maxBytes=512000, backupCount=2, encoding="utf-8")
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s"))
app.logger.addHandler(file_handler)
app.logger.setLevel(logging.INFO)
app.logger.info("App startup")

from app import routes 
