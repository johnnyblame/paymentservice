import hashlib
import logging
import urllib.parse
import urllib.request
import requests
from flask import render_template, redirect, request
from app import app, db
from app.models import Payment
from config import Config

logging.basicConfig(filename='error.log', level=logging.DEBUG)


@app.route('/')
def rec():
    return redirect('/index')


@app.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if request.form['currency'] == 'RUB' or request.form['currency'] == 643:
            if request.method == 'POST':
                shop_id = 5
                shop_order_id = 123456
                payway = 'payeer_rub'
                amount = request.form['amount']
                currency = request.form['currency']
                product_info = request.form['product_info']
                pure_sign = request.form['pure_sign']
                pure_sign = '{}:{}:{}:{}{}'.format(amount, currency, shop_id,
                                                   shop_order_id, Config.SECRET_KEY)
                sign = hashlib.sha256(pure_sign.encode()).hexdigest()
                entry = Payment(shop_id, shop_order_id, payway, amount, currency, product_info, sign)
                db.session.add(entry)
                db.session.commit()
                headers = {'Content-Type': 'application/json'}
                url = 'https://core.piastrix.com/invoice/create'
                values = {'shop_id': shop_id, 'shop_order_id': shop_order_id, 'payway': payway,
                          'amount': amount, 'currency': currency, 'description': product_info, 'sign': sign}
                data = urllib.parse.urlencode(values)
                req = urllib.request.Request(url, data=data, headers=headers)
                response = urllib.request.urlopen(req)
                the_page = response.read()
                return the_page

        elif request.form['currency'] == 'EUR' or request.form['currency'] == 978:
            if request.method == 'POST':
                data = request.form.to_dict()
                shop_id = request.form['shop_id']
                shop_order_id = request.form['shop_order_id']
                amount = request.form['amount']
                currency = request.form['currency']
                product_info = request.form['product_info']
                shop_sign = request.form['shop_sign']
                pure_sign = request.form['pure_sign']
                pure_sign = '{}:{}:{}:{}{}'.format(amount, currency, shop_id,
                                                   shop_order_id, Config.SECRET_KEY)
                sign = hashlib.sha256(pure_sign.encode()).hexdigest()
                entry = Payment(shop_id, shop_order_id, amount, currency, product_info, sign)
                db.session.add(entry)
                db.session.commit()
                data['sign'] = sign
                data['shop_sign'] = sign
                headers = {'Content-Type': 'application/json'}
                with open('data.txt', 'w') as file:
                    file.write(data)
                url = 'https://pay.piastrix.com/en/pay'
                # response = requests.post(url, data=data)
                response = redirect(url)
                response.headers = data
                return response

        elif request.form['currency'] == 'USD' or request.form['currency'] == 840:
            if request.method == 'POST':
                result = request.form.to_dict()
                shop_id = 5
                shop_order_id = 123456
                shop_amount = request.form['amount']
                shop_currency = request.form['currency']
                product_info = request.form['product_info']
                pure_sign = request.form['pure_sign']
                pure_sign = '{}:{}:{}:{}{}'.format(shop_amount, shop_currency, shop_id,
                                                   shop_order_id, Config.SECRET_KEY)
                sign = hashlib.sha256(pure_sign.encode()).hexdigest()
                entry = Payment(shop_id, shop_order_id, shop_amount, shop_currency, product_info, sign)
                db.session.add(entry)
                db.session.commit()
                url = 'https://core.piastrix.com/bill/create'
                params = {'shop_id': shop_id, 'shop_order_id': shop_order_id, 'shop_amount': shop_amount,
                          'payer_currency': shop_currency, 'shop_currency': shop_currency, 'description': product_info,
                          'sign': sign}
                data = urllib.parse.urlencode(params)
                headers = {'Content-Type': 'application/json'}
                esreq = requests.Request(url=url, headers=headers, data=values)
                resp = requests.Session().send(esreq.prepare())
                # req = urllib.request.Request(url, data=data, headers=headers)
                # response = urllib.request.urlopen(req)
                # the_page = response.read()
                return resp.content

    return render_template('index.html', title='PayNow')


@app.route('/result', methods=['POST', 'GET'])
def result():
    if request.method == 'POST':
        result = request.form.to_dict()
        shop_id = request.form['shop_id']
        shop_order_id = request.form['shop_order_id']
        amount = request.form['amount']
        currency = request.form['currency']
        product_info = request.form['description']
        pure_sign = request.form['pure_sign']
        pure_sign = '{}:{}:{}:{}{}'.format(amount, currency, shop_id,
                                           shop_order_id, Config.SECRET_KEY)
        sign = hashlib.sha256(pure_sign.encode()).hexdigest()
        result['sign'] = sign
        result['pure_sign'] = pure_sign
        return render_template('result.html', result=result)
