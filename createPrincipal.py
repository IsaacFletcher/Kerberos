import hashlib
import datetime
from dateutil.relativedelta import relativedelta

realm = "@prototype.kdc".encode('utf-8')


def create_user(usern, passw, realm):
    username = usern.encode('utf-8')
    password = passw.encode('utf-8')
    salt = username + realm
    secret = hashlib.pbkdf2_hmac('sha256', password, salt, 100000)
    ct = datetime.datetime.now()
    valid_until = ct + relativedelta(years=1)
    with open('database.json', 'a') as f:
        f.write(f'{{"username": "{usern}", "secret": "{secret.hex()}, "created": {ct}, "valid-until": {valid_until}"}}\n')

def main():
    print("Creating a principal is simple:D")
    usern = str(input("Input the users username: "))
    passw = input("Input the password: ")
    create_user(usern, passw, realm)
    print("User Created!")


main()