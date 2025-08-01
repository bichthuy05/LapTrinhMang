import threading
from shared.protocol import encode_message, decode_message
from server.matchmaking import add_to_queue, remove_from_queue

class ClientHandler(threading.Thread):
    def __init__(self, conn, addr):
        super().__init__()
        self.conn = conn
        self.addr = addr
        self.username = None
        self.opponent = None
        self.running = True

    def run(self):
        print(f"[+] Client connected: {self.addr}")
        try:
            while self.running:
                data = self.conn.recv(1024)
                if not data:
                    break

                message = decode_message(data)
                self.handle_message(message)
        except Exception as e:
            print(f"[!] Error with {self.addr}: {e}")
        finally:
            remove_from_queue(self)
            self.conn.close()
            print(f"[-] Client disconnected: {self.addr}")

    def handle_message(self, message):
        msg_type = message.get("type")
        payload = message.get("payload")

        if msg_type == "join":
            self.username = payload.get("username")
            print(f"[Handler] Received JOIN from {self.username}")
            add_to_queue(self)
        elif msg_type == "move" and self.opponent:
            self.opponent.conn.sendall(encode_message({
                "type": "opponent_move",
                "payload": {"move": payload.get("move")}
            }))
        elif msg_type == "quit":
            self.running = False

    def send(self, msg_type, payload):
        self.conn.sendall(encode_message({
            "type": msg_type,
            "payload": payload
        }))