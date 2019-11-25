from app import db
from config import Config, UPLOAD_FOLDER
import os
import json


class Payment(db.Model):
    shop_id = db.Column(db.Integer)
    shop_order_id = db.Column(db.Integer)
    amount = db.Column(db.Integer)
    payway = db.Column(db.String(256), nullable=True)
    currency = db.Column(db.String(10))
    product_info = db.Column(db.String(256), nullable=True)
    sign = db.Column(db.String(256), primary_key=True)
    lifetime = db.Column(db.Integer, nullable=True)
    payer_account = db.Column(db.String(128), nullable=True)
    id = db.Column(db.Integer, nullable=True)
    url = db.Column(db.String(256), nullable=True)



    JSON_FILENAME = '.data.json'

    def __repr__(self):
        return '<Payment> {}'.format(self.shop_order_id)

    def generate_key(self):
        hash_i = str('{}:{}:{}:{}:{}').format(self.amount, self.currency, self.shop_id,
                                              self.shop_order_id, Config.SECRET_KEY).encode('utf-8')
        key = hash_i.hex()
        return key

    @classmethod
    def key_to_path(cls, key):
        relative_path = os.path.join(key)
        return relative_path

    @classmethod
    def get(cls, key):
        relative_path = cls.key_to_path(key)
        path = os.path.join(UPLOAD_FOLDER, relative_path)
        with open(os.path.join(path, key + cls.JSON_FILENAME)) as json_file:
            infos = json.load(json_file)
            return cls(**infos)

    def __init__(self, shop_id, shop_order_id, amount, currency, product_info, sign, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.shop_id = shop_id
        self.shop_order_id = shop_order_id
        self.amount = amount
        self.currency = currency
        self.product_info = product_info
        self.sign = sign

    def save(self):
        self.key = self.generate_key()
        self.relative_path = self.key_to_path(self.key)
        path = os.path.join(UPLOAD_FOLDER, self.relative_path)
        os.makedirs(path)
        infos = {'shop_id': self.shop_id, 'shop_order_id': self.shop_order_id, 'amount': self.amount,
                 'currency': self.currency, 'product_info': self.product_info}
        path = os.path.join(UPLOAD_FOLDER, self.relative_path)
        with open(os.path.join(path, self.key + self.JSON_FILENAME), 'w') as json_file:
            json.dump(infos, json_file)
