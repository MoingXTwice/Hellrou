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
    user_id = 'test'
    post_list = list(db.post.find({'poster_id' : user_id}, {'_id' : False}))
    user_info = db.user.find_one({'user_id' : user_id}, {'_id' : False})
    like_id = user_info['like_id']

    if isinstance(like_id, list):
        like_list = list(db.post.find({'post_id' : {'$in' : like_id}}, {'_id' : False}))
    else:
        like_list = list(db.post.find({'post_id': int(like_id)}, {'_id': False}))

    return render_template('mypage.html', post_list = post_list, like_list = like_list, user_info=user_info)

@mypage_bp.route('/del_post', methods=['GET'])
def del_post():
    post_id = request.args.get('post_id')
    db.post.delete_one({'post_id' : int(post_id)})
    return jsonify({'msg' : '등록한 운동이 삭제되었습니다'})

@mypage_bp.route('/del_like', methods=['GET'])
def del_like():
    post_id = request.args.get('post_id')
    user_id = request.args.get('user_id')

    db.user.update_one({'user_id' : user_id}, {'$pull':{'like_id' : int(post_id)}})

    return jsonify({'msg' : '스크랩한운동이 삭제되었습니다'})