from flask import Blueprint, render_template, jsonify, request, redirect
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
            print(user_id)
            user_sel = db.user.find_one({'user_id': user_id})['sel_id']
            print(user_sel)
            find_post = db.post.find_one({'post_id': user_sel})
            print(find_post)
            return render_template('health.html', health=find_post, user_sel=user_sel)
        # 공유된 헬루(내가 쓴 헬루 포함)
        #TODO 필요한 것 선택ID(user.sel_id),스크랩상태(user.like_id) , 공유상태(post.status)
        else:
            find_post = db.post.find_one({'post_id': int(post_id)})
            return render_template('health.html', health=find_post)
    except(jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect('/user/login')


# # 나의 헬루 페이지
# #TODO JWT가 완성이 되면 "나의 헬루"를 클릭하면 user_id를 받아와서 path variable로 넘겨야함?
# @health_bp.route('/<user_id>', methods=['GET'])
# def my_health(user_id):
#     user_sel = db.user.find_one({'user_id': 'kimbs'})['sel_id']
#     find_post = db.post.find_one({'post_id': int(user_sel)})
#     return render_template('health.html', health=find_post, user_sel=user_sel)

# 헬루 등록 페이지
@health_bp.route('/post')
def post():
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

# 공유 기능
@health_bp.route('/share', methods=['POST'])
def share():

    return jsonify({'result': 'success'})

# @app.route("/bucket/done", methods=["POST"])
# def bucket_done():
#     id_receive = request.form['id_give']
#     db.bucket.update_one({'id':int(id_receive)},{'$set':{'done':1}})
#     return jsonify({'msg': 'POST(완료) 연결 완료!'})
