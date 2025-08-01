import socket
import threading
from client_handler import handle_client

HOST = '0.0.0.0'
PORT = 5555

# Tạo socket toàn cục để có thể đóng lại từ luồng khác
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def accept_clients():
    while True:
        try:
            conn, addr = server_socket.accept()
            threading.Thread(target=handle_client, args=(conn, addr)).start()
        except OSError:
            break  # Socket bị đóng, thoát vòng lặp

def wait_for_exit_command():
    while True:
        cmd = input()
        if cmd.strip().lower() == "/exit":
            print("[!] Shutting down server...")
            server_socket.close()
            break

def start_server():
    print(f"Server starting on {HOST}:{PORT}")
    server_socket.bind((HOST, PORT))
    server_socket.listen()

    # Luồng 1: nhận client
    threading.Thread(target=accept_clients, daemon=True).start()

    # Luồng 2: chờ lệnh /exit từ admin
    wait_for_exit_command()

if __name__ == "__main__":
    start_server()
