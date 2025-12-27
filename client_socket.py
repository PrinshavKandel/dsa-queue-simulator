import socket
import json
import threading
HEADER = 64
FORMAT = "utf-8"
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)

class SocketClient:
    def __init__(self):
        # Socket config
        self.HEADER = 64
        self.FORMAT = "utf-8"
        self.PORT = 5050
        self.SERVER = socket.gethostbyname(socket.gethostname())
        self.ADDR = (self.SERVER, self.PORT)
        
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.running = False
        self.traffic_data = None
        self.data_callback = None  # Function to call when data received
    
    def connect(self):
        try:
            self.client.connect(ADDR)
            print(f"[CONNECTED] {SERVER}:{PORT}")
            return True
        except Exception as e:
            print(f"[ERROR] {e}")
            return False
    def receive_data(self):
        try:
         while self.running:
            msg_length = self.client.recv(self.HEADER).decode(self.FORMAT)
            if msg_length:
                msg_length = int(msg_length.strip())
                msg = self.client.recv(msg_length).decode(self.FORMAT)
                data = json.loads(msg)
                if self.data_callback: 
                    self.data_callback(data)
        except:
           self.running = False
    def start(self,callback):
       self.data_callback = callback
       if self.connect():
           self.running = True
           threading.Thread(target=self.receive_data, daemon=True).start()
           return True
       return False