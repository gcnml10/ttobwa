from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient
import time
import json
from bson import ObjectId

app = Flask(__name__)

client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.helimee  # 'dbsparta'라는 이름의 db를 만듭니다.

## HTML을 주는 부분
@app.route('/')
def home():
    return render_template('page.html')

@app.route('/page_input')
def page_input():
    return render_template('page_input.html')

## 인원수 입력하는 부분
@app.route('/peopleinput', methods=['POST'])
def test_post():
    people = request.form['people_give']
    now = time.localtime()
    now1 = "%04d/%02d/%02d %02d:%02d" % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min)
    date = "%04d/%02d/%02d" % (now.tm_year, now.tm_mon, now.tm_mday)
    data = {'date': date,'people': people, 'time':now1}
    db.abfitness.insert_one(data)
    msg = "현재 인원이 업데이트 되었습니다."

    return jsonify({'result': 'success', 'msg': msg})

@app.route('/peopleget', methods=['GET'])
def get():
    now = time.localtime()
    date = "%04d/%02d/%02d" % (now.tm_year, now.tm_mon, now.tm_mday)
    people_list = list(db.abfitness.find({'date':date}))
    print(people_list)
    people_data = people_list[-1]
    return jsonify({'result': 'success', 'current_people': people_data['people'],'current_time': people_data['time']})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
