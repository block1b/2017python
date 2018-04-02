# coding=utf8
# 创建ORM模型
import data_prepare
from peewee import *
import datetime
import json

db = PostgresqlDatabase(
    'henan_dev',
    user='postgres',
    password='111111',
    host='127.0.0.1',
)


# 网关
class Gateway(Model):
    id = TextField()
    gateway_product = IntegerField()
    api_key = TextField()
    createdAt = DateTimeField(default=datetime.datetime.now)
    updatedAt = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = db


# jsonfield
class JSONField(TextField):
    def db_value(self, value):
        return json.dumps(value)

    def python_value(self, value):
        if value is not None:
            return json.loads(value)


# 节点
class Node(Model):
    id = TextField()
    node_product = IntegerField()
    attach_attributes = JSONField(default=None)
    createdAt = DateTimeField(default=datetime.datetime.now)
    updatedAt = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = db


# 节点传感器关联表
class Node_attribute(Model):
    node_product = IntegerField()
    attribute_name = TextField()
    attribute_description = TextField()
    attribute_type = TextField()
    id = IntegerField()
    createdAt = DateTimeField(default=datetime.datetime.now)
    updatedAt = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = db


# 存储的数据
class Node_data(Model):
    gateway = TextField()
    node = TextField()
    data_json = JSONField(default=None)
    id = IntegerField()
    createdAt = DateTimeField(default=datetime.datetime.now)
    updatedAt = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = db

if __name__ == "__main__":
    db.connect()
    # db.create_table(Gateway)
    # print "创建表gateway"
    # g = Gateway.create(id='test003', gateway_product=9, api_key='123456')
    # n = Node.create(id='123', node_product=9)
    # na = Node_attribute.create(node_product=2, attribute_name='tem',
    #                            attribute_description='tem',
    #                            attribute_type='string', id=666)
    for data in Node_data.select():
        print str(data.gateway)
