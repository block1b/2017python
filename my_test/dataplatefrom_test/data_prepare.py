# coding=utf8
# 生成软网关号300个尾号x001-x300


# 批量生成测试数据id
def get_xxx_ids(id_head, min_id, max_id, id_digits):
    id_test_data_s = []
    for a_id in range(min_id, max_id + 1):
        a_gateway_id = id_head + str(a_id).zfill(id_digits)
        id_test_data_s.append(a_gateway_id)

    return id_test_data_s


# 批量生成软网关id
def get_softgateway_ids(id_head, min_id, max_id, id_digits=3):
    return get_xxx_ids(id_head, min_id, max_id, id_digits)


if __name__ == "__main__":
    # 生成软网关id（1234123412340001-1234123412340300）
    softgateway_ids = get_softgateway_ids("1234123412340", 1, 300)
    print softgateway_ids
