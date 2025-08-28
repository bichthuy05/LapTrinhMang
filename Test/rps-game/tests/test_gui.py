import unittest
from unittest.mock import patch, MagicMock, ANY
from client.gui.app import App
from client.gui.animations import LoadingAnimation
import os
from pathlib import Path

class TestGUI(unittest.TestCase):
    @patch('client.gui.app.ChoiceButton')  # Mock nút bấm
    @patch('client.gui.app.ClientNetwork')
    def test_app_initialization(self, mock_net, mock_button):
        """Test khởi tạo ứng dụng mà không cần ảnh thật"""
        # Mock phương thức tạo button
        mock_button.return_value = MagicMock()
        mock_net.return_value = MagicMock()
        # Tạo app và kiểm tra
        app = App()
        self.assertTrue(mock_net.called)
        self.assertTrue(mock_button.called)

        # Kiểm tra button được tạo đủ 3 lần
        self.assertEqual(mock_button.call_count, 3)
        mock_button.assert_any_call(ANY, 'rock', ANY)
        mock_button.assert_any_call(ANY, 'paper', ANY)
        mock_button.assert_any_call(ANY, 'scissors', ANY)

    def test_loading_animation(self):
        """Test animation loading"""
        mock_label = MagicMock()
        animation = LoadingAnimation(mock_label)
        animation.start()
        animation.stop()
        mock_label.config.assert_called()