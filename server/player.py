class Player:
    def __init__(self, conn, addr):
        self.conn = conn
        self.addr = addr
        self.name = ""  # Thêm trường name
        self.choice = None
        self.score = 0  # Thêm trường score nếu cần