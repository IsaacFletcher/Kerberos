import socket
import datetime
import json
import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad,unpad
import base64

host = '127.0.0.1'
port = 6969
realm = 'prototype.kdc'

TGS_NAME = f'krbtgs/{realm}@{realm}'
iv = 'testinitvectorAB'

tgs_session_key = os.urandom(32)
service_session_key = os.urandom(32)



def get_user_secretkey(username):
    if os.path.exists("database.json"):
        with open("database.json", 'r') as j:
            users = json.load(j)
            for user in users:
                if user['username'] == username:
                    client_sec = user['secret']
                    return client_sec
            else:
                print("[-] User not found :(")
    else:
        print("[-] The database does not exist...")

def generate_TGT_message(username, client_ip):
    # we need two messages
    # first is the one we will encrypt with clients secret key and put out generated TGS SK in
    # the second is the one designated for the TGS, which we will encrypt with TGS's secret key.
    # The first message (we will call it a from now on) contains the following.
    client_enc = {
            "TGS-Principal-Name": TGS_NAME,
            "Timestamp": datetime.datetime.now(),
            "Lifetime": 1,
            "TGS-SK": tgs_session_key
            }
    # Next the second message (we will call it b) contains
    tgs_enc = {
            "username": username,
            "TGS-Principal-Name": TGS_NAME,
            "Timestamp": datetime.datetime.now(),
            "UserIP": client_ip,
            "Lifetime": 1,
            "TGS-SK": tgs_session_key
            }

def encrypt_ab(client_enc, client_sec, tgs_enc, tgs, iv):
    key_c = client_sec.encode('utf-8')
    data_c = client_enc.encode('utf-8')
    data = pad(data_c.encode(),16)
    cipher = AES.new(key_c, AES.MODE_CBC, iv)
    return base64.b64encode(cipher.encrypt(data))

def socket_communication():
    while True:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((host, port))
            s.listen()
            conn, addr = s.accept()
            with conn:
                print(f"[+] Connection Established with {addr}")
                while True:
                    data = conn.recv(1024)
                    if not data:
                        break
                    recieved = data.decode('utf-8')
                    parsed = json.loads(recieved)
                    username = parsed['username']
                    get_user_secretkey(username)
