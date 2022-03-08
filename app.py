from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient
from dotenv import load_dotenv

import os
import certifi

from health import health_bp
from mypage import mypage_bp

app = Flask(__name__)
# app.config["TEMPLATES_AUTO_RELOAD"] = True

# 환경변수 값 불러오기
load_dotenv()

# DB Configure
mongo_host = os.getenv('MONGODB_HOST')
client = MongoClient(mongo_host, tlsCAFile=certifi.where())

db = client.hellrou


#Blueprint 선언
app.register_blueprint(health_bp, url_prefix='/health')
app.register_blueprint(mypage_bp, url_prefix='/mypage')

@app.route('/')
def home():
    return render_template('main.html')

@app.route('/all_list', methods=['GET'])
def all_list():
    #all_post = list(db.post.find({ 'status': True }, {'_id': False}).sort({"datetime": -1 }))
    all_post = list(db.post.find({},{'_id':False}))

    return jsonify({"all_post" : all_post})


if __name__ == '__main__':
   app.run('0.0.0.0', port=5000, debug=True)