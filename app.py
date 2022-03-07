from flask import Flask
from pymongo import MongoClient
from dotenv import load_dotenv

import os
import certifi

from health import health_bp

app = Flask(__name__)
# app.config["TEMPLATES_AUTO_RELOAD"] = True

# 환경변수 값 불러오기
load_dotenv()

# DB Configure
mongo_host = os.getenv('MONGODB_HOST')
client = MongoClient(mongo_host, tlsCAFile=certifi.where())
db = client.hellrou

app.register_blueprint(health_bp, url_prefix='/health')

if __name__ == '__main__':
   app.run('0.0.0.0', port=5000, debug=True)