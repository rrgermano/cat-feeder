from machine import Pin, PWM
import utime
from pulse_u16 import PulseLED

def servo(sm, pos):
    STEP = 15
    MAX = 2000000
    MIN = 1000000
    if pos == 'MAX' and sm.duty_ns()!=MAX:
        for i in range(MIN, MAX+STEP, STEP):
            sm.duty_ns(i)
    elif pos == 'MIN' and sm.duty_ns()!=MIN:
        for i in range(MAX+STEP, MIN, -STEP):
            sm.duty_ns(i)

    

def save(lista):
    print('salvando')
    indicator.change_color('GREEN', 1.5)
    cards_write = open('./cards.txt', 'w')
    cards_write.write(','.join(lista))
    cards_write.close()
            
if __name__== '__main__':
    indicator = PulseLED(18,19,20, 2)
    sm = PWM(Pin(15))
    save_bt = Pin(12, Pin.IN,  Pin.PULL_UP)
    sm.freq(50)              
    reader = MFRC522(spi_id=0,sck=2,miso=4,mosi=3,cs=1,rst=0)

    try:
        while True:
            uid = read()
            if not save_bt.value():
                if uid:
                    cards.append(read())
                    save(cards)
                print(cards)
            uid = read()
            if uid in cards:
                servo(sm, 'MAX')
            else:
                servo(sm, 'MIN')

    except KeyboardInterrupt:
        print("Bye")


