import json

def encode_message(message: dict) -> bytes:
    return json.dumps(message).encode('utf-8')

def decode_message(data: bytes) -> dict:
    return json.loads(data.decode('utf-8'))