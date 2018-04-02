# coding=utf8
# 将peewee_learn/data_prepare.py准备的数据写入数据库
# 数据有：网关信息，节点信息，节点传感器信息
# 使用peewee_learn/models.py准备的上述三表的模型操作数据库
# 数据库：postgresql/henan_dev

from peewee_learn import data_prepare
from peewee_learn import models


# 生成大网关ids：[20180108001~20180108005]
big_gateway_ids = data_prepare.get_big_gateway_ids("201801008", 1, 5)
# print big_gateway_ids

# 生成节点ids：[0108001~0108005]
node_ids = data_prepare.get_node_ids("0108", 1, 5)
# print node_ids

# 将大网关的信息导入数据库表henan_dev/gateway
db = models.db
db.connect()  # 连接数据库
gateway = models.Gateway
# g = Gateway.create(id='test003', gateway_product=9, api_key='123456')
for a_id in big_gateway_ids:
    # gateway.create(id=a_id, gateway_product=9, api_key='123456')
    print "已将大网关", a_id, "存入数据库"

# 将节点信息导入数据库表henan_dev/node
node = models.Node
# n = Node.create(id='123', node_product=9)
for a_id in node_ids:
    # node.create(id=a_id, node_product=666)  # 默认节点的类型为测试节点，有全类型传感器
    print "已将节点", a_id, "存入数据库"

# 为节点生产类型"666"指定可以连接的传感器
# 获取准备的传感器类型[all]
attribute = data_prepare.attribute
# print attribute
# 将节点的传感器配置写入数据库
node_attribute = models.Node_attribute
# na = Node_attribute.create(node_product=2, attribute_name='tem',
#                            attribute_description='tem',
#                            attribute_type='string', id=666)
for a_sensor in attribute:
    # node_attribute.create(node_product=666, attribute_name=a_sensor,
    #                       attribute_description=a_sensor, attribute_type='string')
    print "已将传感器", a_sensor, "存入数据库"
