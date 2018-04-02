# coding=utf8
from marshmallow import Schema, fields, pprint
from biggateway import UpDev


class Settings(Schema):
    rabbitmq_conf = fields.Dict()
    up_dev = fields.List(fields.Dict)


class ConstSettings(object):
    def __init__(self, gateway_ids, nodes, attributes):
        up_devs = []
        for gateway_id in gateway_ids:
            up_dev = UpDev(num=gateway_id, gateway_id=gateway_id,
                           nodes=nodes, attributes=attributes)
            up_devs.append(up_dev.result.data)

        # print up_devs
        rabbitmq_conf = dict(host='127.0.0.1')
        setting = dict(rabbitmq_conf=rabbitmq_conf, up_dev=up_devs)

        setings = Settings()
        self.result = setings.dump(setting)


if __name__ == "__main__":
    gateway_ids = ['201501',
                   '201502',
                   '201503',
                   '201504',
                   '201505'
                   ]  # 复数个大网关

    nodes = ['0300110203600018', '0300110103700025']  # 网关下的节点s，默认网关使用的相同节点
    attributes = ['tem', 'hum']  # 节点上的传感器s，默认同组网关有相同数量传感器
    # 以上为参数
    cs = ConstSettings(gateway_ids=gateway_ids, nodes=nodes, attributes=attributes)
    pprint(cs.result.data)
    # 写入文件
    import json
    jsObj = json.dumps(cs.result.data, indent=2)  # 缩进
    add_n_jsObj = "const settings = " + jsObj + ";\n\nmodule.exports = settings;"  # 修饰为.js文件
    fileObject = open('dev_conf.js', 'w')
    fileObject.write(add_n_jsObj)
    fileObject.close()
    print type(add_n_jsObj)
