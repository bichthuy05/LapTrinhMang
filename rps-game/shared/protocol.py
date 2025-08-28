import json
import struct

class Protocol:
    @staticmethod
    def pack_message(data):
        """Đóng gói dữ liệu thành chuỗi bytes để gửi qua socket"""
        try:
            json_data = json.dumps(data).encode('utf-8')
            header = struct.pack('!I', len(json_data))
            return header + json_data
        except Exception as e:
            print(f"Lỗi đóng gói tin nhắn: {e}")
            return None

    @staticmethod
    def unpack_message(conn):
        """Giải mã dữ liệu nhận từ socket"""
        try:
            # Nhận 4 byte đầu tiên (độ dài tin nhắn)
            raw_len = Protocol._recv_all(conn, 4)
            if not raw_len:
                return None
                
            msg_len = struct.unpack('!I', raw_len)[0]
            data = Protocol._recv_all(conn, msg_len)
            if not data:
                return None
                
            return json.loads(data.decode('utf-8'))
        except Exception as e:
            print(f"Lỗi giải mã tin nhắn: {e}")
            return None

    @staticmethod
    def _recv_all(conn, length):
        """Nhận đủ số byte theo yêu cầu"""
        data = b""
        while len(data) < length:
            packet = conn.recv(length - len(data))
            if not packet:
                return None
            data += packet
        return data