# coding=utf8
# 将目录内所有文件打包压缩为7z
# 参数：源文件目录，压缩文件保存目录，压缩文件名
# -*- coding: utf-8 -*-

import os
import zipfile


def dir_to_7z(dir_path, zip_path, zip_name):
    try:
        # 检查参数目录，若不存在，创建
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        if not os.path.exists(zip_path):
            os.makedirs(zip_path)
        # 创建压缩文件
        zip_path_name = zip_path + '/' + zip_name
        zf = zipfile.ZipFile(str(zip_path_name), mode='w')
        # 遍历目标目录
        for root, dirs, files in os.walk(str(dir_path), topdown=False):
            for name in files:
                # 获取目录内文件名
                file_name = os.path.join(root, name)
                # print file_name
                # 压缩该文件
                zf.write(file_name)
        print "succeed"
    except Exception:
        print "failed"


if __name__ == "__main__":
    doc_dir = "./doc_dir"
    zip_dir = "./doc_7z"
    zip_name = "demo.7z"
    dir_to_7z(doc_dir, zip_dir, zip_name)
