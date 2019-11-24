from app import app, db
from flask import render_template, redirect, flash, request
from app.forms import PayForm, CURRENCY_CHOICES
from app.models import Payment

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    form = PayForm()
    if form.validate_on_submit():
        currency_choice = dict(CURRENCY_CHOICES).get(form.currency.data)

        if currency_choice == 'RUB':
            return redirect('/index')
        elif currency_choice == 'EUR':
            if request.method == 'POST':
                shop_order_id = 5
                shop_id = 5
                amount = request.form['amount']
                currency = request.form['currency']
                product_info = request.form['product_info']
                sign = request.form['key']
                entry = Payment(shop_order_id, shop_id, amount, currency, product_info, sign)
                db.session.add(entry)
                db.session.commit()
                url = 'https://pay.piastrix.com/ru/pay'
                return redirect(url, code=307)
        else:
            url = 'https://pay.piastrix.com/ru/pay'
            return redirect(url, code=307)

    return render_template('index.html', title='PayNow', form=form)
