import socket
import datetime
import json

host = '127.0.0.1'
port = 6969

def get_tgt(asreq):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        print("[+] Connected to the AS")
        s.sendall(asreq)
        print("[*] Sending the message...")
        tgt = s.recv(1024)
        print("[+] Recieved TGT!")
        print(tgt)

def first_m_gen():
    username = input("Username: ")
    service = input("Which service do you want to authenticate to: ")
    timestamp = datetime.datetime.now()
    lifetime = 1

    print("[*] Generating First Message from your input")

    message = {
        "username": username,
        "service": service,
        "timestamp": timestamp.isoformat(),
        "lifetime": lifetime
        }
    print("[+] Message Generated!")
    asreq = json.dumps(message).encode('utf-8')
    print("[*] Preparing to send the message to AS")
    get_tgt(asreq)

first_m_gen()