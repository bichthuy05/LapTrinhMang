from shared.protocol import Protocol

class Matchmaker:
    def __init__(self):
        self.queue = []
        self.rooms = []

    def add_player(self, player):
        if player not in self.queue:
            self.queue.append(player)
        self.try_match()

    def remove_player(self, name):
        self.queue = [p for p in self.queue if p.name != name]
        for room in self.rooms:
            if room.has_player(name):
                room.remove_player(name)
                if len(room.players) < 2:
                    self.rooms.remove(room)

    def try_match(self):
        while len(self.queue) >= 2:
            p1 = self.queue.pop(0)
            p2 = self.queue.pop(0)
            
            try:
                # Kiểm tra kết nối còn hoạt động
                if not self._check_connection(p1.conn) or not self._check_connection(p2.conn):
                    continue
                    
                room = Room(p1, p2)
                self.rooms.append(room)
                print(f"🎉 Đã ghép cặp {p1.name} với {p2.name}")
                
                # Gửi thông báo cho cả 2 client
                self._notify_match_found(p1, p2)
                self._notify_match_found(p2, p1)
                
                room.start_game()
            except Exception as e:
                print(f"❌ Lỗi khi ghép cặp: {e}")

    def _notify_match_found(self, player, opponent):
        try:
            Protocol.send_message(player.conn, {
                'type': 'MATCH_FOUND',
                'opponent': opponent.name,
                'status': 'success'
            })
        except Exception as e:
            print(f"❌ Không thể gửi MATCH_FOUND cho {player.name}: {e}")

    def _check_connection(self, conn):
        """Kiểm tra kết nối còn hoạt động"""
        try:
            conn.settimeout(1.0)
            Protocol.send_message(conn, {'type': 'PING'})
            response = Protocol.unpack_message(conn)
            return response and response.get('type') == 'PONG'
        except:
            return False

    def find_room_by_player(self, name):
        for room in self.rooms:
            if room.has_player(name):
                return room
        return None
    
    def is_room_active(self, room_id):
        """Kiểm tra phòng còn hoạt động không"""
        return room_id in self.rooms and len(self.rooms[room_id].players) == 2
    
    def reset_player(self, player_name):
        """Reset player về trạng thái ban đầu"""
        if player_name in self.players:
            player = self.players[player_name]
            player.room_id = None
            player.score = 0
            self.add_player(player)  # Đưa về hàng đợi
    
    def cleanup_room(self, room_id):
        """Dọn dẹp phòng triệt để"""
        if room_id in self.rooms:
            # Gửi thông báo cho tất cả player còn kết nối
            for p in self.rooms[room_id].players:
                if p in self.players and self.is_player_connected(p):
                    try:
                        safe_send(self.players[p].conn, {
                            'type': 'ROOM_CLOSED',
                            'reason': 'Đối thủ mất kết nối'
                        })
                    except:
                        pass
            # Xóa phòng
            del self.rooms[room_id]


class Room:
    def __init__(self, p1, p2):
        self.player1 = p1.name
        self.player2 = p2.name
        self.players = {p1.name: p1, p2.name: p2}
        self.moves = {}
        self.room_id = f"{p1.name}_{p2.name}"
        self.replay_votes = {}  
    
    def get_opponent(self, player_name):
        """Lấy đối thủ của người chơi hiện tại"""
        if player_name not in self.players:
            return None
        return next((name for name in self.players if name != player_name), None)

    def is_player_connected(self, player_name):
        """Kiểm tra người chơi còn kết nối không"""
        if player_name not in self.players or not self.players[player_name]:
            return False
        try:
            Protocol.send_message(self.players[player_name].conn, {'type': 'PING'})
            return True
        except:
            return False
    
    def has_player(self, player_name):
        """Kiểm tra player có trong phòng không"""
        return player_name in self.players
    
    def receive_move(self, player_name, move):
        """Xử lý nước đi"""
        if not self.has_player(player_name):
            raise ValueError(f"Player {player_name} không có trong phòng")
        
        self.moves[player_name] = move
        print(f"📩 Nhận nước đi từ {player_name}: {move}")
        
        if len(self.moves) == 2:
            self.send_result()
    
    def send_result(self):
        """Gửi kết quả cho cả hai người chơi"""
        p1_move = self.moves.get(self.player1)
        p2_move = self.moves.get(self.player2)
        
        result_p1, result_p2 = get_result(p1_move, p2_move)
        
        for player, result in [(self.player1, result_p1), (self.player2, result_p2)]:
            if player in self.players:
                try:
                    safe_send(self.players[player].conn, {
                        'type': 'GAME_RESULT',
                        'opponent_move': p2_move if player == self.player1 else p1_move,
                        'result': result,
                        'message': 'Kết thúc trận đấu'
                    })
                except Exception as e:
                    print(f"⚠️ Lỗi gửi kết quả cho {player}: {e}")

    def remove_player(self, name):
        if name in self.players:
            del self.players[name]

    def start_game(self):
        self.moves.clear()
        self.replay_votes.clear()
        for name, player in self.players.items():
            opp_name = [n for n in self.players if n != name][0]
            
            # ĐẢM BẢO DỮ LIỆU GỬI ĐÚNG ĐỊNH DẠNG
            message = {
                "type": "match_found",
                "opponent": opp_name,
                "message": f"Đã tìm thấy đối thủ: {opp_name}",
                "status": "success"  # THÊM TRƯỜNG NÀY
            }
            safe_send(player.conn, message)

    def receive_replay_vote(self, name, vote):
        self.replay_votes[name] = vote
        if len(self.replay_votes) == 2:
            if all(self.replay_votes.values()):
                self.start_game()
            else:
                for player in self.players.values():
                    safe_send(player.conn, {"type": "end_game"})


def safe_send(conn, data):
    try:
        if conn and conn.fileno() != -1:
            # Gọi đúng cách với 1 tham số
            packed_data = Protocol.pack_message(data)
            conn.sendall(packed_data)
    except Exception as e:
        print(f"❌ Gửi thất bại: {e}")


def get_result(m1, m2):
    if m1 == m2:
        return "draw", "draw"
    win_map = {"rock": "scissors", "paper": "rock", "scissors": "paper"}
    if win_map[m1] == m2:
        return "win", "lose"
    return "lose", "win"


matchmaker = Matchmaker()