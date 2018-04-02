# coding=utf8
# 使用模型序列化大网关模拟数据
from marshmallow import Schema, fields, pprint

# gateway_data = {
#         "node_datas": [{
#             "node_id": "0300110203600018",
#             "node_attributes": {
#                 "hum": "10.770000", "tem": "19.200002"
#                 }
#             },
#             {
#             "node_id": "0300110103700025",
#             "node_attributes": {
#                 "hum": "10.780000", "tem": "19.200003"
#                 }
#             }]
#         }


class NodeSchma(Schema):
    node_id = fields.Str()
    node_attributes = fields.Dict()


class GatewayData(Schema):
    node_datas = fields.Nested(NodeSchma, many=True)


class GetGatewayData(object):
    def __init__(self, nodes, values):
        node_datas = []
        for node in nodes:
            node_data_dict = dict(node_id=str(node), node_attributes=values)
            n = NodeSchma()
            node_data = n.dump(node_data_dict)
            node_datas.append(node_data.data)

        gateway_data_dict = dict(node_datas=node_datas)
        gateway_data = GatewayData()
        self.result = gateway_data.dump(gateway_data_dict)


if __name__ == "__main__":
    nodes = ["0300110203600018", "0300110103700025"]
    # attributes = ['hum', 'tem']
    values = {'hum': '1', 'tem': '2'}

    ggd = GetGatewayData(nodes=nodes, values=values)
    pprint(ggd.result.data, indent=2)
    print type(ggd.result.data)
