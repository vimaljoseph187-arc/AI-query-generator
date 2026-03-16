from flask import Flask, render_template, request
from flask_session import Session
import os

app = Flask(__name__)

# Set secret key properly
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY') 
# app.config('app.config.ProductionConfig')
app.config.from_object('core.config.ProductionConfig')

current_app = app

from core.controller.BOController import app as BO
app.register_blueprint(BO, url_prefix='')