import time

from microblocks_wifi_radio import Radio
r = Radio()
r.send_number(123)
r.send_string("hello")

while True:
    time.sleep(0.01)
    if r.message_received():
        print(r.last_string)
        print(r.last_number)