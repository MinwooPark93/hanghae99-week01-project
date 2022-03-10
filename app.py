from flask import Flask, render_template, jsonify, request, redirect, url_for
from pymongo import MongoClient
import jwt
import hashlib
import certifi
import os
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta


app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config['UPLOAD_FOLDER'] = "./static/profile_pics"

SECRET_KEY = 'Hanghae99team10project'

ca = certifi.where()

client = MongoClient("mongodb+srv://sharerooom:shareroom@cluster0.skz7o.mongodb.net/cluster0?retryWrites=true&w=majority",tlsCAFile=ca)
db = client.shareroom


@app.route('/')
def home():
    diaries = list(db.pictures.find({}, {'_id': False}))
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.users.find_one({"username": payload["id"]})
        return render_template('index.html', user_info=user_info, diaries=diaries)
    except jwt.ExpiredSignatureError:
        return redirect(url_for("login", msg="로그인 시간이 만료되었습니다."))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("login", msg="로그인 정보가 존재하지 않습니다."))


@app.route('/login')
def login():
    msg = request.args.get("msg")
    return render_template('login.html', msg=msg)


@app.route('/sign_in', methods=['POST'])
def sign_in():
    # 로그인
    username_receive = request.form['username_give']
    password_receive = request.form['password_give']

    pw_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()
    result = db.users.find_one({'username': username_receive, 'password': pw_hash})

    if result is not None:
        payload = {
         'id': username_receive,
         'exp': datetime.utcnow() + timedelta(seconds=60 * 60 * 24)  # 로그인 24시간 유지
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256').decode('utf-8')
        ## 로컬개발환경에서는 .decode('utf-8')을 사용하였을때 sever error 발생,
        ## python3.6 ver 이상부터 사용하지 않는 방식이다.
        ## 서버 환경에 있는 python의 version에 따라 .decode('utf-8') 부분을 추가,삭제 해야할지 고민해야함
        return jsonify({'result': 'success', 'token': token})
    # 찾지 못하면
    else:
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})


@app.route('/sign_up/save', methods=['POST'])
def sign_up():
    username_receive = request.form['username_give']
    password_receive = request.form['password_give']
    password_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()
    doc = {
        "username": username_receive,                               # 아이디
        "password": password_hash,                                  # 비밀번호
        "profile_name": username_receive,                           # 프로필 이름 기본값은 아이디
    }
    db.users.insert_one(doc)
    return jsonify({'result': 'success'})


@app.route('/sign_up/check_dup', methods=['POST'])
def check_dup():
    # 아이디 중복확인 체크
    username_receive = request.form['username_give']
    exists = bool(db.users.find_one({"username": username_receive}))
    return jsonify({'result': 'success', 'exists': exists})

######################################################################################
# 병윤님 섹션 추가
######################################################################################

@app.route('/pictures')
def review_home():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])

        return render_template('index.html', diaries = list(db.pictures.find({}, {'_id': False}))
)

    except jwt.ExpiredSignatureError:
        return redirect(url_for("login", token_expired="로그인 시간이 만료되었습니다."))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("login"))


# @app.route('/pictures', methods=['GET'])
# def show_pictures():
#     diaries = list(db.pictures.find({}, {'_id': False}))
#     return render_template('index.html', diaries=diaries)


@app.route('/pictures', methods=['POST'])
def save_pictures():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.users.find_one({"username": payload["id"]})
        # 데이터를 reviw.html에서 받아옴
        content_receive = request.form['content_give']

        file = request.files["file_give"]
        # 확장자명 만듬
        extension = file.filename.split('.')[-1]

        # datetime 클래스로 현재 날짜와시간 만들어줌 -> 현재 시각을 출력하는 now() 메서드
        today = datetime.now()
        mytime = today.strftime('%Y-%m-%d-%H-%M-%S')

        filename = f'file-{mytime}'
        # 파일에 시간붙여서 static폴더에 filename 으로 저장
        save_to = f'static/{filename}.{extension}'
        file.save(save_to)

        doc = {
            'username':user_info["username"],
            'profile_name':user_info["profile_name"],
            'content': content_receive,
            'file': f'{filename}.{extension}',
            'time': today.strftime('%Y.%m.%d')
        }
        # pictures collection에 저장
        db.pictures.insert_one(doc)

        return jsonify({'msg': '저장 완료!'})
    except(jwt.ExpiredSignatureError, jwt.exceptions.DecodeError):
        return redirect(url_for("home"))

######################################################################################
######################################################################################


# mypage link-test
@app.route('/mypage')
def mypage():
    token_receive = request.cookies.get('mytoken')
    payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
    user_info = db.users.find_one({"username": payload["id"]})
    return render_template('mypage.html', user_info=user_info)


# mypage ajax-GET-/pictures
@app.route('/picturesToMypage', methods=['GET'])
def load_pictures():
    diaries = list(db.pictures.find({}, {'_id': False}))
    return jsonify({'diaries': diaries})

# mypage ajax-POST-/pictures-delete
@app.route('/picturesToMypage', methods=['POST'])
def del_pictures():
    picture = request.form['picture_give']

    picture_div = picture.split('/')

    file = f'static/{picture_div[2]}'

    os.remove(file)

    # pictures = list(db.pictures.find({'file': a[2]}, {'_id': False}))
    db.pictures.delete_one({'file': picture_div[2]})
    # print(pictures)

    return jsonify({'result': 'success'})

######################################################################################
######################################################################################

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)

