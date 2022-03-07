from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

from pymongo import MongoClient

# client = MongoClient('mongodb+srv://test:sparta@cluster0.psxi0.mongodb.net/Cluster0?retryWrites=true&w=majority')
# db = client.dbsparta

client = MongoClient('mongodb+srv://test:sparta@cluster0.g14io.mongodb.net/Cluster0?retryWrites=true&w=majority')
db = client.dbsparta

@app.route('/')
def home_page():
    return render_template('index.html')

@app.route('/login')
def login_page():
    return render_template('login.html')

@app.route('/logout')
def logout_page():
    return render_template('index.html')

@app.route('/mypage')
def my_page():
    return render_template('mypage.html')


@app.route('/allrooms', methods=['GET'])
def show_rooms():
    myrooms = list(db.myrooms.find({}, {'_id': False}))
    return jsonify({'rooms': myrooms})


# API 역할을 하는 부분
@app.route('/allrooms', methods=['POST'])
def upload_rooms():
    img_receive = request.form['room_img']
    title_receive = request.form['room_title']

    doc = {
        'title': title_receive,
        'img': img_receive
    }
    db.myrooms.insert_one(doc)

    return jsonify({'msg': f'{title_receive} 저장!'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)