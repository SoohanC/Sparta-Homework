# flask_server
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

# db
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.dbhomework


@app.route('/')
def homework():
    return render_template('index.html')


@app.route('/api/order', methods=["POST"])
def postOrder():
    quantity = request.form["quantity"]
    name = request.form["name"]
    address = request.form["address"]
    phone_num = request.form["phoneNumber"]
    credit_card = request.form["creditCard"]
    exp_date = request.form["expirationDate"]
    cvc = request.form["CVC"]
    db_data = {"quantity": quantity, "name": name, "address": address, "phoneNum": phone_num,
               "creditCard": credit_card, "expDate": exp_date, "cvc": cvc}
    db.salty_shopping.insert_one(db_data)
    order_data = {"quantity": quantity, "name": name, "address": address, "phoneNum": phone_num,
                  "creditCard": credit_card, "expDate": exp_date, "cvc": cvc}
    return jsonify({'result': 'success'})


@app.route('/api/order', methods=["GET"])
def getOrder():
    orders = list(db.salty_shopping.find({},{"_id":False}))
    return jsonify({'result': 'success', 'orders': orders})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
