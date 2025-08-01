# server/rps_server.py
import socket
from server.client_handler import ClientHandler

HOST = '127.0.0.1'
PORT = 12345

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen()
    print(f"[Server] Listening on {HOST}:{PORT}")

    while True:
        conn, addr = server_socket.accept()
        handler = ClientHandler(conn, addr)
        handler.start()

if __name__ == "__main__":
    start_server()
