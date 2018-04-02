# coding=utf8
# 将生成的数据导入数据库
# 向数据库导入复数网关
from data_prepare import get_softgateway_ids
from db_model import db, Gateways, Scenegateways

if __name__ == "__main__":
    db.connect()

    print "清空数据表"
    # 读取所有数据
    for i in Scenegateways.select():
        print(i.scene_id, i.gateway_id)
        try:
            # 删除
            i.delete_instance()

        except Exception as e:
            print e
            # pass
    # 读取所有数据
    for i in Gateways.select():
        print(i.id, i.gateway_name)
        try:
            # 删除
            i.delete_instance()

        except Exception as e:
            print e
            # pass

    # # 向数据库写入数据
    # print "将测试数据写入数据库 loading。。。"
    # softgateway_ids = get_softgateway_ids("1234123412340", 1, 300)
    # # print softgateway_ids
    # count = 0
    # for api_key in softgateway_ids:
    #     count += 1
    #     try:
    #         # 写入网关数据
    #         g = Gateways.create(id=count, gateway_name=api_key, gateway_api_key=api_key,
    #                             gateway_type='soft', gateway_shared_state='rw',
    #                             gateway_description='', manager_id=1)
    #     except Exception as e:
    #         # print e
    #         pass
    #     try:
    #         # 写入场景网关关联数据
    #         sg = Scenegateways.create(scene_id=1, gateway_id=count)
    #     except Exception as e:
    #         # print e
    #         pass

    print "succeed"
