# coding=utf8
# 压缩文件
import zipfile
print('creating archive')
zf = zipfile.ZipFile('./doc_7z/demo.7z', mode='w')
try:
    print('adding doc')
    zf.write('./doc_dir/demo.docx')
finally:
    print('closing')
    zf.close()
