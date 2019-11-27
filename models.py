from routes import db


class Payment(db.Model):
    shop_id = db.Column(db.Integer)
    shop_order_id = db.Column(db.Integer)
    amount = db.Column(db.Integer)
    currency = db.Column(db.String(10))
    product_info = db.Column(db.String(256), nullable=True)
    sign = db.Column(db.String(256), primary_key=True)
    payway = db.Column(db.String(256), nullable=True)

    def __repr__(self):
        return '<Payment> {}'.format(self.sign)

    def __init__(self, shop_id, shop_order_id, amount, currency, product_info, sign, payway, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.shop_id = shop_id
        self.shop_order_id = shop_order_id
        self.amount = amount
        self.currency = currency
        self.product_info = product_info
        self.sign = sign
        self.payway = payway

