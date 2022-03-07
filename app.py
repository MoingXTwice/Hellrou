from flask import Flask, render_template
from pymongo import MongoClient
from dotenv import load_dotenv

import os
import certifi

app = Flask(__name__)

# 환경변수 값 불러오기
load_dotenv()

# DB Configure
mongo_host = os.getenv('MONGODB_HOST')
client = MongoClient(mongo_host, tlsCAFile=certifi.where())
db = client.hellrou



@app.route('/')
def home():
    all_post = list(db.post.find({}, {'_id': False}))
    return render_template('main.html')

if __name__ == '__main__':
   app.run('0.0.0.0', port=5000, debug=True)