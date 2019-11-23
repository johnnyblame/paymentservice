from app import app
from flask import render_template, redirect, flash
from app.forms import PayForm, CURRENCY_CHOICES


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    form = PayForm()
    if form.validate_on_submit():
        currency_choice = dict(CURRENCY_CHOICES).get(form.currency.data)

        if currency_choice == 'RUB':
            return redirect('/index')
        elif currency_choice == 'EUR':
            url = 'https://pay.piastrix.com/ru/pay'
            return redirect(url, code=307)
        else:
            url = 'https://pay.piastrix.com/ru/pay'
            return redirect(url, code=307)

    return render_template('index.html', title='PayNow', form=form)
