# coding=utf8
from datetime import date
from marshmallow import Schema, fields, pprint


class QueueSchema(Schema):
    exchange = fields.Str()
    routing_keys = fields.List(fields.Str())  # list string


class NodeSchema(Schema):
    node_id = fields.Str()
    attributes = fields.List(fields.Str())  # list string


class BigGatewaySchema(Schema):
    alias = fields.Str()
    gateway_id = fields.Str()
    dev_type = fields.Str()
    nodes = fields.Nested(NodeSchema, many=True)  # list NodeSchema
    queue = fields.Nested(QueueSchema())


# make a_up_dev
class UpDev(object):
    def __init__(self, num, gateway_id, nodes, attributes):
        exchange = 'gateway.' + str(gateway_id)
        routing_keys = []
        for node in nodes:
            for attribute in attributes:
                routing_key = 'node.' + str(node) + '.attributes.' + str(attribute)
                routing_keys.append(routing_key)

        queue_value = dict(exchange=exchange, routing_keys=routing_keys)
        queue = QueueSchema()
        queue_result = queue.dump(queue_value)

        # nodes
        nodes_value = []
        for node in nodes:
            node_value = dict(node_id=str(node), attributes=attributes)
            node_schema = NodeSchema()
            node_result = node_schema.load(node_value)
            nodes_value.append(node_result.data)

        # gateway
        gateway = dict(alias='test_gateway_' + str(num), gateway_id=gateway_id, dev_type='IotGateway',
                       nodes=nodes_value, queue=queue_result.data)

        gateway_schema = BigGatewaySchema()
        self.result = gateway_schema.dump(gateway)


if __name__ == "__main__":
    # 参数
    N = 0  # 编号
    gateway_id = '0134567839600003'  # 上行网关id
    nodes = ['0300110203600018', '0300110103700025']  # 网关下的节点s
    attributes = ['tem', 'hum']  # 节点上的传感器s，默认同组网关有相同数量传感器
    # 网关配置a_up_dev dict
    updev = UpDev(num=N, gateway_id=gateway_id, nodes=nodes, attributes=attributes)
    pprint(updev.result.data, indent=2)  # 格式化输出
