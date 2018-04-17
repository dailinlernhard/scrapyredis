__author__='dailin'

import hashlib

class Encryptor(object):

    @classmethod
    def encrypt(cls,encrypt_type,value):
        if hasattr(hashlib,encrypt_type):
            res = getattr(hashlib,encrypt_type)(value)

            return res.hexdigest()


if __name__ == '__main__':
    res = Encryptor.encrypt('md5','100025366'.encode())
    print(res)