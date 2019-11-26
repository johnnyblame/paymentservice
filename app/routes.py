import hashlib
import logging
import requests
from flask import render_template, redirect, request, jsonify
from app import app, db
from app.models import Payment
from config import Config
import json

logging.basicConfig(filename='error.log', level=logging.INFO)


@app.route('/')
def rec():
    return redirect('/index')


@app.route('/index', methods=['GET', 'POST'])
def index():
    return render_template('index.html', title='PayNow')


@app.route('/pay_handler', methods=['GET', 'POST'])
def pay():
    j = request.get_json()
    if j['currency'] == 643 or j['currency'] == '643':
        if request.method == "POST":
            shop_id = 5
            shop_order_id = 123456
            payway = 'payeer_rub'
            amount = j['amount']
            currency = j['currency']
            product_info = j['description']
            pure_sign = '{}:{}:{}:{}:{}{}'.format(amount, currency, payway, shop_id,
                                                  shop_order_id, Config.SECRET_KEY)
            sign = hashlib.sha256(pure_sign.encode('utf8')).hexdigest()
            entry = Payment(shop_id, shop_order_id, amount, currency, product_info, sign, payway)
            db.session.add(entry)
            db.session.commit()
            url = 'https://core.piastrix.com/invoice/create'
            params = {'shop_id': shop_id, 'shop_order_id': shop_order_id,
                      'amount': '{0:.2f}'.format(float(amount)),
                      'currency': int(currency), 'payway': payway,
                      'description': product_info, 'sign': sign}
            headers = {'Content-Type': 'application/json'}
            data = json.dumps(params)
            response = requests.post(url, data, headers=headers).json()
            if response['result'] is True:
                return jsonify(dict(redirect=response['data']['url']))
            else:
                print(response)

    elif j['currency'] == '978' or j['currency'] == 978:
        if request.method == "POST":
            shop_id = 5
            shop_order_id = 101
            amount = j['amount']
            currency = j['currency']
            product_info = j['description']
            pure_sign = '{}:{}:{}:{}{}'.format(amount, currency, shop_id,
                                               shop_order_id, Config.SECRET_KEY)
            sign = hashlib.sha256(pure_sign.encode('utf-8')).hexdigest()
            entry = Payment(shop_id, shop_order_id, amount, currency, product_info, sign, payway=None)
            db.session.add(entry)
            db.session.commit()
            params = {'shop_id': shop_id, 'shop_order_id': shop_order_id, 'amount': '{0:.2f}'.format(float(amount)),
                      'currency': int(currency), 'description': product_info, 'sign': sign}
            url = 'https://pay.piastrix.com/en/pay'
            headers = {'Content-Type': 'application/json'}
            data = json.dumps(params)
            requests.post(url, data, headers=headers)
            return jsonify(dict(redirect=url))


    elif j['currency'] == 840 or j['currency'] == '840':
        if request.method == "POST":
            shop_id = 5
            shop_order_id = 123456
            shop_amount = j['amount']
            shop_currency = j['currency']
            product_info = j['description']
            pure_sign = '{}:{}:{}:{}:{}{}'.format(shop_currency, '{0:.2f}'.format(float(shop_amount)), shop_currency,
                                                  shop_id, shop_order_id, Config.SECRET_KEY)
            sign = hashlib.sha256(pure_sign.encode('utf-8')).hexdigest()
            entry = Payment(shop_id, shop_order_id, shop_amount, shop_currency, product_info, sign, payway=None)
            db.session.add(entry)
            db.session.commit()
            url = 'https://core.piastrix.com/bill/create'
            params = {'shop_id': shop_id, 'shop_order_id': shop_order_id,
                      'shop_amount': '{0:.2f}'.format(float(shop_amount)),
                      'payer_currency': int(shop_currency), 'shop_currency': int(shop_currency),
                      'description': product_info, 'sign': sign}
            headers = {'Content-Type': 'application/json'}
            data = json.dumps(params)
            response = requests.post(url, data, headers=headers).json()
            if response['result'] is True:
                return jsonify(dict(redirect=response['data']['url']))
            else:
                print(response)

