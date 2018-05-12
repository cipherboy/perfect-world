import utils

import random
import requests
import secrets
import getpass
import hashlib, hmac, base64

def sign_args(args, api_key):
    data = '&'.join([key + "=" + args[key] for key in sorted(args.keys())])
    key = base64.b64decode(bytes(api_key, 'ascii'))
    args_hmac = hmac.new(key, bytes(data, 'ascii'), hashlib.sha1)
    return base64.b64encode(args_hmac.digest()).decode('ascii')

def handle_response_yubikey(data):
    r_obj = {}
    h = None
    for line in data.split("\r\n"):
        if line == "" or not '=' in line:
            continue

        i = line.index("=")
        key = line[0:i]
        value = line[i+1:]
        if key != 'h':
            r_obj[key] = value
        else:
            h = value

    return r_obj, h

def check_otp_yubikey(url, acct_id, api_key, token):
    nonce = ''.join(random.SystemRandom().choices("abcdefghijklmnopqrstuvwxyz0123456789", k=32))
    data = {'id': acct_id, 'otp': token, 'nonce': nonce}
    data['h'] = sign_args(data, api_key)

    r = requests.get(url, params=data)

    r_obj, h = handle_response_yubikey(r.text)
    if sign_args(r_obj, api_key) != h:
        return False

    return r_obj['status'] == 'OK'

def yubikey():
    cfg = utils.load_config('/home/cipherboy/.pw/auth/yubikey.json')
    token = getpass.getpass("YubiKey OTP: ")

    for device in cfg['devices']:
        l = len(device)
        if token[0:l] == device:
            for provider in cfg['providers']:
                if check_otp_yubikey(provider['url'], provider['id'], provider['api_key'], token):
                    return True

    return False


if __name__ == "__main__":
    print(yubikey())

