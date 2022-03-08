from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient
from dotenv import load_dotenv

import os
import certifi
import hashlib

from health import health_bp
from mypage import mypage_bp
from signuplogin import user_bp

app = Flask(__name__)
#app.config["TEMPLATES_AUTO_RELOAD"] = True

# 환경변수 값 불러오기
load_dotenv()
app.secret_key = os.getenv('SECRET_KEY')

# DB Configure
mongo_host = os.getenv('MONGODB_HOST')
client = MongoClient(mongo_host, tlsCAFile=certifi.where())

db = client.hellrou


#Blueprint 선언
app.register_blueprint(health_bp, url_prefix='/health')
app.register_blueprint(mypage_bp, url_prefix='/mypage')
app.register_blueprint(user_bp, url_prefix='/user')

@app.route('/')
def home():
    user_id = request.cookies.get('mytoken')
    if user_id :
        isLogin = True
    else :
        isLogin = False
    print(isLogin)
    return render_template('main.html', isLogin=isLogin)

@app.route('/view_list', methods=['GET'])
def view_list():
    type = request.args.get('type')
    #cate = request.args.get('cate')
    txt = request.args.get('txt')

    if type=='title' : #title 검색시 like 조건문
        post_list = list(db.post.find({'title' : {'$regex': txt}}, {'_id': False}))
    elif type=='poster_id' : #작성자 검색시 equal 조건문
        post_list = list(db.post.find({'poster_id': txt}, {'_id': False}))
    else :
        post_list = list(db.post.find({},{'_id': False}))

    return jsonify({"post_list" : post_list})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)