from passwordhelper import PasswordHelper
import sys

PH = PasswordHelper()

password = '123456'

salt = PH.get_salt()

hashWithSalt = PH.get_hash(password.encode('utf-8') + salt)

print("password = {0}".format(password))
print("salt = {0}".format(salt))
print("Hash with salt = {0}".format(hashWithSalt)) 