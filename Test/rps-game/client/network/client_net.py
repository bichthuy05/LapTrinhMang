import socket
import json
import threading
from shared.constants import SERVER_IP, SERVER_PORT

class ClientNetwork:
    def __init__(self, message_handler):
        self.socket = None
        self.connected = False
        self.message_handler = message_handler
        self.player_name = None
        self.opponent_name = None


    def connect(self, username, timeout=5):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.settimeout(timeout)
            self.socket.connect((SERVER_IP, SERVER_PORT))

            connect_msg = json.dumps({
                "name": username,
                "type": "CONNECT"
            }).encode('utf-8')

            header = len(connect_msg).to_bytes(4, byteorder='big')
            self.socket.sendall(header + connect_msg)

            self.connected = True
            threading.Thread(target=self._receive_messages, daemon=True).start()
            return True
        except Exception as e:
            print(f"Connection error: {e}")
            return False

    def _receive_messages(self):
        while self.connected:
            try:
                header = self.socket.recv(4)
                if not header:
                    break
                length = int.from_bytes(header, byteorder='big')
                data = self.socket.recv(length)
                if not data:
                    break
                msg = json.loads(data.decode('utf-8'))
                # 👉 Lưu tên khi nhận được MATCH_FOUND
                if msg.get("type") == "MATCH_FOUND":
                    self.player_name = msg.get("you")
                    self.opponent_name = msg.get("opponent")
                    print(f"🔗 Ghép cặp: Bạn = {self.player_name}, Đối thủ = {self.opponent_name}")

                if self.message_handler:
                    self.message_handler(msg)
            except Exception as e:
                print(f"Receive error: {e}")
                break

    def send_move(self, move):
        if not self.connected:
            raise ConnectionError("Not connected to server")
        msg = json.dumps({"type": "PLAYER_MOVE", "move": move}).encode('utf-8')
        header = len(msg).to_bytes(4, byteorder='big')
        self.socket.sendall(header + msg)

    def send_replay_vote(self, vote):
        if not self.connected:
            raise ConnectionError("Not connected to server")
        msg = json.dumps({"type": "REPLAY_VOTE", "vote": vote}).encode('utf-8')
        header = len(msg).to_bytes(4, byteorder='big')
        self.socket.sendall(header + msg)

    def disconnect(self):
        try:
            if self.socket:
                msg = json.dumps({"type": "DISCONNECT"}).encode('utf-8')
                header = len(msg).to_bytes(4, byteorder='big')
                self.socket.sendall(header + msg)
                self.socket.close()
        except:
            pass
        finally:
            self.connected = False
            self.socket = None