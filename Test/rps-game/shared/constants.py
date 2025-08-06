from enum import Enum, auto

class MessageType(Enum):
    """Các loại message trong game"""
    CONNECT = auto()
    DISCONNECT = auto()
    PLAYER_READY = auto()
    PLAYER_MOVE = auto()
    GAME_RESULT = auto()
    MATCH_FOUND = auto()
    ERROR = auto()
    HEARTBEAT = auto()

# Cấu hình mạng
SERVER_IP = '127.0.0.1'
SERVER_PORT = 5555
BUFFER_SIZE = 4096

# Game constants
class Move(Enum):
    ROCK = 0
    PAPER = 1
    SCISSORS = 2

class Result(Enum):
    WIN = auto()
    LOSE = auto()
    DRAW = auto()
    INVALID = auto()