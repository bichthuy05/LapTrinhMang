
# Game Rock-Paper-Scissors

1. Thành viên và nhiệm vụ:
  Huy: Server Core
  Nhuần : Client Handler
  Mỹ Hoàng : GUI
  Thủy : Protocol & Testing

2. Cách thức hoạt động:

CHẾ ĐỘ 2 NGƯỜI CHƠI:
  Người chơi 1 (Client 1): nhập tên->kết nối đến Server → chọn Rock/Paper/Scissors.
  Người chơi 2 (Client 2) nhập tên->kết nối → Server ghép cặp 2 người → bắt đầu trận đấu.
  Server so sánh lựa chọn → trả kết quả về cả 2 client.

CHẾ ĐỘ CHƠI VỚI MÁY:
  Người chơi nhập tên-> kết nối đến Server → chọn Rock/Paper/Scissors 
  Máy kết nối -> server ghép cặp người với máy -> bắt đầu trận đấu.
  Server so sánh lựa chọn -> trả kết quả về client.

3. Luật chơi:
  Rock smashes scissors.
  Paper covers rock.
  Scissors cut paper.

4. CÁCH CHẠY:

Run the Server:
PS C:\Game Rock-Paper-Scissors> cd rps-game       
PS C:\Game Rock-Paper-Scissors\rps-game> python -m server.rps_server

Run the Client:
PS C:\Game Rock-Paper-Scissors\rps-game> python -m client.main





  
