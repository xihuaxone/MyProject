import base64
from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex

from settings import global_config


class AesCrypt(object):
    def __init__(self):
        identify = global_config.get_section('identify')
        print(identify.get('user_login_sk'))
        self.key = identify.get('user_login_sk').encode('utf-8')
        self.mode = AES.MODE_CBC
        self.iv = identify.get('user_login_iv').encode('utf-8')

    @staticmethod
    def _pad_byte(b: bytes):
        bytes_num_to_pad = AES.block_size - (len(b) % AES.block_size)
        padding = bytes([bytes_num_to_pad]) * bytes_num_to_pad
        padded = b + padding
        return padded

    @staticmethod
    def _unpad_byte(b: bytes):
        return b[:-ord(b[len(b) - 1:])]

    def encrypt(self, code: str):
        code = code.encode('utf-8')
        code = self._pad_byte(code)
        encrypted = AES.new(self.key, self.mode, self.iv).encrypt(code)
        encrypted_base64 = base64.b64encode(b2a_hex(encrypted)).decode('utf8')
        return encrypted_base64

    def decrypt(self, code: str):
        base64_str = base64.b64decode(code.encode('utf8'))
        aes_str = AES.new(self.key, self.mode, self.iv).decrypt(a2b_hex(base64_str))
        complete_aes_str = str(self._unpad_byte(aes_str), encoding='utf8')
        return complete_aes_str
