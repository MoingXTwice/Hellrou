from flask import Blueprint, render_template, jsonify, request, redirect, flash, g
from pymongo import MongoClient
from datetime import datetime, timedelta
import pytz
from dotenv import load_dotenv
import jwt
import uuid

import os
import certifi

load_dotenv()

mongo_host = os.getenv('MONGODB_HOST')
client = MongoClient(mongo_host, tlsCAFile=certifi.where())
db = client.hellrou

SECRET_KEY = os.getenv('SECRET_KEY')

health_bp = Blueprint('health', __name__)

#한국 시간 설정
KST = pytz.timezone('Asia/Seoul')

# 모든 회원의 상세 보기 페이지
# 이 페이지의 역할 - 1.나의 루틴 클릭시 나의 sel_id 가져오기
#                2.공유된 것 클릭시 post_id 가져오기
@health_bp.route('', methods=['GET'])
def detail_view():
    token_receive = request.cookies.get('mytoken')
    try:
        post_id = request.args.get('post_id')
        # 나의 헬루
        if post_id is None:
            user_id = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])['id']
            user_info = db.user.find_one({'user_id': user_id})
            user_sel = user_info['sel_id']
            find_post = db.post.find_one({'post_id': user_sel})

            if user_sel in user_info['like_id']: #선택한 헬루가 스크랩되었는지 체크
                like_status = True
            else:
                like_status = False

            sel_status = True

            return render_template('health.html', health=find_post, user_sel=user_sel, like_status = like_status, sel_status = sel_status)
        # 공유된 헬루(내가 쓴 헬루 포함)
        #TODO 필요한 것 선택ID(user.sel_id),스크랩상태(user.like_id) , 공유상태(post.status)
        else:
            find_post = db.post.find_one({'post_id': post_id}) #post_id에 해당되는 post데이터 가져오기
            user_info = db.user.find_one({'user_id' : g.user_id})
            like_id = user_info['like_id'] #로그인한 user_id의 like_id 가져오기

            if post_id in like_id: #선택한 헬루가 스크랩되었는지 체크
                like_status = True
            else:
                like_status = False

            if post_id == user_info['sel_id']:
                sel_status = True
            else:
                sel_status = False


            return render_template('health.html', health=find_post, like_status = like_status, user_id=g.user_id, sel_status = sel_status)
    except(jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        flash('로그인 후 이용 가능합니다.')
        return redirect('/user/login')


# # 나의 헬루 페이지
# @health_bp.route('/<user_id>', methods=['GET'])
# def my_health(user_id):
#     user_sel = db.user.find_one({'user_id': 'kimbs'})['sel_id']
#     find_post = db.post.find_one({'post_id': int(user_sel)})
#     return render_template('health.html', health=find_post, user_sel=user_sel)

# 헬루 등록 페이지
@health_bp.route('/post')
def post():
    token_receive = request.cookies.get('mytoken')

    return render_template('post.html')

# 헬루 등록 api
@health_bp.route('/post', methods=['POST'])
def post_api():
    token_receive = request.cookies.get('mytoken')

    try:
        # poster_id 값 가져오기
        user_id = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])['id']

        title = request.form['title']
        desc = request.form['desc']
        process = request.form['process']
        day1 = request.form['day1']
        day2 = request.form['day2']
        day3 = request.form['day3']
        day4 = request.form['day4']
        day5 = request.form['day5']
        day6 = request.form['day6']
        day7 = request.form['day7']
        write_time = datetime.now(KST).strftime('%Y-%m-%d %H:%M:%S')

        doc = {
            'post_id': uuid.uuid4().hex,
            'poster_id': user_id,
            'title': title,
            'desc': desc,
            'process': process,
            'day1': day1,
            'day2': day2,
            'day3': day3,
            'day4': day4,
            'day5': day5,
            'day6': day6,
            'day7': day7,
            'status': False,
            'datetime': write_time,
            'likes': 0
        }
        db.post.insert_one(doc)

        return jsonify({'result': 'success', 'msg': '헬루 등록이 완료되었습니다.'})
    except(jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect('/user/login')

#TODO 공유기능을 같이 묶을 수 있지 않을까?
#일단 기능 구현 먼저 해두고 리팩토링 -> status 값을 가져와야 하나?
# 공유 기능
@health_bp.route('/share', methods=['POST'])
def share():
    token_receive = request.cookies.get('mytoken')
    try:
        user_id = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])['id']
        post_id = request.form['post_id']
        db.post.update_one({'post_id': post_id}, {'$set': {'status': True}})
        return jsonify({'result': 'success'})
    except(jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect('/user/login')

# 공유 취소 기능
@health_bp.route('/share_cancel', methods=['POST'])
def share_cancel():
    token_receive = request.cookies.get('mytoken')
    try:
        user_id = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])['id']
        post_id = request.form['post_id']
        db.post.update_one({'post_id': post_id}, {'$set': {'status': False}})
        return jsonify({'result': 'success'})
    except(jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect('/user/login')

# 스크랩 기능
@health_bp.route('/scrap', methods=['POST'])
def scrap():
    try:
        user_id = g.user_id
        post_id = request.form['post_id']

        post_data = db.post.find_one({'post_id' : post_id}, {'_id' : False})
        if user_id == post_data['poster_id']:
            return jsonify({'msg' : '본인의 헬루는 스크랩할 수 없습니다'})
        else:
            db.user.update_one({'user_id': user_id}, {'$push': {'like_id': post_id}})
            db.post.update_one({'post_id' : post_id}, {'$inc' : {'likes' : 1}})
            return jsonify({'result': 'success'})
    except(jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect('/user/login')


# 선택 기능
@health_bp.route('/select', methods=['POST'])
def select():
    try:
        user_id = g.user_id
        post_id = request.form['post_id']
        db.user.update_one({'user_id': user_id}, {'$set': {'sel_id': post_id}})
        return jsonify({'msg': '선택되었습니다'})
    except(jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect('/user/login')