import socket
import json

HOST = '127.0.0.1'
PORT = 12345

def encode_message(message: dict) -> bytes:
    return json.dumps(message).encode('utf-8')

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(encode_message({
        "type": "join",
        "payload": {"username": "Player1"}
    }))