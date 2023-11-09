import asyncio
import evdev
import multiprocessing
from evdev import InputDevice, categorize  # import * is evil :)

lock = multiprocessing.Lock()


def refresh_devices():
    lock.acquire()
    
    devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
    nfc_devices = []
    barcode = []
    for device in devices:
        if device.name == 'Sycreader USB Reader' or device.name == 'IC Reader IC Reader' or device.name == 'GASIA PS2toUSB Adapter':
            nfc_devices.append(device.path)
        elif device.name == 'Opticon Opticon USB Barcode Reader':
            barcode.append(device.path)
    
            
    global nfc_dev
    nfc_dev = nfc_devices
            
    lock.release()

nfc_devices = []
refresh_devices()
    

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



def RFID_worker_fn(q: multiprocessing.Queue, device: InputDevice):
    while True:
        number = []
        try:
            for event in device.read_loop():
                if event.type == evdev.ecodes.EV_KEY:
                    data = evdev.categorize(event)  # Save the event temporarily to introspect it
                    if data.keystate == 1:  # Down events only
                        key_lookup = scancodes.get(data.scancode) or u'UNKNOWN:{}'.format(data.scancode)  # Lookup or return UNKNOWN:XX
                        if key_lookup == 'CRLF':
                            q.put((device, get_number(number)))
                            break
                        else:
                            number.append(int(key_lookup))
        except OSError as e:
            refresh_devices()
            return

def wait_for_rfid():
    q = multiprocessing.Queue()
    nfc_devices = [InputDevice(dev) for dev in nfc_dev]
    procs = [multiprocessing.Process(target=RFID_worker_fn, args=(q, device,)) for device in nfc_devices]
    [p.start() for p in procs]
    while True:
        try:
            device, ID = q.get()
            return ID
        except Exception as e:
            print(e)
            break

    [p.join() for p in procs]
    
    if ID:
        return ID
    return None

    
    













 


