import socket
import datetime
import json
import os

host = '127.0.0.1'
port = 6969
realm = 'prototype.kdc'

TGS_NAME = f'krbtgs/{realm}@{realm}'


tgs_session_key = os.urandom(32)
service_session_key = os.urandom(32)


def get_user_secretkey(username):
    if os.path.exists("database.json"):
        with open("database.json", 'r') as j:
            users = json.load(j)
            for user in users:
                if user['username'] == username:
                    return user['secret']
            else:
                print("[-] User not found :(")            
    else:
        print("[-] The database does not exist...")

def generate_TGT_message() # todo
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

