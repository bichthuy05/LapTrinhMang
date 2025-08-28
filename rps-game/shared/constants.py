from enum import Enum, auto

class MessageType(Enum):
    """Các loại message trong game"""
    CONNECT = auto()        # Kết nối đến server
    DISCONNECT = auto()     # Ngắt kết nối
    PLAYER_READY = auto()   # Sẵn sàng chơi
    REQUEST_MOVE = auto()   # Server yêu cầu người chơi chọn nước đi  ✅ THÊM DÒNG NÀY
    PLAYER_MOVE = auto()    # Gửi nước đi
    GAME_RESULT = auto()    # Kết quả game
    MATCH_FOUND = auto()    # Đã tìm thấy đối thủ
    ERROR = auto()          # Lỗi
    HEARTBEAT = auto()      # Giữ kết nối
    PLAYER_LEFT = auto()    # Đối thủ thoát game

# Cấu hình mạng
SERVER_IP = '127.0.0.1'
SERVER_PORT = 5555
RECONNECT_DELAY = 5  # Thời gian chờ kết nối lại (giây)

# Game constants
class Move(Enum):
    ROCK = 'rock'
    PAPER = 'paper'
    SCISSORS = 'scissors'

class Result(Enum):
    WIN = 'win'
    LOSE = 'lose'
    DRAW = 'draw'
    INVALID = 'invalid'
    OPPONENT_LEFT = 'opponent_left'  # Đối thủ thoát game
