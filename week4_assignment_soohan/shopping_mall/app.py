from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.dbhomework


## HTML 화면 보여주기
@app.route('/')
def homework():
    return render_template('index.html')


# 주문하기(POST) API
@app.route('/order', methods=['POST'])
def save_order():
    name_receive=request.form['name']
    count_receive=request.form['count']
    address_receive=request.form['address']
    phone_receive=request.form['phone']
    db_data = {"name":name_receive,"count":count_receive,"address":address_receive,"phone":phone_receive}
    db.shopping_mall.insert_one(db_data) #여기서 db_data에 objectID 가 들어가져버림
    order_data = {"name":name_receive,"count":count_receive,"address":address_receive,"phone":phone_receive}
    return jsonify({'result': 'success', 'order': order_data})

# 주문 목록보기(Read) API
@app.route('/order', methods=['GET'])
def view_orders():
    orders = list(db.shopping_mall.find({},{"_id":False}))
    return jsonify({'result': 'success', 'orders': orders})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)