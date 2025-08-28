import unittest
from unittest.mock import patch, MagicMock
from client.network.client_net import ClientNetwork
from shared.protocol import Protocol
from shared.constants import MessageType

class TestClientNetwork(unittest.TestCase):
    def setUp(self):
        self.mock_handler = MagicMock()
        self.socket_patcher = patch('socket.socket')
        self.mock_socket = self.socket_patcher.start()
        self.mock_sock_instance = MagicMock()
        self.mock_socket.return_value = self.mock_sock_instance
        self.client = ClientNetwork(self.mock_handler)

    def tearDown(self):
        self.socket_patcher.stop()
        if hasattr(self.client, 'disconnect'):
            self.client.disconnect()

    def test_connect_success(self):
        """Test kết nối thành công"""
        self.mock_sock_instance.connect.return_value = None
        result = self.client.connect("test_player")
        self.assertTrue(result)
        self.assertTrue(self.client.connected)
        self.mock_sock_instance.connect.assert_called_once_with(('127.0.0.1', 5555))

    def test_send_message(self):
        """Test gửi message"""
        self.mock_sock_instance.connect.return_value = None
        self.client.connect("test_player")
        
        # Mock thành công gửi message
        self.mock_sock_instance.send.return_value = None
        
        result = self.client.send_move('rock')
        self.assertTrue(result)
        
        # Kiểm tra message được gửi
        self.mock_sock_instance.send.assert_called_once()

    def test_receive_message(self):
        """Test nhận message"""
        self.mock_sock_instance.connect.return_value = None
        self.client.connect("test_player")
        
        # Mock data nhận được
        test_msg = Protocol.create_message(
            MessageType.GAME_RESULT,
            {'result': 'win'}
        )
        self.mock_sock_instance.recv.side_effect = [
            test_msg.encode(),
            b''  # Điều kiện dừng
        ]
        
        self.client._receive_messages()
        self.mock_handler.assert_called_once()

if __name__ == '__main__':
    unittest.main(verbosity=2)