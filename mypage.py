from flask import Flask, Blueprint, render_template, jsonify, request, redirect, url_for, g
from pymongo import MongoClient
from dotenv import load_dotenv

import os
import certifi
import jwt

app = Flask(__name__)

# 환경변수 값 불러오기
load_dotenv()
secret_key = os.getenv('SECRET_KEY')

# DB Configure
mongo_host = os.getenv('MONGODB_HOST')
client = MongoClient(mongo_host, tlsCAFile=certifi.where())
db = client.hellrou

#Blueprint
mypage_bp = Blueprint('mypage', __name__)

@mypage_bp.route('/') #마이페이지의 ListPage
def mypage():
    try: #로그인 쿠키내의 user_id값과 로그인상태값 변수선언
        user_id = g.user_id
        auth = g.auth
    except: #로그인되어있지 않으면 로그인페이지로 강제이동
        return redirect(url_for('user.login'))

    #검색시 파라미터값 변수저장
    type = request.args.get('type')
    # cate = request.args.get('cate')
    txt = request.args.get('txt')

    #검색결과적용하여 post 컬렉션에서 로그인된 ID가 작성한 운동 리스트 추출
    if type == 'title':
        post_list = list(db.post.find({'$and': [{'title': {'$regex': txt}}, {'poster_id': user_id}]}, {'_id': False}))
    else:
        post_list = list(db.post.find({'poster_id' : user_id}, {'_id' : False}))

    #로그인된 ID에 해당하는 유저의 데이터 추출
    user_info = db.user.find_one({'user_id' : user_id}, {'_id' : False})
    like_id = user_info['like_id'] #스크랩한 운동리스트 ID값 변수저장

    if like_id: #like_id가 존재하는 경우
        if isinstance(like_id, list): #like_id가 리스트 형식인지 확인
            like_list = list(db.post.find({'post_id': {'$in': like_id}}, {'_id': False})) #post_id가 like_id에 해당되는지 확인 후 추출
        else:  #리스트가 아니면 스크랩한 id값에 해당하는 운동데이터 추출
            like_list = list(db.post.find({'post_id': like_id}, {'_id': False}))
    else: #스크랩한 내역이 없는 경우 제외하고 데이터 전송
        return render_template('mypage.html', post_list = post_list, user_info=user_info, isLogin = auth)

    return render_template('mypage.html', post_list = post_list, like_list = like_list, user_info=user_info, isLogin = auth)

@mypage_bp.route('/del_post', methods=['GET']) #내가 등록한 운동의 삭제
def del_post():
    post_id = request.args.get('post_id')
    db.post.delete_one({'post_id' : post_id})
    return jsonify({'msg' : '등록한 운동이 삭제되었습니다'})

@mypage_bp.route('/del_like', methods=['GET']) #내가 스크랩한 운동의 삭제
def del_like():
    post_id = request.args.get('post_id')
    user_id = request.args.get('user_id')

    db.user.update_one({'user_id' : user_id}, {'$pull':{'like_id' : post_id}}) #배열에서 해당 ID 삭제 후 업데이트
    db.post.update_one({'post_id' : post_id}, {'$inc' : {'likes' : -1}})

    return jsonify({'msg' : '스크랩한운동이 삭제되었습니다'})