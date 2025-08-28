import unittest
from unittest.mock import MagicMock
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from server.matchmaking import add_to_queue, GameRoom
from server.player import Player


class TestMatchmaking(unittest.TestCase):
    def setUp(self):
        self.mock_conn1 = MagicMock()
        self.mock_conn2 = MagicMock()
        self.player1 = Player(self.mock_conn1, ('127.0.0.1', 12345))
        self.player2 = Player(self.mock_conn2, ('127.0.0.1', 12346))
    
    def test_game_room(self):
        """Test logic phòng game"""
        room = GameRoom(self.player1, self.player2)
        self.player1.choice = 'rock'
        self.player2.choice = 'scissors'
        room.start_game()
        
        # Verify gửi kết quả
        self.mock_conn1.sendall.assert_called()
        self.mock_conn2.sendall.assert_called()