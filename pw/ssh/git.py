from github import Github

def user_context(username, password):
    g = Github(username, password)
    return g.get_user()

def grant_github(username, password, keyname, keyfile):
    u = user_context(username, password)

    key = open(keyfile).read()
    key_obj = u.create_key(keyname, key)

    return key_obj.id

def revoke_github(username, password, kid=None, keyname=None):
    assert(kid != None or keyname != None)
    assert(kid == None or keyname == None)

    if kid != None:
        assert(type(kid) == int)
    if keyname != None:
        assert(type(keyname) == str)

    u = user_context(username, password)

    found = 0
    if keyname == None:
        for pkey_obj in u.get_keys():
            if pkey_obj.title == keyname:
                kid = pkey_obj
                found += 1

    if found > 1:
        print("Refusing to revoke all keys with name: " + keyname)
        return False

    if kid == None:
        print("Key not found: " + keyname)
        return False

    key_obj = u.get_key(kid)
    key_obj.delete()

    return True
