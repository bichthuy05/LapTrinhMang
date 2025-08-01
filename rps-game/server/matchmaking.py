import threading

waiting_queue = []
lock = threading.Lock()

def add_to_queue(client_handler):
    with lock:
        waiting_queue.append(client_handler)
        print(f"[Queue] Added {client_handler.username}")
    try_match()

def remove_from_queue(client_handler):
    with lock:
        if client_handler in waiting_queue:
            waiting_queue.remove(client_handler)
            print(f"[Queue] Removed {client_handler.username}")

def try_match():
    with lock:
        if len(waiting_queue) >= 2:
            player1 = waiting_queue.pop(0)
            player2 = waiting_queue.pop(0)

            player1.opponent = player2
            player2.opponent = player1

            player1.send("match_found", {"opponent": player2.username})
            player2.send("match_found", {"opponent": player1.username})

            print(f"[Match] {player1.username} vs {player2.username}")