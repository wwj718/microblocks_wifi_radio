# WiFi Radio

This package works with [MicroBlocks](https://microblocks.fun/) WiFi Radio library.

## Install

```
pip install microblocks_wifi_radio
```

## Usage

```
import time
from microblocks_wifi_radio import Radio
r = Radio()
r.send_number(123)
r.send_string("hello")

while True:
    time.sleep(0.01)
    if r.message_received():
        print(r.last_number)
        print(r.last_string)
```

## Note

Most code is written by GPT4: [GPT4 translated the MicroBlocks code](https://chat.openai.com/share/86846465-edc5-4703-b25f-c726f4cde580)