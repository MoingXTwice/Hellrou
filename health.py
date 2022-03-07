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

KST = pytz.timezone('Asia/Seoul')

@health_bp.route('')
def view():
    return 'view'

# 헬루 등록 페이지
@health_bp.route('/post')
def post():
    return render_template('post.html')

@health_bp.route('/post', methods=['POST'])
def post_api():

    # 글 번호 1씩 증가
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
    # %Y가 이상하게 출력됨
    write_time = datetime.now(KST).strftime('%Y-%m-%D %H:%M:%S')
    print(write_time)

    doc = {
        'post_id': post_id,
        'poster_id': 'test',
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

    return jsonify({'result': 'success'})
