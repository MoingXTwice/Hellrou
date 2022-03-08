from flask import Blueprint, render_template, jsonify, request
from pymongo import MongoClient
from datetime import datetime, timedelta
import pytz
from dotenv import load_dotenv

import os
import certifi

load_dotenv()

mongo_host = os.getenv('MONGODB_HOST')
client = MongoClient(mongo_host, tlsCAFile=certifi.where())
db = client.hellrou

health_bp = Blueprint('health', __name__)

#한국 시간 설정
KST = pytz.timezone('Asia/Seoul')

# 모든 회원의 상세 보기 페이지
@health_bp.route('', methods=['GET'])
def detail_view():
    post_id = request.args.get('post_id')
    find_post = db.post.find_one({'post_id': int(post_id)})
    print(find_post)
    return render_template('detail_view.html', health=find_post)

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

    #TODO 이 방법은 글 삭제가 되면 삭제된 번호에 글이 다시 들어갈 수 있음
    # auto increment 를 찾아보고 안되면 uuid로 대체
    posts = list(db.post.find({}, {'_id': False}))
    post_id = len(posts) + 1


    #TODO poster_id 값 가져오기

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
        'post_id': post_id,
        'poster_id': 'kimbs',
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

@health_bp.route('/share', methods=['POST'])
def share():

    return jsonify({'result': 'success'})

# @app.route("/bucket/done", methods=["POST"])
# def bucket_done():
#     id_receive = request.form['id_give']
#     db.bucket.update_one({'id':int(id_receive)},{'$set':{'done':1}})
#     return jsonify({'msg': 'POST(완료) 연결 완료!'})
