import utils

import pyotp
import qrcode
import getpass

def enroll_totp(name):
    secret = pyotp.random_base32()
    return secret, pyotp.totp.TOTP(secret).provisioning_uri(name, issuer_name="perfect-world")

def gen_qrcode(secret, name, filename):
    uri = pyotp.totp.TOTP(secret).provisioning_uri(name, issuer_name="perfect-world")
    img = qrcode.make(data=uri)
    img.save(filename)

def check_otp_totp(secret, token):
    totp = pyotp.TOTP(secret)
    return totp.verify(token)

def totp():
    cfg = utils.load_config('/home/cipherboy/.pw/auth/totp.json')
    token = getpass.getpass("TOTP: ")

    for device in cfg['devices']:
        if check_otp_totp(device['secret'], token):
            return True

    return False


if __name__ == "__main__":
    print(totp())

