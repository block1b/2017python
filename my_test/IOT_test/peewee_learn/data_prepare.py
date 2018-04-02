# coding=utf8
# 需要准备的数据，
# 数据库需要的数据：网关信息，节点信息，节点传感器；
# 网关模拟脚本需要的数据：网关与节点关联关系，节点与传感器关联关系，传感器值
# 自定义简化：每个节点接固定数量的传感器，传感器值相同，保留网关与节点的多对多关系。


# 批量生成测试数据id
def get_xxx_ids(id_head, min_id, max_id, id_digits):
    id_test_data_s = []
    for a_id in range(min_id, max_id + 1):
        a_gateway_id = id_head + str(a_id).zfill(id_digits)
        id_test_data_s.append(a_gateway_id)

    return id_test_data_s


# 大网关信息s
# big_gateway_id_model="20180105xxx"  # 年+月+日+n位编号
# 批量生成大网关id（id固定前缀，最小id编号，最大id编号，id编号位数）
def get_big_gateway_ids(id_head, min_id, max_id, id_digits=3):
    return get_xxx_ids(id_head, min_id, max_id, id_digits)
# get_big_gateway_ids("20180105", 1, 2, 3)


# 节点信息s
# node_id_model="0105xxx"  # 月+日+n位编号
# 批量生成节点id（id固定前缀，最小id编号，最大id编号，id编号位数）
def get_node_ids(id_head, min_id, max_id, id_digits=3):
    return get_xxx_ids(id_head, min_id, max_id, id_digits)
# get_node_ids("0105", 1, 3, 3)

# 传感器类型s
# 默认全全传感器类型14种
attribute = ['tem', 'hum', 'gas', 'val', 'cur', 'fre',
             'lig', 'pre', 'swi', 'wat', 'rai', 'res',
             'tim', 'err']
# 默认传感器值相同
default_value = "123"  # 默认属性值
attribute_values = {
    'tem': default_value, 'hum': default_value,
    'gas': default_value, 'val': default_value,
    'cur': default_value, 'fre': default_value,

    'lig': default_value, 'pre': default_value,
    'swi': default_value, 'wat': default_value,
    'rai': default_value, 'res': default_value,
    'tim': default_value, 'err': default_value
    }

# 节点与传感器的关联关系
# 自定义关系，默认多有节点连接了所有传感器
# 数据库中该关系由节点产品类型绑定,在节点产品中添加标号位666的测试节点产品
node_attribute = dict(node_product=666, attribute=attribute)
# 网关模拟脚本中所有节点使用所有传感器值attribute_values

# 网关与节点关系表
# 1.自定义
gateway_node = dict(gateway="20180105001", node=['0105001', '0105002'])
# 2.m*n,组合结果参考自定义格式
# schemas_json_model网关模拟脚本使用时需结合:
# python package schemas_json_model/gateway_date.py
