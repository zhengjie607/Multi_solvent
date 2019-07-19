


from Crypto.Cipher import AES,DES
from binascii import b2a_hex, a2b_hex
import binascii 
import os

class PrpCrypt(object):
 
    def __init__(self, key):
        self.key = key.encode('utf-8')
        self.mode = AES.MODE_CBC
        self.BS = AES.block_size 
    def encrypt(self, text):
        text=self.pad(text)
        text = text.encode('utf-8')
        cryptor = AES.new(self.key, self.mode, self.key)
        self.ciphertext = cryptor.encrypt(text)
        return binascii.b2a_base64(self.ciphertext)
 
    # 解密后，去掉补足的空格用strip() 去掉
    def decrypt(self, text):
        cryptor = AES.new(self.key, self.mode,self.key)
        plain_text = cryptor.decrypt(binascii.a2b_base64(text))
        aaa=bytes.decode(plain_text)
        aaa=self.unpad(aaa)
        # return plain_text.rstrip('\0')
        return aaa
    def pad(self,s): 
        return s + (self.BS - len(s) %self.BS) * chr(self.BS - len(s) % self.BS)
    def unpad(self,s): 
        return s[:-ord(s[len(s) - 1:])]
if __name__ == '__main__':
    pc = PrpCrypt("ynrvhnqqeatwwpon")  # 初始化密钥
    e = pc.encrypt("2EQ+dsLxGas2V+/HqU2kMg==23EXwLqGILT5LRaWyyukQagw==VDv3uIqbfqtaKP+jeIeapA==18CwcpBGdJYJIcW1zQXW4ZuXw==")  # 加密
    d = pc.decrypt(e)  # 解密
    f=open("1.txt","w")
    print("加密:",str(e))
    print("解密:", d)
    f.write(str(e,encoding = "utf-8"))
    f.close()


# In[ ]:


dir(os.open)

