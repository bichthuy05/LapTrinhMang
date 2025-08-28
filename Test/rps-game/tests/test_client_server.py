# tests/test_client_server.py
import unittest
from unittest.mock import patch, MagicMock
import socket

class TestClientServer(unittest.TestCase):
    @patch('socket.socket')
    def test_client_connection(self, mock_socket):
        """Test kết nối client sử dụng mock socket"""
        # 1. Setup mock
        mock_conn = MagicMock()
        mock_socket.return_value = mock_conn
        
        # 2. Giả lập kết nối thành công
        mock_conn.connect.return_value = None
        
        # 3. Gọi hàm kết nối thực tế từ code của bạn
        # Ví dụ: hàm connect() từ client_net.py
        from client.network.client_net import ClientNetwork
        client = ClientNetwork()
        result = client.connect("test_player")
        
        # 4. Kiểm tra kết quả
        self.assertTrue(result)
        mock_conn.connect.assert_called_once_with(('127.0.0.1', 5555))  # Kiểm tra kết nối tới đúng host/port