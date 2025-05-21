import hashlib
import datetime
from dateutil.relativedelta import relativedelta
import json
import os

realm = "@prototype.kdc".encode('utf-8')


def create_user(usern, passw, realm):
    username = usern.encode('utf-8')
    password = passw.encode('utf-8')
    salt = username + realm
    secret = hashlib.pbkdf2_hmac('sha256', password, salt, 100000)
    ct = datetime.datetime.now()
    valid_until = ct + relativedelta(years=1)
    
    info = {
        "username": usern, 
        "secret": secret.hex(), 
        "created": ct.isoformat(), 
        "valid-until":valid_until.isoformat()
    }

    if os.path.exists("database.json"):
        with open("database.json", 'r') as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = []
    else:
        data = []
    
    if not isinstance(data, list):
        raise ValueError("[-] database.json is not a list")
    data.append(info)

    with open("database.json", 'w') as f:
        json.dump(data, f, indent=2)

def main():
    print("Creating a principal is simple:D")
    usern = str(input("Input the users username: "))
    passw = input("Input the password: ")
    create_user(usern, passw, realm)
    print("User Created!")


main()
