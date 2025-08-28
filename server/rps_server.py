import socket
import threading
from server.client_handler import handle_client
   
waiting_queue = []
rooms = {}
# Địa chỉ và cổng của server
HOST = "127.0.0.1"
PORT = 5555

def start_server():
    threads = []
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((HOST, PORT))
        server_socket.listen()
        
        print(f"🖥 Server đang chạy tại {HOST}:{PORT}")
        print("Nhấn Ctrl+C để dừng server...")

        try:
            while True:
                conn, addr = server_socket.accept()
                print(f"🎮 Kết nối mới từ {addr}")
                
                # Tạo thread riêng cho mỗi client
                client_thread = threading.Thread(
                    target=handle_client,
                    args=(conn, addr, waiting_queue, rooms),
                    daemon=True
                ).start()
            
        except KeyboardInterrupt:
            print("\n🛑 Đang dừng server...")
            # Đóng tất cả kết nối
            for thread in threads:
                thread.join(timeout=1)
        finally:
            print("✅ Server đã dừng")

if __name__ == "__main__":
    start_server()