__author__ = 'dailin'
from fdfs_client.client import *


class FDFSClient:

    def __init__(self):
        import os

        curr_dir = os.path.dirname(os.path.realpath(__file__))
        configFile = curr_dir + os.sep + "client.conf"

        self.client = Fdfs_client(configFile)
        print("===========Fdfs_client初始化完成")

    def save(self,date,extName='png'):
        info = self.client.upload_by_buffer(filebuffer=date,file_ext_name=extName)
        return info['Remote file_id'].decode()



if __name__ == '__main__':
    with open("C:\\Users\\Administrator\\Desktop\\1.png",'rb') as pic:
        data = pic.read()

    uri = FDFSClient().save(data)
    print(uri)

