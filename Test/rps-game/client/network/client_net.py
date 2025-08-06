import socket
import threading
import time
from shared.protocol import Protocol
from shared.constants import SERVER_IP, SERVER_PORT, BUFFER_SIZE, MessageType

class ClientNetwork:
    def __init__(self, message_handler):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.message_handler = message_handler
        self.connected = False
        self.heartbeat_thread = None

    def connect(self, username: str) -> bool:
        """Kết nối tới server game"""
        try:
            self.client_socket.connect((SERVER_IP, SERVER_PORT))
            self.connected = True
            
            # Gửi message kết nối
            connect_msg = Protocol.create_message(
                MessageType.CONNECT,
                {'username': username}
            )
            self.send(connect_msg)
            
            # Bắt đầu thread nhận message
            receive_thread = threading.Thread(target=self.receive_messages)
            receive_thread.daemon = True
            receive_thread.start()
            
            # Bắt đầu thread heartbeat
            self.heartbeat_thread = threading.Thread(target=self.send_heartbeat)
            self.heartbeat_thread.daemon = True
            self.heartbeat_thread.start()
            
            return True
        except Exception as e:
            print(f"Connection error: {e}")
            return False

    def disconnect(self):
        """Ngắt kết nối với server"""
        if self.connected:
            disconnect_msg = Protocol.create_message(MessageType.DISCONNECT)
            self.send(disconnect_msg)
            self.connected = False
            self.client_socket.close()

    def send(self, message: str):
        """Gửi message tới server"""
        try:
            self.client_socket.send(message.encode('utf-8'))
        except Exception as e:
            print(f"Send error: {e}")
            self.disconnect()

    def send_move(self, move: int):
        """Gửi lựa chọn kéo/búa/bao tới server"""
        move_msg = Protocol.create_message(
            MessageType.PLAYER_MOVE,
            {'move': move}
        )
        self.send(move_msg)

    def receive_messages(self):
        """Nhận message từ server"""
        while self.connected:
            try:
                data = self.client_socket.recv(BUFFER_SIZE).decode('utf-8')
                if not data:
                    self.disconnect()
                    break
                
                # Xử lý message nhận được
                message = Protocol.parse_message(data)
                self.message_handler(message)
                
            except Exception as e:
                print(f"Receive error: {e}")
                self.disconnect()
                break

    def send_heartbeat(self):
        """Gửi heartbeat để giữ kết nối"""
        while self.connected:
            try:
                heartbeat_msg = Protocol.create_message(MessageType.HEARTBEAT)
                self.send(heartbeat_msg)
                time.sleep(5)  # Gửi mỗi 5 giây
            except Exception as e:
                print(f"Heartbeat error: {e}")
                self.disconnect()
                break