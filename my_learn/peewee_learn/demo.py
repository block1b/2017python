# coding=utf8
# peewee 操作 postgresql
from peewee import *

db = PostgresqlDatabase(
    'peewee_test_db',
    user='postgres',
    password='111111',
    host='127.0.0.1',
)


class Person(Model):
    name = CharField()
    birthday = DateField()
    is_relative = BooleanField()

    class Meta:
        database = db


class Pet(Model):
    owner = ForeignKeyField(Person, related_name='pets')
    name = CharField()
    animal_type = CharField()

    class Meta:
        database = db

# 连接
db.connect()
# db.create_tables([Person, Pet])

# # 保存数据
from datetime import date
#
# # 生成对象并执行save操作
# uncle_bob = Person(name='Bob', birthday=date(1960, 1, 15), is_relative=True)
# uncle_bob.save()
#
# # 用create方法直接创建记录
# grandma = Person.create(name='Grandma', birthday=date(1935, 3, 1), is_relative=True)
herb = Person.create(name='Herb', birthday=date(1950, 5, 5), is_relative=False)
#
# # 嗯，grandma没有给姓
# grandma.name = 'Grandma L'
# grandma.save()
#
# # 现在添加宠物
# bob_kitty = Pet.create(owner=uncle_bob, name='Kitty', animal_type='cat')
# herb_fido = Pet.create(owner=herb, name='Fido', animal_type='dog')
# herb_mittens = Pet.create(owner=herb, name='Mittens', animal_type='cat')
# herb_mittens_jr = Pet.create(owner=herb, name='Mittens Jr', animal_type='cat')

# # 取一行数据，使用SelectQuery.get()
# grandma = Person.select().where(Person.name == 'Grandma L').get()
# print(grandma.birthday)

# 取所有数据
for person in Person.select():
    print(person.name, person.is_relative)

# # 列出所有类型为cat的宠物的主人名字
# query = Pet.select().where(Pet.animal_type == 'cat')
# for pet in query:
#     print(pet.name, pet.owner.name)
