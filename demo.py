import time
from microblocks_wifi_radio import Radio
r = Radio()
r.send_number(123)
time.sleep(1)
r.send_string("hello")
time.sleep(1)
r.send_pair("light", -10)

while True:
    time.sleep(0.01)
    if r.message_received():
        print(r.last_number)
        print(r.last_string)