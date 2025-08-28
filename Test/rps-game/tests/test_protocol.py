import unittest
import sys
from pathlib import Path

# Fix import path
sys.path.insert(0, str(Path(__file__).parent.parent))

from shared.protocol import Protocol
from shared.constants import MessageType, Move, Result

class TestProtocol(unittest.TestCase):
    def setUp(self):
        self.test_data = {
            'CONNECT': {'username': 'player1'},
            'PLAYER_MOVE': {'move': Move.ROCK.value},
            'GAME_RESULT': {'result': Result.WIN.value}
        }

    def test_message_creation(self):
        # Test tất cả loại message
        for msg_type in MessageType:
            with self.subTest(msg_type=msg_type):
                msg = Protocol.create_message(msg_type, self.test_data.get(msg_type.name.lower(), {}))
                self.assertIsInstance(msg, str)
                self.assertIn('"type":', msg)
                
    def test_message_parsing(self):
        test_data = {
        'PLAYER_MOVE': {'choice': 'rock'},  # Sử dụng tên message type thực tế
        'GAME_RESULT': {'result': 'win', 'opponent_move': 'scissors'},
        # Thêm các message type khác
        }

        # Test roundtrip (create -> parse)
        for msg_type, data in self.test_data.items():
            with self.subTest(msg_type=msg_type):
                enum_type = getattr(MessageType, msg_type)
                original = Protocol.create_message(enum_type, data)
                parsed = Protocol.parse_message(original)
                self.assertEqual(parsed['type'].name, msg_type)
                self.assertEqual(parsed['data'], data)

    def test_edge_cases(self):
        # Test empty message
        empty_msg = Protocol.create_message(MessageType.HEARTBEAT)
        self.assertEqual(Protocol.parse_message(empty_msg)['data'], {})

        # Test invalid cases
        with self.assertRaises(ValueError):
            Protocol.parse_message("invalid_json")

if __name__ == '__main__':
    unittest.main(verbosity=2)