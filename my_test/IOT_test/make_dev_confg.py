# coding=utf8
# 用于生成IOT的配置文件

from schemas_json_model import dev_config
from marshmallow import Schema, fields, pprint
from peewee_learn import data_prepare


# 生成大网关ids：[20180108001~20180108005]
gateway_ids = data_prepare.get_big_gateway_ids("201801008", 1, 5)
# print big_gateway_ids
# 生成节点ids：[0108001~0108005]
nodes = data_prepare.get_node_ids("0108", 1, 5)
# print node_ids
# 获取准备的传感器类型[all]
attributes = data_prepare.attribute
# print attribute

# 以上为参数
cs = dev_config.ConstSettings(gateway_ids=gateway_ids, nodes=nodes, attributes=attributes)
pprint(cs.result.data)
# 写入文件
import json
jsObj = json.dumps(cs.result.data, indent=2)  # 缩进
add_n_jsObj = "const settings = " + jsObj + ";\n\nmodule.exports = settings;"  # 修饰为.js文件
fileObject = open('dev_conf.js', 'w')
fileObject.write(add_n_jsObj)
fileObject.close()
print type(add_n_jsObj)
