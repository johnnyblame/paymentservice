from app import db
from config import Config, UPLOAD_FOLDER
import uuid
import os
import simplejson


class Payment(db.Model):
    shop_id = db.Column(db.Integer)
    shop_order_id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Integer)
    currency = db.Column(db.String(10))

    JSON_FILENAME = '.data.json'

    def __repr__(self):
        return '<Payment> {}'.format(self.shop_order_id)

    def generate_key(self):
        hash_i = str(self.amount + ':' + self.currency + ':' + self.shop_id + ':' + self.shop_order_id + ':'
                     + Config.SECRET_KEY)
        key = uuid.uuid4().hex[:hash_i]
        return key

    @classmethod
    def key_to_path(cls, key):
        relative_path = os.path.join(key[0], key[1], key)
        return relative_path

    @classmethod
    def get(cls, key):
        relative_path = cls.key_to_path(key)
        path = os.path.join(UPLOAD_FOLDER, relative_path)
        with open(os.path.join(path, key + cls.JSON_FILENAME)) as json_file:
            infos = simplejson.load(json_file)
            return cls(**infos)

    def __init__(self, *args, **kwargs):
        self.key = kwargs.get('key')
        self.path = kwargs.get('path')
        self.shop_id = kwargs.get('shop_id')
        self.shop_order_id = kwargs.get('shop_order_id')
        self.amount = kwargs.get('amount')
        self.currency = kwargs.get('currency')

    def save(self):
        self.key = self.generate_key()
        self.relative_path = self.key_to_path(self.key)
        path = os.path.join(UPLOAD_FOLDER, self.relative_path)
        os.makedirs(path)
        infos = {'shop_id': self.shop_id, 'shop_order_id': self.shop_order_id, 'amount': self.amount,
                 'currency': self.currency}
        path = os.path.join(UPLOAD_FOLDER, self.relative_path)
        with open(os.path.join(path, self.key + self.JSON_FILENAME), 'w') as json_file:
            simplejson.dump(infos, json_file)
