import unittest
from shared.protocol import Protocol
from shared.constants import MessageType

class TestProtocol(unittest.TestCase):
    def test_create_and_parse_message(self):
        # Test message không có data
        msg_type = MessageType.CONNECT
        json_str = Protocol.create_message(msg_type)
        parsed = Protocol.parse_message(json_str)
        
        self.assertEqual(parsed['type'], msg_type)
        self.assertEqual(parsed['data'], {})
        
        # Test message có data
        test_data = {'username': 'player1', 'score': 100}
        json_str = Protocol.create_message(MessageType.GAME_RESULT, test_data)
        parsed = Protocol.parse_message(json_str)
        
        self.assertEqual(parsed['type'], MessageType.GAME_RESULT)
        self.assertEqual(parsed['data'], test_data)
    
    def test_invalid_message(self):
        # Test message không hợp lệ
        with self.assertRaises(ValueError):
            Protocol.parse_message("invalid json")
        
        with self.assertRaises(ValueError):
            Protocol.parse_message('{"type": "invalid_type", "data": {}}')

if __name__ == '__main__':
    unittest.main()