import tkinter as tk
from tkinter import messagebox, simpledialog
from PIL import Image, ImageTk
import os, socket, threading, random, time
from shared.protocol import Protocol

HOST, PORT = "127.0.0.1", 5555

class App:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Rock Paper Scissors Game")
        self.window.geometry("600x500")
        self.window.configure(bg="white")

        self.mode = None
        self.player_name = None
        self.opponent_name = None
        self.client_socket = None
        self.player_move = None
        self.opponent_move = None
        self.keep_running = True

        self.images = {}
        self.load_images()
        self.setup_ui()

    # ===== Load hình =====
    def load_images(self):
        base_path = os.path.join(os.path.dirname(__file__), "..", "assets")
        for choice in ["rock", "paper", "scissors"]:
            img_path = os.path.join(base_path, f"{choice}.png")
            img = Image.open(img_path).resize((100, 100))
            self.images[choice] = ImageTk.PhotoImage(img)

    # ===== Setup UI =====
    def setup_ui(self):
        self.label_info = tk.Label(self.window, text="Chọn chế độ chơi:", font=("Arial", 18, "bold"), bg="white")
        self.label_info.pack(pady=10)

        self.btn_demo = tk.Button(self.window, text="🎲 Demo (Ngẫu nhiên)", font=("Arial", 14),
                                  bg="#4CAF50", fg="white", command=lambda: self.start_game("demo"))
        self.btn_demo.pack(pady=5)

        self.btn_multi = tk.Button(self.window, text="👥 2 Người Chơi", font=("Arial", 14),
                                   bg="#2196F3", fg="white", command=lambda: self.start_game("multi"))
        self.btn_multi.pack(pady=5)

        self.frame_buttons = tk.Frame(self.window, bg="white")
        self.frame_buttons.pack(pady=10)

        self.btn_rock = tk.Button(self.frame_buttons, image=self.images["rock"], command=lambda: self.make_choice("rock"))
        self.btn_paper = tk.Button(self.frame_buttons, image=self.images["paper"], command=lambda: self.make_choice("paper"))
        self.btn_scissors = tk.Button(self.frame_buttons, image=self.images["scissors"], command=lambda: self.make_choice("scissors"))

        self.btn_rock.grid(row=0, column=0, padx=5)
        self.btn_paper.grid(row=0, column=1, padx=5)
        self.btn_scissors.grid(row=0, column=2, padx=5)

        self.enable_choice(False)

        self.label_player = tk.Label(self.window, text="Bạn:", font=("Arial", 14), bg="white")
        self.label_player.pack()
        self.label_player_img = tk.Label(self.window, bg="white")
        self.label_player_img.pack()

        self.label_opponent = tk.Label(self.window, text="Đối thủ:", font=("Arial", 14), bg="white")
        self.label_opponent.pack()
        self.label_opponent_img = tk.Label(self.window, bg="white")
        self.label_opponent_img.pack()

        self.label_result = tk.Label(self.window, text="", font=("Arial", 16), bg="white")
        self.label_result.pack(pady=10)

    # ===== Bắt đầu game =====
    def start_game(self, mode):
        self.mode = mode
        self.player_name = simpledialog.askstring("Tên người chơi", "Nhập tên của bạn:")
        if not self.player_name:
            messagebox.showerror("Lỗi", "Phải nhập tên để chơi!")
            return

        if mode == "demo":
            self.label_info.config(text=f"Chào {self.player_name} (Demo)", fg="green")
        else:
            self.label_info.config(text=f"Chào {self.player_name} (2 Người Chơi)", fg="blue")
            self.connect_server()

        self.enable_choice(True)
        self.btn_demo.config(state=tk.DISABLED)
        self.btn_multi.config(state=tk.DISABLED)

    def enable_choice(self, enable=True):
        state = tk.NORMAL if enable else tk.DISABLED
        self.btn_rock.config(state=state)
        self.btn_paper.config(state=state)
        self.btn_scissors.config(state=state)

    # ===== Chọn nước đi =====
    def make_choice(self, choice):
        self.player_move = choice
        self.label_player_img.config(image=self.images[choice])
        self.label_player_img.image = self.images[choice]
        self.enable_choice(False)

        if self.mode == "demo":
            opp_choice = random.choice(["rock", "paper", "scissors"])
            self.label_opponent_img.config(image=self.images[opp_choice])
            self.label_opponent_img.image = self.images[opp_choice]
            self.show_result(self.player_move, opp_choice)
            self.ask_replay()
        else:
            msg = Protocol.pack_message({"type": "PLAYER_MOVE", "move": choice})
            try:
                self.client_socket.sendall(msg)
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không gửi được dữ liệu: {e}")

    # ===== Hiển thị kết quả demo =====
    def show_result(self, player, opponent):
        if player == opponent:
            result = "HÒA!"
        elif (player == "rock" and opponent == "scissors") or \
             (player == "paper" and opponent == "rock") or \
             (player == "scissors" and opponent == "paper"):
            result = "BẠN THẮNG!"
        else:
            result = "BẠN THUA!"
        self.label_result.config(text=result)

    # ===== Kết nối server =====
    def connect_server(self):
        try:
            self.client_socket = socket.socket()
            self.client_socket.connect((HOST, PORT))

            connect_msg = {"type": "CONNECT", "name": self.player_name, "version": "1.0"}
            self.client_socket.sendall(Protocol.pack_message(connect_msg))

            ack = Protocol.unpack_message(self.client_socket)
            if not ack or ack.get("type") != "CONNECT_ACK" or ack.get("status") != "success":
                raise ConnectionError(ack.get('message', 'Kết nối bị từ chối'))

            # (tuỳ chọn) đồng bộ lại tên chính xác server trả về
            self.player_name = ack.get("you", self.player_name)


            threading.Thread(target=self.listen_server, daemon=True).start()
            threading.Thread(target=self.heartbeat, daemon=True).start()
            self.label_info.config(text="Đang tìm đối thủ...")

        except Exception as e:
            messagebox.showerror("Lỗi", f"Kết nối thất bại: {str(e)}")
            self.btn_multi.config(state=tk.NORMAL)

    # ===== Gửi heartbeat =====
    def heartbeat(self):
        while self.keep_running and self.client_socket:
            try:
                self.client_socket.sendall(Protocol.pack_message({"type": "HEARTBEAT"}))
                time.sleep(2)
            except:
                break

    # ===== Nghe server =====
    def listen_server(self):
        while self.keep_running and self.client_socket:
            try:
                data = Protocol.unpack_message(self.client_socket)
                if not data:
                    continue

                msg_type = data.get("type")
                
                if msg_type == "MATCH_FOUND":
                    self.player_name = data.get("you", self.player_name)
                    self.opponent_name = data.get("opponent")

                    self.window.after(0, lambda: self.label_info.config(
                        text=f"🎉 {self.player_name} đã được ghép cặp với {self.opponent_name}"
                    ))
                    self.enable_choice(True)


                elif msg_type == "GAME_RESULT":
                    your_move = data["your_move"]
                    opp_move = data["opponent_move"]
                    result = data["result"]
                    winner = data.get("winner")
                    # Sử dụng after để cập nhật giao diện
                    self.window.after(0, lambda: self._show_result(your_move, opp_move, result, winner))
                    

                elif msg_type == "OPPONENT_DISCONNECTED":
                    def handle_disconnect():
                        messagebox.showinfo(
                            "Thông báo",
                            data.get("message", "Đối thủ đã thoát game")
                        )
                        self._reset_to_waiting_mode()

                    self.window.after(0, handle_disconnect)


                elif msg_type == "REPLAY_RESPONSE":
                    if data.get("status") == "success":
                        self.window.after(0, lambda: self.label_info.config(
                            text=f"Đang đấu với {self.opponent_name}"
                        ))
                    else:
                        self.window.after(0, lambda: self.label_info.config(
                            text="Đang tìm đối thủ mới..."
                        ))

                else:
                    # fallback xử lý các loại message khác
                    self.window.after(0, lambda: self.handle_server_message(data))

            except ConnectionResetError:
                self.window.after(0, self._handle_disconnect)
                break
            except Exception as e:
                print(f"Lỗi nhận dữ liệu: {e}")
                self.window.after(0, self._handle_disconnect)
                break

    def _update_match_ui(self):
        """Cập nhật UI khi tìm thấy đối thủ"""
        self.label_info.config(text=f"Đối thủ: {self.opponent_name}")
        self.enable_choice(True)

    def handle_game_result(self, data):
        """Xử lý và hiển thị kết quả game"""
        # Cập nhật nước đi
        self.label_opponent_img.config(image=self.images[data.get("opponent_move")])
        self.label_opponent_img.image = self.images[data.get("opponent_move")]
        
        # Hiển thị kết quả
        result = data.get("result")
        message = data.get("message", "")
        
        if result == "win":
            self.label_result.config(text=f"BẠN THẮNG!\n{message}")
        elif result == "lose":
            self.label_result.config(text=f"BẠN THUA!\n{message}")
        else:
            self.label_result.config(text=f"HÒA!\n{message}")
        
        # Cho phép chơi lại
        self.ask_replay()

    def _reset_to_waiting_mode(self):
        """Reset về trạng thái chờ"""
        self.opponent_name = None
        self.player_move = None
        self.label_info.config(text="Đang tìm đối thủ mới...")
        self.label_result.config(text="")
        self.label_player_img.config(image="")
        self.label_opponent_img.config(image="")
        self.enable_choice(False)

        # ===== Cập nhật kết quả từ server =====
    def _show_result(self, your_move, opp_move, result, winner):
        self.label_player_img.config(image=self.images[your_move])
        self.label_player_img.image = self.images[your_move]
        self.label_opponent_img.config(image=self.images[opp_move])
        self.label_opponent_img.image = self.images[opp_move]

        if result == "win":
            self.label_info.config(text=f"Bạn thắng! (Người thắng: {self.player_name})")
        elif result == "lose":
            self.label_info.config(text=f"Bạn thua! (Người thắng: {self.opponent_name})")
        else:  # draw
            self.label_info.config(text=f"{self.player_name} và {self.opponent_name} hòa")
        self.ask_replay()

    # ===== Hỏi chơi lại =====
    def ask_replay(self):
        replay = messagebox.askyesno("Chơi lại", "Bạn có muốn chơi tiếp không?")
        if replay:
            self.reset_for_new_game()
        else:
            self.disconnect_and_quit()

    def reset_for_new_game(self):
        """Reset UI cho game mới"""
        self.label_result.config(text="")
        self.label_player_img.config(image="")
        self.label_opponent_img.config(image="")
        self.player_move = None
        self.enable_choice(True)
        
        # Gửi yêu cầu chơi lại tới server
        if self.client_socket:
            try:
                self.client_socket.sendall(Protocol.pack_message({
                    "type": "REPLAY_REQUEST"
                }))
            except:
                pass

    def disconnect_and_quit(self):
        """Đóng kết nối và thoát"""
        self.keep_running = False
        if self.client_socket:
            try:
                self.client_socket.sendall(Protocol.pack_message({
                    "type": "DISCONNECT",
                    "reason": "player_quit"
                }))
                self.client_socket.close()
            except:
                pass
        self.window.destroy()


    def handle_server_message(self, msg):
        msg_type = msg.get('type')
    
        if msg_type == 'OPPONENT_EARLY_DISCONNECT':
            self.window.after(0, lambda: (
                messagebox.showwarning(
                    "Mất kết nối",
                    msg.get('message', 'Đối thủ mất kết nối trước khi bắt đầu')
                ),
                self._reset_ui_to_lobby()
            ))

        elif msg_type == 'ROOM_CLOSED':
            self.window.after(0, lambda: (
                self.label_info.config(
                    text=f"Lỗi: {msg.get('reason', 'Phòng đã đóng')}"
                ),
                self._reset_ui_to_lobby()
            ))

    
    def _reset_ui_to_lobby(self):
        """Reset hoàn toàn về trạng thái ban đầu"""
        self.opponent_name = None
        self.player_move = None
        self.label_info.config(text="Đang chờ kết nối...")
        self.label_result.config(text="")
        self.label_player_img.config(image="")
        self.label_opponent_img.config(image="")
        self.enable_choice(False)
        
        # Cho phép kết nối lại
        self.btn_multi.config(state=tk.NORMAL)
        self.btn_demo.config(state=tk.NORMAL)   
        


    def run(self):
        self.window.mainloop()


if __name__ == "__main__":
    app = App()
    app.run()