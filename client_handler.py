from player import Player
from matchmaking import add_to_queue

def handle_client(conn, addr):
    print(f"New connection from {addr}")
    player = Player(conn, addr)
    conn.sendall(b"Waiting for another player...\n")
    add_to_queue(player)
