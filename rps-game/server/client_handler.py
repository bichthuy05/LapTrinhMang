from server.player import Player
from .matchmaking import matchmaker
from shared.protocol import Protocol
import socket
import time
import threading

waiting_queue = []
rooms = {}
lock = threading.Lock()

class Room:
    def __init__(self):
        self.players = {}  # danh sách người chơi trong phòng
        self.choices = {}
        self.lock = threading.Lock()
    
    def add_player(self, player):
        """Thêm người chơi vào phòng"""
        if player and player.name:
            self.players[player.name] = player
            return True
        return False
    
    def get_opponent(self, player_name):
        """Lấy đối thủ của người chơi hiện tại"""
        return next((name for name in self.players if name != player_name), None)
    
    def is_player_connected(self, player_name):
        """Kiểm tra người chơi còn kết nối không"""
        if player_name not in self.players:
            return False
        try:
            Protocol.send_message(self.players[player_name].conn, {'type': 'PING'})
            return True
        except:
            return False

def handle_client(conn, player, waiting_queue, active_games):
    player_name = None
    room = None
    
    try:
        # Nhận thông tin kết nối ban đầu
        msg = Protocol.unpack_message(conn)
        if not msg or msg.get('type') != 'CONNECT':
            return
            
        player_name = msg.get('name', 'Người chơi')
        print(f"🎮 {player_name} đã kết nối từ {conn.getpeername()}")

        # Gửi ACK để client không đóng kết nối
        safe_send(conn, {
            'type': 'CONNECT_ACK',
            'status': 'success',
            'you': player_name
        })


        # Thêm vào hàng đợi matchmaking
        with lock:
            # Tìm phòng có sẵn
            found_room = None
            found_room_id = None
            for room_id, r in rooms.items():
                if len(r['players']) < 2:
                    found_room = r
                    found_room_id = room_id
                    break
            
            if found_room:
                # Ghép cặp với người chơi đang chờ
                opponent_name = next(iter(found_room['players'].keys()))
                found_room['players'][player_name] = conn
                room = found_room
                
                # Gửi thông báo cho cả 2 người chơi
                safe_send(conn, {
                    'type': 'MATCH_FOUND',
                    'you': player_name,
                    'opponent': opponent_name,
                    'status': 'success'
                })
                safe_send(found_room['players'][opponent_name], {
                    'type': 'MATCH_FOUND',
                    'you': opponent_name,
                    'opponent': player_name,
                    'status': 'success'
                })
            else:
                # Tạo phòng mới
                room_id = f"room_{len(rooms)+1}"
                rooms[room_id] = {
                    'players': {player_name: conn},
                    'choices': {},
                    'lock': threading.Lock()
                }
                room = rooms[room_id]
                        
        # Xử lý các message từ client
        while True:
            msg = Protocol.unpack_message(conn)
            if not msg:
                break
                
            msg_type = msg.get('type')
            
            if msg_type == 'PLAYER_MOVE':
                move = msg.get('move')
                if not room:
                    continue
                    
                with room['lock']:
                    room['choices'][player_name] = move
                    
                    # Kiểm tra đủ 2 nước đi
                    if len(room['choices']) == 2:
                        players = list(room['players'].keys())
                        p1, p2 = players[0], players[1]
                        m1, m2 = room['choices'][p1], room['choices'][p2]
                        
                        # Xác định kết quả
                        result_p1, result_p2 = get_result(m1, m2)
                        if result_p1 == 'win':
                            winner = p1; loser = p2
                        elif result_p2 == 'win':
                            winner = p2; loser = p1
                        else:  # draw
                            winner = None
                        
                        # Gửi kết quả
                        safe_send(room['players'][p1], {
                            'type': 'GAME_RESULT',
                            'your_move': m1,
                            'opponent_move': m2,
                            'result': result_p1,
                            'winner': winner  # thêm thông tin người thắng (None nếu hòa)
                        })
                        safe_send(room['players'][p2], {
                            'type': 'GAME_RESULT',
                            'your_move': m2,
                            'opponent_move': m1,
                            'result': result_p2,
                            'winner': winner  # thêm thông tin người thắng (None nếu hòa)
                        })
                        
                        # Reset cho ván mới
                        room['choices'] = {}
            
            elif msg_type == 'DISCONNECT':
                break
                
    except ConnectionResetError:
        print(f"⚠️ {player_name} mất kết nối đột ngột")
    except Exception as e:
        print(f"⚠️ Lỗi với {player_name if player_name else 'client'}: {str(e)}")
    finally:
        room_to_remove = None
        with lock:
            for room_id, r in list(rooms.items()):
                if player_name in r['players']:
                    # Xóa player ra khỏi phòng
                    del r['players'][player_name]

                    if not r['players']:
                        # Nếu không còn ai thì đánh dấu xoá phòng
                        room_to_remove = room_id
                    else:
                        # Còn đối thủ thì báo
                        opponent_name = next(iter(r['players'].keys()))
                        opponent_conn = r['players'][opponent_name]

                        safe_send(opponent_conn, {
                            'type': 'OPPONENT_DISCONNECTED',
                            'message': f'{player_name} đã thoát trận'
                        })

                        # Cho đối thủ quay lại hàng chờ
                        waiting_queue.append((opponent_name, opponent_conn))

                    break  # đã xử lý xong

            if room_to_remove:
                del rooms[room_to_remove]

        try:
            conn.close()
            print(f"❌ {player_name} đã thoát")
        except:
            pass



def safe_send(conn, data):
    """Gửi dữ liệu an toàn qua socket"""
    try:
        if conn and conn.fileno() != -1:
            packed_data = Protocol.pack_message(data)
            if packed_data:
                conn.sendall(packed_data)
    except Exception as e:
        print(f"⚠️ Lỗi gửi dữ liệu: {e}")

def get_result(move1, move2):
    """Xác định kết quả từ 2 nước đi"""
    if move1 == move2:
        return 'draw', 'draw'
    win_map = {'rock': 'scissors', 'scissors': 'paper', 'paper': 'rock'}
    if win_map[move1] == move2:
        return 'win', 'lose'
    return 'lose', 'win'

def send_game_result(room, winner=None, reason=""):
    """Gửi kết quả đồng bộ cho cả hai người chơi"""
    for player in room.players:
        if matchmaker.is_player_connected(player):
            result = 'win' if player == winner else 'lose' if winner else 'draw'
            safe_send(matchmaker.players[player].conn, {
                'type': 'GAME_RESULT',
                'result': result,
                'message': reason or ('Bạn thắng!' if result == 'win' else 'Hòa!' if result == 'draw' else 'Bạn thua'),
                'opponent_move': room.moves.get(room.get_opponent(player)),
                'your_move': room.moves.get(player)
            })
    matchmaker.cleanup_room(room.room_id)


def send_heartbeat(conn):
    """Kiểm tra kết nối bằng heartbeat"""
    try:
        safe_send(conn, {'type': 'PING'})
        resp = Protocol.unpack_message(conn)
        return resp and resp.get('type') == 'PONG'
    except:
        return False

def cleanup_player(player_name, room_id):
    """Dọn dẹp khi người chơi ngắt kết nối"""
    print(f"⚠️ {player_name} đã ngắt kết nối")
    matchmaker.remove_player(player_name)
    
    # Xử lý phòng nếu có
    if room_id and room_id in matchmaker.rooms:
        room = matchmaker.rooms[room_id]
        opponent = room.get_opponent(player_name)
        
        if opponent and matchmaker.is_player_connected(opponent):
            try:
                safe_send(matchmaker.players[opponent].conn, {
                    'type': 'OPPONENT_DISCONNECTED',
                    'message': f'Đối thủ {player_name} đã thoát',
                    'room_id': room_id
                })
                matchmaker.reset_player(opponent)
            except Exception as e:
                print(f"⚠️ Lỗi thông báo cho {opponent}: {str(e)}")
        
        matchmaker.cleanup_room(room_id)

def handle_early_disconnect(player_name, room_id):
    """Xử lý đặc biệt cho ngắt kết nối sớm"""
    if not player_name:
        return
        
    print(f"🔴 {player_name} ngắt kết nối sớm")
    matchmaker.remove_player(player_name)
    
    if room_id and room_id in matchmaker.rooms:
        room = matchmaker.rooms[room_id]
        opponent = room.get_opponent(player_name)
        
        if opponent and matchmaker.is_player_connected(opponent):
            try:
                safe_send(matchmaker.players[opponent].conn, {
                    'type': 'OPPONENT_EARLY_DISCONNECT',
                    'message': 'Đối thủ mất kết nối trước khi bắt đầu',
                    'room_id': room_id
                })
                matchmaker.reset_player(opponent)
            except Exception as e:
                print(f"⚠️ Lỗi thông báo early disconnect: {str(e)}")
        
        matchmaker.cleanup_room(room_id)