from flask import Flask, render_template, jsonify, request, g
from pymongo import MongoClient
from dotenv import load_dotenv

import os
import certifi
import hashlib
import jwt

from health import health_bp
from mypage import mypage_bp
from signuplogin import user_bp

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True

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

@app.before_request #로그인 여부 및 쿠키내 아이디 추출 전역함수
def authenticate():
    token_receive = request.cookies.get('mytoken') #로그인으로 설정된 쿠키값 저장
    if token_receive:
        payload = jwt.decode(token_receive, app.secret_key, algorithms=["HS256"]) #쿠키값 복호화
        g.user_id = payload['id']
        g.auth = True
    else:
        g.auth = False

@app.route('/')
def home():
    type = request.args.get('type')
    # cate = request.args.get('cate')
    txt = request.args.get('txt')

    # 2022 03 08 21:57 sort likes 순으로 내림차순 추가
    if type == 'title':  # title 검색시 like 조건문
        post_list = list(db.post.find({'$and': [{'title': {'$regex': txt}}, {'status': True}]}, {'_id': False}).sort('likes', -1))
    elif type == 'poster_id':  # 작성자 검색시 equal 조건문
        post_list = list(db.post.find({'$and': [{'poster_id': txt}, {'status': True}]}, {'_id': False}).sort('likes', -1))
    else:
        post_list = list(db.post.find({'status': True}, {'_id': False}).sort('likes', -1).limit(12))

    return render_template('view.html', post_list = post_list)
#   return render_template('view.html', post_list = post_list, isLogin=g.auth)

@app.route('/view_list', methods=['GET'])
def view_list():
    offset = int(request.args.get('offset'))
    limit = int(request.args.get('limit'))
    post_list = list(db.post.find({'status':True},{'_id': False}).sort('likes', -1).skip(offset).limit(limit))
    return jsonify({"post_list" : post_list})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)