# -*- coding: utf-8 -*-
# flake8: noqa

from qiniu import Auth, put_file, etag,put_data
import qiniu.config

#需要填写你的 Access Key 和 Secret Key
access_key = 'iLe599pzNdu7dOIJGWgnOr_nTUu0xB7Xi3pgfKBJ'
secret_key = 'rmlNgcC0Uogx3vhZwsBPuCoONJz4HVtjAnt5DvTi'
def storage(filedata):
    #上传图片到七牛
    #构建鉴权对象
    q = Auth(access_key, secret_key)

    #要上传的空间
    bucket_name = 'ihome'

    # #上传后保存的文件名
    # key = 'my-python-logo.png'

    #生成上传 Token，可以指定过期时间等
    token = q.upload_token(bucket_name, None, 3600)

    #要上传文件的本地路径
    # localfile = './sync/bbb.jpg'

    ret, info = put_data(token, None, filedata)
    # print(ret)
    # print(info)
    # print("key",ret.get("key"))
    if info.status_code == 200:
        #上传成功，返回文件名
        return ret.get("key")
    else:
        raise Exception("上传七牛失败")

if __name__ == '__main__':
    with open("./timg.jpg","rb")as f:
        filedata=f.read()
        storage(filedata)

