from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient
import time
import json
from bson import ObjectId
from pytz import timezone
from datetime import datetime

app = Flask(__name__)

client = MongoClient('mongodb://test:test@15.165.29.169', 27017)  # mongoDB는 27017 포트로 돌아갑니다#localhost .mongodb://test:test@15.165.29.169
db = client.helimee  # 'dbsparta'라는 이름의 db를 만듭니다.

## HTML을 주는 부분
@app.route('/')
def home():
    return render_template('page.html')

@app.route('/admin')
def admin():


    return render_template('page.html')

@app.route('/page_input')
def page_input():
    return render_template('page_input.html')

@app.route('/about_page')
def about_page():
    return render_template('about_page.html')

## 인원수 입력하는 부분
@app.route('/peopleinput', methods=['POST'])
def test_post():
    people = request.form['people_give']
    manager_name = request.form['manager_name']
    manager_password = request.form['manager_password']
    max_number = request.form['max_number']
    user_info = list(db.user.find({'name':manager_name}))
    if max_number != '-1':
        db.abfitness.update_one({'max_number_find':'find'},{'$set':{'max_number':max_number}})
    if len(user_info) == 0:
        msg = "이름을 확인해주세요"
    elif user_info[-1]['password'] == manager_password:
        now =  datetime.now(timezone('Asia/Seoul'))  #time.localtime()
        date = now.strftime("%Y/%m/%d")
        # now1 = "%04d/%02d/%02d %02d:%02d" % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min)
        now1 = now.strftime('%Y/%m/%d %H:%M')
        # date = "%04d/%02d/%02d" % (now.tm_year, now.tm_mon, now.tm_mday)
        data = {'date': date,'people': people, 'time':now1}
        db.abfitness.insert_one(data)
        msg = "현재 인원이 업데이트 되었습니다."
    else:
        msg = "비밀번호가 일치하지 않습니다."

    return jsonify({'result': 'success', 'msg': msg})

# 공지글 수정
@app.route('/noticeinput', methods=['POST'])
def notice_post():
    manager_name = request.form['manager_name']
    manager_password = request.form['manager_password']
    user_info = list(db.user.find({'name': manager_name}))
    if len(user_info) == 0:
        msg = "이름을 확인해주세요"
    elif user_info[-1]['password'] == manager_password:
        notice_head1 = request.form['notice_head1']
        notice_content1 = request.form['notice_content1']
        notice_head2 = request.form['notice_head2']
        notice_content2 = request.form['notice_content2']
        notice_head3 = request.form['notice_head3']
        notice_content3 = request.form['notice_content3']
        notice_head4 = request.form['notice_head4']
        notice_content4 = request.form['notice_content4']
        notice_head5 = request.form['notice_head5']
        notice_content5 = request.form['notice_content5']
        db.abfitness.update_one({'notice': 'notice'},
                                {'$set': {'notice_head1': notice_head1, 'notice_content1': notice_content1,
                                          'notice_head2': notice_head2, 'notice_content2': notice_content2,
                                          'notice_head3': notice_head3, 'notice_content3': notice_content3,
                                          'notice_head4': notice_head4, 'notice_content4': notice_content4,
                                          'notice_head5': notice_head5, 'notice_content5': notice_content5,}})
        msg = '수정되었습니다.'
    else:
        msg = "비밀번호가 일치하지 않습니다."
    return jsonify({'result': 'success', 'msg': msg})

@app.route('/peopleget', methods=['GET'])
def get():
    now =  datetime.now(timezone('Asia/Seoul'))
    # date = "%04d/%02d/%02d" % (now.tm_year, now.tm_mon, now.tm_mday)
    date = now.strftime("%Y/%m/%d")
    people_list = list(db.abfitness.find({'date':date}))
    max_list = list(db.abfitness.find({'max_number_find': 'find'}))
    people_data = people_list[-1]
    max_number = max_list[-1]
    notice = list(db.abfitness.find({'notice':"notice"}))[-1]
    del notice['_id']
    print(people_data['people'],people_data['time'],max_number['max_number'])
    return jsonify({'result': 'success', 'current_people': people_data['people'],'current_time': people_data['time'],'max_number':max_number['max_number'], 'notice':notice})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
