from flask import Flask, Blueprint, render_template, jsonify, request
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

#Blueprint
mypage_bp = Blueprint('mypage', __name__)

@mypage_bp.route('/')
def mypage():
    return render_template('mypage.html')

@mypage_bp.route('/list', methods=['GET'])
def mypage_list():
    user_id = request.args.get('user_id')
    mypage_list = list(db.post.find({'poster_id' : user_id},{'_id' : False}))

    return jsonify({"mypage_list" : mypage_list})

@mypage_bp.route('/like_list', methods=['GET'])
def like_list():
    user_id = request.args.get('user_id')
    user_info = db.user.find_one({'user_id':user_id}, {'_id' : False})
    like_id = user_info['like_id']

    if isinstance(like_id, list):
        like_list = list(db.post.find({'post_id': {'$in': like_id}}, {'_id': False}))
    else:
        like_list = list(db.post.find({'post_id': int(like_id)}, {'_id': False}))

    return jsonify({"like_list" : like_list})