import json
from enum import Enum
from shared.constants import MessageType

class Protocol:
    @staticmethod
    def create_message(msg_type: MessageType, data: dict = None) -> str:
        """
        Tạo message theo định dạng JSON
        :param msg_type: Loại message (từ MessageType)
        :param data: Dữ liệu kèm theo (dict)
        :return: Chuỗi JSON
        """
        message = {
            'type': msg_type.value,
            'data': data if data else {}
        }
        return json.dumps(message)
    
    @staticmethod
    def parse_message(json_str: str) -> dict:
        """
        Phân tích message JSON từ server
        :param json_str: Chuỗi JSON nhận được
        :return: Dictionary chứa thông tin message
        """
        try:
            message = json.loads(json_str)
            return {
                'type': MessageType(message['type']),
                'data': message.get('data', {})
            }
        except (json.JSONDecodeError, ValueError) as e:
            raise ValueError(f"Invalid message format: {e}")