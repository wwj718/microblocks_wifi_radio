import socket
import struct
import socket
import threading
from typing import Any
from queue import Queue


class Radio:
    def __init__(self, group=0):
        # group 0-255
        self.group = group
        self._port = 34567
        # run the udp server
        self._message_queue = Queue()
        self.last_number = None
        self.last_string = None
        udp_server_thread = threading.Thread(target=self._run_udp_server)
        udp_server_thread.daemon = True
        udp_server_thread.start()

    def _process_udp_received_packet(self):
        if self._message_queue.empty():
            return False

        msg = self._message_queue.get()
        # self._msg = msg # debug
        if len(msg) < 8:
            return False

        if not (msg[0] == 77 and msg[1] == 66 and msg[2] == 82):
            return False

        if msg[3] != self.group:
            return False

        self.last_number = msg[4] | (msg[5] << 8) | (msg[6] << 16) | (msg[7] << 24)
        self.last_string = msg[8:].decode("utf-8")  # Assuming the message is a bytes object

        return True

    def _run_udp_server(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server_socket.bind(("0.0.0.0", self._port))
        while True:
            data, client_address = server_socket.recvfrom(1024)
            # print("client_address: ", client_address)
            if client_address[1] == 34567:
                # Do not accept own messages
                self._message_queue.put(data)

    def send_pair(self, s: str = "light", n: int = 10):
        msg = bytearray()
        msg.extend(b"MBR")
        msg.append(self.group)
        msg.extend(struct.pack("<I", n))
        msg.extend(s.encode("utf-8"))
        broadcast_address = ("255.255.255.255", self._port)
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        sock.sendto(msg, broadcast_address)
        sock.close()

    def send_number(self, n:int):
        self.send_pair("", int(n))

    def send_string(self, s:str):
        self.send_pair(str(s), 0)

    def message_received(self):
        return self._process_udp_received_packet()
