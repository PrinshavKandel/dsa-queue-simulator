import socket
import threading
import json
import time
class SocketServer:
    def __init__(self):
        self.HEADER = 64
        self.FORMAT = "utf-8"
        self.PORT = 5050
        self.SERVER = socket.gethostbyname(socket.gethostname())
        self.ADDR = (self.SERVER, self.PORT)
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(self.ADDR)
        self.connected_clients = []
        self.running = False
    
    def send_to_client(self, conn, data):
        message = json.dumps(data)
        msg_encoded = message.encode(self.FORMAT)
        msg_length = len(msg_encoded)
        send_length = str(msg_length).encode(self.FORMAT)
        send_length += b' ' * (self.HEADER - len(send_length))
        try:
            conn.send(send_length)
            conn.send(msg_encoded)
        except:
            pass
    
    def broadcast_data(self, data):
        for conn in self.connected_clients[:]:
            try:
                self.send_to_client(conn, data)
            except:
                self.connected_clients.remove(conn)
    
    def handle_client(self, conn, addr):
        print(f"[NEW CONNECTION] {addr} connected")
        self.connected_clients.append(conn)
        try:
            while self.running:
                time.sleep(0.1)
        except:
            pass
        if conn in self.connected_clients:
            self.connected_clients.remove(conn)
        conn.close()
        print(f"[DISCONNECTED] {addr} disconnected")
    
    def start(self):
        self.running = True
        def listen():
            self.server.listen()
            print(f"[LISTENING] Server on {self.SERVER}:{self.PORT}")
            while self.running:
                try:
                    conn, addr = self.server.accept()
                    thread = threading.Thread(target=self.handle_client, args=(conn, addr))
                    thread.daemon = True
                    thread.start()
                except:
                    break
        server_thread = threading.Thread(target=listen)
        server_thread.daemon = True
        server_thread.start()
    
    def stop(self):
        self.running = False
        for conn in self.connected_clients:
            conn.close()
        self.server.close()
        print("[SERVER] Stopped")

