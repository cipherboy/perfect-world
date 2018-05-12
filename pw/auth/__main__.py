import sys

import pw.auth

def __main__():
    yubikey = True
    totp = False

    if len(sys.argv) > 1 and sys.argv[1] == 'totp':
        totp = True
        yubikey = False

    if yubikey:
        print(pw.auth.yubikey.request())
    if totp:
        print(pw.auth.totp.request())



__main__()
