# coding=utf8
# 创建ORM模型
# 网关表，场景网关关联表
import data_prepare
from peewee import *
import datetime

db = PostgresqlDatabase(
    'dataplatform',
    # 'hantest',
    user='postgres',
    password='111111',
    # host='192.168.1.106',
    host='127.0.0.1',
)


# 网关
class Gateways(Model):
    id = IntegerField()
    gateway_name = TextField()
    gateway_api_key = TextField()
    gateway_type = TextField()
    gateway_shared_state = TextField()
    gateway_description = TextField()
    manager_id = IntegerField()

    class Meta:
        database = db


# 场景
class Scenes(Model):
    id = IntegerField()
    scene_name = TextField()
    manager_id = IntegerField()
    life_time = DateTimeField(default=datetime.datetime.now)
    scene_description = TextField()

    class Meta:
        database = db


# 场景-网关关联表
class Scenegateways(Model):
    scene_id = IntegerField()
    gateway_id = IntegerField()

    class Meta:
        database = db
        primary_key = CompositeKey('scene_id', 'gateway_id')


if __name__ == "__main__":
    db.connect()
    # db.create_table(Scenegateways)

    # g = Gateways.create(id=5, gateway_name='0', gateway_api_key='1234123412340005',
    #                     gateway_type='soft', gateway_shared_state='rw',
    #                     gateway_description='', manager_id=1)
    # s = Scenes.create(id=1,scene_name=2,manager_id=1)

    # emmm不知道为啥提示没有字段 id
    # sg = Scenegateways.create(scene_id=1, gateway_id=1)

    # 读取所有数据
    for i in Scenegateways.select():
        print(i.scene_id, i.gateway_id)
        try:
            # 删除
            i.delete_instance()

        except Exception as e:
            print e
            pass
    print "succeed"
