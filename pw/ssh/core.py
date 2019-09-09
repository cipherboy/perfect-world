import subprocess

def gen_key(keyfile, keytype="rsa"):
    cmd = ['ssh-keygen', '-f', keyfile, '-N', '']
    if keytype == "rsa":
        cmd.extend(['-t', 'rsa', '-b', '2048'])
    elif keytype == 'ec':
        cmd.extend(['-t', 'ed25519'])
    else:
        print("Unknown keytype: " + keytype)
        return False

    p = subprocess.Popen(cmd, shell=False, stdin=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    p.wait(timeout=300)

    if p.returncode != 0:
        return False

    return True
