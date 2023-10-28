import socket
import struct
import socket
import threading
from typing import Any
from queue import Queue


class Radio:
    def __init__(self, group=0, receive_message=True, receive_own_message=False):
        # group 0-255
        self._group = group
        self._port = 34567
        # run the udp server
        self._message_queue = Queue()
        self._receive_own_message = receive_own_message
        self.last_string = None
        self.last_number = None
        self.on_message = None

        if receive_message:
            udp_server_thread = threading.Thread(target=self._run_udp_server)
            udp_server_thread.daemon = True
            udp_server_thread.start()
            print("Start listening for messages...")

    def _run_udp_server(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server_socket.bind(("0.0.0.0", self._port))
        while True:
            data, client_address = server_socket.recvfrom(1024)
            # print("client_address: ", client_address)
            decoded_message = None
            if self._receive_own_message:
                decoded_message = self._decode_message(data)
            else:
                # default behavior: Do not receive own messages
                if client_address[1] == 34567:
                    decoded_message = self._decode_message(data)

            if decoded_message:
                self._message_queue.put(decoded_message)
                if callable(self.on_message):
                    self.on_message(decoded_message[0], decoded_message[1])

    def _decode_message(self, data):
        if len(data) < 8:
            return False

        if not (data[0] == 77 and data[1] == 66 and data[2] == 82):
            return False

        if data[3] != self._group:
            return False

        the_number = data[4] | (data[5] << 8) | (data[6] << 16) | (data[7] << 24)
        the_string = data[8:].decode("utf-8")  # Assuming the message is a bytes object

        return (the_number, the_string)

    def send_pair(self, s: str = "light", n: int = 10):
        msg = bytearray()
        msg.extend(b"MBR")
        msg.append(self._group)
        msg.extend(struct.pack("<I", n))
        msg.extend(s.encode("utf-8"))
        broadcast_address = ("255.255.255.255", self._port)
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        sock.sendto(msg, broadcast_address)
        sock.close()

    def send_string(self, s: str):
        self.send_pair(str(s), 0)

    def send_number(self, n: int):
        self.send_pair("", int(n))

    def message_received(self):
        if self._message_queue.empty():
            return False
        else:
            self.last_number, self.last_string = self._message_queue.get()
            return True
        