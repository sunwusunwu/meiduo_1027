# # -*- coding:utf-8 -*-
# # Author : Sunwu
# # Date : 2021/11/30 11:06
from django.core.files.storage import Storage
from django.conf import settings
from fdfs_client.client import Fdfs_client


class FastDFSStorage(Storage):
    """自定义存储到远程服务器的存储系统"""

    def __init__(self, client_path=None, base_url=None):
        self.client_path = client_path or settings.FDFS_CLIENT_CONF
        self.base_url = base_url or settings.FDFS_BASE_URL

    def _open(self, name, mode='rb'):
        pass

    def _save(self, name, content):
        """
        文件存储时什么调用此方法,但是此方法默认是向本地存储,在此方法做实现文件存储到远程的FastDFS服务器
        :param name: 要上传的文件名
        :param content: 以rb模式打开的文件对象 将来通过content.read() 就可以读取到文件的二进制数据
        :return: file_id
        """
        client = Fdfs_client(self.client_path)
        # 通过客户端上传文件的方法上传到远程服务器
        ret = client.upload_by_buffer(content.read())
        # 判断是否上传成功
        if ret.get('Status') != 'Upload successed.':
            raise Exception('Upload file failed')
        field_id = ret.get('Remote file_id')
        return field_id

    def exists(self, name):
        """
        当要进行上传时都调用此方法判断文件是否已上传,如果没有上传才会调用save方法进行上传
        :param name: 要上传的文件名
        :return: True(表示文件已存在,不需要上传)  False(文件不存在,需要上传)
        """
        return False

    def url(self, name):
        """
        当要访问图片时,就会调用此方法获取图片文件的绝对路径
        :param name: 要访问图片的file_id
        :return: 完整的图片访问路径: storage_server IP:8888 + file_id
        """
        return self.base_url + name





# client = Fdfs_client('F:/meiduo_1027/meiduo_mall/meiduo_mall/utils/fastdfs/client.conf')
# print(client)
# ret = client.upload_by_filename('C:/Users/jm/Desktop/001.png')
# print(ret)
