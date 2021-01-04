from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient
import random
import time
import json
from bson import ObjectId

app = Flask(__name__)

client = MongoClient('mongodb://test:test@3.34.200.148', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.dbsparta  # 'dbsparta'라는 이름의 db를 만듭니다.


## HTML을 주는 부분
@app.route('/')
def home():
    return render_template('page_type1.html')


## 문장입력하는 부분
@app.route('/sentanceinput', methods=['POST'])
def test_post():
    korean_receive = request.form['korean_give']
    eng_receive = request.form['eng_give']
    userID = request.form['userID']
    reference = request.form['reference_give']
    id_receive = request.form['ids']
    print(id_receive)
    print(reference)
    eng_split = eng_receive.split()
    if id_receive == '0':
        memo_reveive = request.form['memo']
        sentance = {'userID': userID, 'writerID': userID, 'korean': korean_receive, 'eng': eng_split,
                    'reference': reference, 'count': 0, 'memo': memo_reveive, 'running': 'Y'}
        db.sentances.insert_one(sentance)
        msg = '새로운 문장이 저장되었습니다.'
    else:
        db.sentances.update_one({'_id': ObjectId(id_receive)},
                                {'$set': {'korean': korean_receive, 'eng': eng_split, 'reference': reference}})
        msg = '수정되었습니다.'
    return jsonify({'result': 'success', 'msg': msg})


@app.route('/sentanceinput_in_entire', methods=['POST'])
def test_post_entire():
    korean_receive = request.form['korean_give']
    eng_receive = request.form['eng_give']
    userID = request.form['userID']
    reference = request.form['reference_give']
    memo = request.form['memo_give']
    id_receive = request.form['id']
    print(id_receive)
    print(reference)
    eng_split = eng_receive.split()
    db.sentances.update_one({'_id': ObjectId(id_receive)},
                            {'$set': {'korean': korean_receive, 'eng': eng_split, 'reference': reference,
                                      'memo': memo}})
    msg = '수정되었습니다.'
    return jsonify({'result': 'success', 'msg': msg})


@app.route('/sentanceget', methods=['POST'])
def send_post():
    userID = request.form['userID']
    sen_list = list(db.sentances.find({'userID': userID}))
    send_sen = random.choice(sen_list)

    # class JSONEncoder(json.JSONEncoder):
    #     def default(self, o):
    #         if isinstance(o, ObjectId):
    #             return str(o)
    #         return json.JSONEncoder.default(self, o)

    # send_sen_encoded = JSONEncoder().encode(send_sen)
    # json.encode(analytics, cls=JSONEncoder)

    send_sen['_id'] = str(send_sen['_id'])

    return jsonify({'result': 'success', 'send_sen': send_sen})


@app.route('/wholesentanceget', methods=['POST'])
def whole_send_post():
    userID = request.form['userID']
    sen_list = list(db.sentances.find({}))
    send_sen = random.choice(sen_list)
    send_sen['_id'] = str(send_sen['_id'])
    return jsonify({'result': 'success', 'send_sen': send_sen})

@app.route('/delete_real', methods=['POST'])
def delete_real():
    ID = request.form['ID']
    db.sentances.delete_one({'_id': ObjectId(ID)})
    msg='삭제되었습니다'
    return jsonify({'result': 'success', 'msg': msg})


@app.route('/except_list', methods=['POST'])
def except_list_post():
    userID = request.form['userID']
    print(userID)
    except_list = list(db.sentances.find({'running': 'N', 'userID': userID}))
    for except_sen in except_list:
        except_sen['_id'] = str(except_sen['_id'])
    return jsonify({'result': 'success', 'list': except_list})


@app.route('/entire_list', methods=['POST'])
def list_post():
    userID = request.form['userID']
    entire_list = list(db.sentances.find({'running': 'Y', 'userID': userID}))
    for entire_sen in entire_list:
        entire_sen['_id'] = str(entire_sen['_id'])
    print(entire_list)
    return jsonify({'result': 'success', 'list': entire_list})


@app.route('/countup', methods=['POST'])
def count_up():
    count_up_ids = request.form['countup_give']
    userID = request.form['userID']
    count_up_sen = db.sentances.find_one({'userID': userID, '_id': ObjectId(count_up_ids)})
    print(count_up_sen)
    new_count = count_up_sen['count'] + 1
    db.sentances.update_one({'userID': userID, '_id': ObjectId(count_up_ids)}, {'$set': {'count': new_count}})
    msg = '횟수 추가!'
    return jsonify({'result': 'success', 'msg': msg, 'new_count': new_count})


@app.route('/countreset', methods=['POST'])
def count_reset():
    userID = request.form['userID']
    count_reset_ids = request.form['countreset_give']
    count_reset_sen = db.sentances.find_one({'userID': userID, '_id': ObjectId(count_reset_ids)})
    print(count_reset_sen)
    new_count = 0
    db.sentances.update_one({'userID': userID, '_id': ObjectId(count_reset_ids)}, {'$set': {'count': new_count}})
    msg = '횟수 초기화!'
    return jsonify({'result': 'success', 'msg': msg, 'new_count': new_count})


@app.route('/score', methods=['POST'])
def score_get():
    # answer_list = set(list(request.form['answer'].split())) #list(request.form['answer'].split())
    # eng_sen1 = set(list(request.form['eng_test'].split()))  #list(request.form['eng_test'].split())

    # 입력한 값
    answer_list = list(request.form['answer'].split())
    # 정답
    eng_sen2 = list(request.form['eng_test'].split())
    eng_sen1 = list(request.form['eng_test'].split())

    score = 0
    for answer in answer_list:
        for eng in eng_sen1:
            if answer.lower() == eng.lower():
                score += 1
                eng_sen1.remove(eng)

    # for word in eng_sen1:
    #     for answer_word in answer_list:
    #         if word.lower() == answer_word.lower():
    #             score +=1
    my_score = str(len(eng_sen2)) + '단어 중 ' + str(score) + '개 일치합니다!'  # (score/len(eng_sen1))*100
    return jsonify({'result': 'success', 'score': my_score})


@app.route('/workload', methods=['POST'])
def workload_post():
    userID = request.form['userID']
    workload_receive = request.form['workoad_give']
    today = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    whether_day = db.dayworkload.find_one({'userID': userID, 'date': today}, {'_id': 0})
    print('whenther_day', whether_day)
    if not whether_day:
        db.dayworkload.insert_one({'userID': userID, 'date': today, 'workload': workload_receive})
    else:
        new_workload = int(db.dayworkload.find_one({'userID': userID, 'date': today}, {'_id': 0})['workload']) + int(
            workload_receive)
        db.dayworkload.update_one({'userID': userID, 'date': today}, {'$set': {'workload': new_workload}})
    msg = '오늘 총 ' + str(
        db.dayworkload.find_one({'userID': userID, 'date': today}, {'_id': 0})['workload']) + '개를 학습하셨습니다!'

    return jsonify({'result': 'success', 'msg': msg})


@app.route('/deletelist', methods=['POST'])
def delete_list():
    userID = request.form['userID']
    delete_list = request.form['delete_list']
    delete_list1 = json.loads(delete_list)
    for delete_sen in delete_list1:
        print(delete_sen)
        db.sentances.update_one({'userID': userID, 'korean': delete_sen}, {'$set': {'running': 'N'}})
    #
    # for delete_sen in delete_list1:
    #     delete1 = db.sentances.find_one({'korean':delete_sen})
    #     db.sentances.delete_one(delete1)
    msg = '선택한 항목이 학습목록에서 제외되었습니다.'
    return jsonify({'result': 'success', 'msg': msg})


@app.route('/returnlist', methods=['POST'])
def return_list():
    userID = request.form['userID']
    return_list = request.form['return_list']
    return_list1 = json.loads(return_list)
    for return_sen in return_list1:
        db.sentances.update_one({'userID': userID, 'korean': return_sen}, {'$set': {'running': 'Y'}})

    # for return_sen in return_list1:
    #     return1 = db.excepts.find_one({'korean':return_sen})
    #     db.excepts.delete_one(return1)
    msg = '선택한 항목이 학습목록에서 포함되었습니다.'
    return jsonify({'result': 'success', 'msg': msg})


@app.route('/memo', methods=['POST'])
def memo():
    userID = request.form['userID']
    memo = request.form['memo']
    kor = request.form['kor']
    db.sentances.update_one({'userID': userID, 'korean': kor}, {'$set': {'memo': memo}})
    msg = '메모가 저장되었습니다.'
    return jsonify({'result': 'success', 'msg': msg})


@app.route('/sendtosentance', methods=['POST'])
def sendtome():
    userID = request.form['userID']
    kor_sen = request.form['kor_sen']
    print(kor_sen)
    new_sen = db.sentances.find_one({'korean': kor_sen}, {'_id': 0})
    print(new_sen)
    eng = new_sen['eng']
    reference = new_sen['reference']
    print(eng)
    writerID = new_sen['writerID']
    print(eng)
    sentance = {'userID': userID, 'writerID': writerID, 'korean': kor_sen, 'eng': eng, 'reference': reference, 'count': 0, 'memo': '',
                'running': 'Y'}
    print(sentance)
    if userID == writerID:
        msg = '본인이 입력한 문장입니다.'
    else:
        db.sentances.insert_one(sentance)
        whether_benefactor = db.sentances.find_one({'benefactor': writerID})
        if not whether_benefactor:
            new_benefactor = {'benefactor': writerID, 'frequency': 1}
            db.sentances.insert_one(new_benefactor)
        else:
            new_frequency = db.sentances.find_one({'benefactor': writerID})['frequency'] + 1
            db.sentances.update_one({'benefactor': writerID}, {'$set': {'frequency': new_frequency}})
        msg = '내 문장에 추가되었습니다.'
    return jsonify({'result': 'success', 'msg': msg})


@app.route('/credits', methods=['POST'])
def credits():
    userID = request.form['userID']
    whether_frequency = db.sentances.find_one({'benefactor': userID})['frequency']
    if not whether_frequency:
        frequency = 0
    else:
        frequency = whether_frequency
    return jsonify({'result': 'success', 'frequency': frequency})


@app.route('/search', methods=['GET'])
def search():
    search_word = request.args.get('search_word')
    print(str(search_word))
    entire_eng = list(db.sentances.find({'eng': {'$regex': search_word, '$options': 'i'}, }, {'_id': 0}))
    entire_list_korean = list(db.sentances.find({'korean': {'$regex': search_word, '$options': 'i'}}, {'_id': 0}))
    entire = entire_eng + entire_list_korean

    entire_list2 = []
    for search in entire:
        checking = 0
        for i in entire_list2:
            if search['korean'] == i['korean']:
                checking += 1
        if checking == 0:
            entire_list2.append(search)

    print(entire_list2)
    return jsonify({'result': 'success', 'list': entire_list2})

@app.route('/graph', methods=['GET'])
def graph():
    userID = request.args.get('userID')
    print(userID)
    graph_list = list(db.dayworkload.find({'userID':userID},{'_id':0}))

    graph_list.reverse()
    print(graph_list)
    return jsonify({'result': 'success', 'graph': graph_list})

####################################스크랩핑 크롤링 메타테그
# @app.route('/video_list', methods=['POST'])
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import schedule
def video_list():

    # driver = webdriver.Chrome('D:/temp/chromedriver.exe')
    # driver.get(url)

    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('window-size=1920x1080')
    options.add_argument("disable-gpu")
    options.add_argument(
        "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")

    driver = webdriver.Chrome('D:/temp/chromedriver.exe', options=options)
    url = 'https://www.youtube.com/c/%EB%9D%BC%EC%9D%B4%EB%B8%8C%EC%95%84%EC%B9%B4%EB%8D%B0%EB%AF%B8/videos'
    driver.get(url)

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    youtube = soup.select('.style-scope.ytd-grid-renderer')
    i = 0
    videos = []
    while i < 7:
        video = youtube[i]
        if not video.a:
            pass
        else:
            videos.append('https://www.youtube.com' + video.a['href'])
        i += 1
    driver.close()
    video_list = []
    for video in videos:
        url1 = video
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
        data = requests.get(url1, headers=headers)
        soup = BeautifulSoup(data.text, 'html.parser')

        og_image = soup.select_one('meta[property="og:image"]')
        og_title = soup.select_one('meta[property="og:title"]')
        og_description = soup.select_one('meta[property="og:description"]')

        url_title = og_title['content']
        url_description = og_description['content']
        url_image = og_image['content']
        print(url_title,url_image,url_description)
        today = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        video_list.append({'date':today,'url': video, 'title': url_title, 'desc': url_description, 'image': url_image})
        list_dic = {'date':today}
        i=0
        for video in video_list:
            i +=1
            list_dic[str(i)] = video

    db.video_list.insert_one(list_dic)

def job():
    today = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    whether = db.video_list.find({'date':today})
    if not whether:
        video_list()

def run():
    schedule.every(10).second.do(job)
    while True:
        schedule.run_pending()

@app.route('/video_list', methods=['POST'])
def video_send():
    today = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    list = db.video_list.find_one({'date':today},{'_id':0})

    return jsonify({'result': 'success', 'video_list': list})

@app.route('/send_email', methods=['POST'])
def send_email():
    address = request.form['address']
    content = request.form['content']
    print(address+content)
    import smtplib
    from email.mime.text import MIMEText
    google_server = smtplib.SMTP_SSL('smtp.gmail.com',465)

    google_server.login('gcnml0@gmail.com','ejugnntzoqaeskkk')

    msg = MIMEText(address+'  '+content)
    msg['Subject'] = '생활학원에서 건의 사랑 들어왔습니다.~~'

    google_server.sendmail(address,'gcnml0@gmail.com',msg.as_string())

    google_server.quit()
    return jsonify({'result': 'success','msg':'메일이 발송되었습니다. 소중한 의견 감사합니다.'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
