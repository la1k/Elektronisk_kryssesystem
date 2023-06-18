import asyncio
import evdev
from evdev import InputDevice, categorize  # import * is evil :)

devices = [evdev.InputDevice(path) for path in evdev.list_devices()]

nfc_dev = []
barcode = []
for device in devices:
    if device.name == 'Sycreader USB Reader':
        nfc_dev.append(device.path)
    elif device.name == 'Opticon Opticon USB Barcode Reader':
        barcode.append(device.path)
        
        
    

scancodes = {
    # Scancode: ASCIICode
    0: None, 1: u'ESC', 2: u'1', 3: u'2', 4: u'3', 5: u'4', 6: u'5', 7: u'6', 8: u'7', 9: u'8',
    10: u'9', 11: u'0', 12: u'-', 13: u'=', 14: u'BKSP', 15: u'TAB', 16: u'Q', 17: u'W', 18: u'E', 19: u'R',
    20: u'T', 21: u'Y', 22: u'U', 23: u'I', 24: u'O', 25: u'P', 26: u'[', 27: u']', 28: u'CRLF', 29: u'LCTRL',
    30: u'A', 31: u'S', 32: u'D', 33: u'F', 34: u'G', 35: u'H', 36: u'J', 37: u'K', 38: u'L', 39: u';',
    40: u'"', 41: u'`', 42: u'LSHFT', 43: u'\\', 44: u'Z', 45: u'X', 46: u'C', 47: u'V', 48: u'B', 49: u'N',
    50: u'M', 51: u',', 52: u'.', 53: u'/', 54: u'RSHFT', 56: u'LALT', 100: u'RALT'
}




def convert(list):
     
    # Converting integer list to string list
    s = [str(i) for i in list]
     
    # Join list items using join()
    res = int("".join(s))
     
    return(res)

def get_number(number):
    return(convert(number))

async def helper(dev):
    number = []

    async for event in dev.async_read_loop():
        


        if event.type == evdev.ecodes.EV_KEY:
            data = evdev.categorize(event)  # Save the event temporarily to introspect it
            if data.keystate == 1:  # Down events only
                key_lookup = scancodes.get(data.scancode) or u'UNKNOWN:{}'.format(data.scancode)  # Lookup or return UNKNOWN:XX
                if key_lookup == 'CRLF':
                    return get_number(number)
                else:
                    number.append(int(key_lookup))


def wait_for_rfid():
    dev1 = InputDevice(nfc_dev[0])
    dev2 = InputDevice(nfc_dev[1])
    dev3 = InputDevice(nfc_dev[2])
    dev4 = InputDevice(nfc_dev[3])
    loop = asyncio.get_event_loop()
    
    async def main():
        tasks = [asyncio.create_task(helper(dev)) for dev in [dev1, dev2, dev3, dev4]]
        done, _ = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
        results = [task.result() for task in done]
        return results[0]
    
    try:
        return loop.run_until_complete(main())
    finally:
        loop.close()
  
  
    
# def wait_rfid():
#     dev1 = InputDevice(nfc_dev[0])
#     dev2 = InputDevice(nfc_dev[1])
#     dev3 = InputDevice(nfc_dev[2])
#     dev4 = InputDevice(nfc_dev[3])
#     loop = asyncio.get_event_loop()

    
#     for gul in dev1, dev2, dev3, dev4:
#         asyncio.ensure_future(helper(gul))















 


