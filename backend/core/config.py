import os
from dotenv import load_dotenv
from datetime import timedelta

load_dotenv()



class Config(object):
		DEBUG = False
		TESTING = False
		DATABASE_URI = 'sqlite:///:memory:'


class ProductionConfig(Config):

	DB_URL = os.environ.get('DATABASE_URL') or 'mysql+pymysql://root:@127.0.0.1:3306/whats_app'
	BASE_URL     = 'http://127.0.0.1:5000'
	UPLOAD_FOLDER = '/static/uploads'
	PERMANENT_SESSION_LIFETIME = timedelta(minutes=120)
	SESSION_TYPE = 'filesystem'    
	SESSION_COOKIE_DOMAIN = ''
class DevelopmentConfig(Config):
		DEBUG = True


class SECRET_KEY(Config):
	SECRET_KEY = '90c41266fb96f9ffaaedf19ada8ef9412b871984baf345910ca5feaa4182fefc'
