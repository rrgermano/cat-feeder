from mfrc522 import MFRC522
from machine import reset
import utime


class SimpleRFID:    
    def __init__(self, spi_id=0,sck=3,miso=1,mosi=2,cs=4,rst=0):
        self.reader = MFRC522(spi_id=spi_id,sck=sck,miso=miso,mosi=mosi,cs=cs,rst=rst)
        with open('./cards.txt', 'rb') as file:
            self.cards = list(set(file.read().split(';')))
            file.close()
        
    
    def read(self):
        for _ in range(4):
            (stat, tag_type) = self.reader.request(self.reader.REQIDL)
            if stat == self.reader.OK:
                (stat, uid) = self.reader.SelectTagSN()
                if stat == self.reader.OK:
                    return uid
        return None

    def save(self, func):
        uid = self.read_block()
        if uid:
            if uid not in self.cards:
            
                self.cards.append(uid)
                func('g', 3)
            else:
                self.cards.remove(uid)
                func('b', 3)
            with open('./cards.txt', 'wb') as f:
                f.write(','.join(self.cards))
                f.close()
                reset()
            return True
            
        func('r', 3)
        return False
        
    def uidToString(self, uid):
        mystring = ""
        for i in uid:
            mystring = "%02X" % i + mystring
        return mystring
    
    def auth(self):
        uid = self.read()
        if uid is None:
            return None
        if uid in self.cards:
            return 'Authorized'
        else:
            return 'Not Authorized'
    
    def read_block(self):
        now = utime.time()
        while (utime.time() - now) < 30:
            (stat, tag_type) = self.reader.request(self.reader.REQIDL)
            if stat == self.reader.OK:
                (stat, uid) = self.reader.SelectTagSN()
            if stat == self.reader.OK:
                return self.uidToString(uid)
        return None
