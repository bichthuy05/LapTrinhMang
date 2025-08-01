import threading
from game_logic import determine_winner

waiting_players = []
lock = threading.Lock()

class GameRoom:
    def __init__(self, player1, player2):
        self.players = [player1, player2]

    def start_game(self):
        for player in self.players:
            player.conn.sendall(b"Send your move (rock/paper/scissors):\n")

        for player in self.players:
            try:
                move = player.conn.recv(1024).decode().strip()
                if move not in ['rock', 'paper', 'scissors']:
                    move = None
                player.choice = move
            except:
                player.choice = None

        result = determine_winner(self.players[0].choice, self.players[1].choice)
        msg = f"\nPlayer 1 chose {self.players[0].choice}, Player 2 chose {self.players[1].choice}.\n"

        if result == 0:
            msg += "Result: Draw!\n"
        elif result == 1:
            msg += "Player 1 wins!\n"
        elif result == 2:
            msg += "Player 2 wins!\n"
        else:
            msg += "Invalid moves. No winner.\n"

        for player in self.players:
            try:
                player.conn.sendall(msg.encode())
                player.conn.close()
            except:
                pass

def add_to_queue(player):
    with lock:
        waiting_players.append(player)
        if len(waiting_players) >= 2:
            p1 = waiting_players.pop(0)
            p2 = waiting_players.pop(0)
            room = GameRoom(p1, p2)
            threading.Thread(target=room.start_game).start()
