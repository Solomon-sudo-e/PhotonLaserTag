
import socket


class UDPConnection:
    def __init__(self, listen_port=7501, send_port=7500):
        self.listen_port = listen_port
        self.send_port = send_port
        self.sender = None
        self.listener = None

    def initialize(self):
        try:
            self.sender = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.listener = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.listener.bind(("0.0.0.0", self.listen_port))
            print(f"[Net] Listening on port {self.listen_port}")
            return True
        except Exception as e:
            print(f"[Net] Initialization failed: {e}")
            return False

    def update_send_port(self, new_port):
        if isinstance(new_port, int):
            self.send_port = new_port
            print(f"[Net] Send port updated to {new_port}")
            return True
        print("[Net] Invalid port type. Must be int.")
        return False

    def transmit(self, message):
        try:
            self.sender.sendto(message.encode(), ("127.0.0.1", self.send_port))
            print(f"[Net] Sent: {message}")
            return True
        except Exception as e:
            print(f"[Net] Send error: {e}")
            return False

    def shutdown(self):
        if self.sender:
            self.sender.close()
        if self.listener:
            self.listener.close()
        print("[Net] Sockets closed.")
