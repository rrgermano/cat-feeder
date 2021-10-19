from simple_rfid import SimpleRFID
from drivers import PulseLED, Servo, HoldButton

def save(pause):
    indicator.change_color('g', 1)
    res = reader.save(pause)
    if res == "Add":
        indicator.blink('g', 3)
    elif res == "Remove":
        indicator.blink('b', 3)
    else:
        indicator.blink('r', 3)
    pause()
        
def _handler():
    global flag
    flag = True
    
def pause():
    next(sm_pause)
    next(indicator_pause)
    next(save_button_pause)
    

flag = False
sm = Servo(15)
indicator = PulseLED(18,19,20)
save_button = HoldButton(5)
sm_pause = sm.pause()
indicator_pause = indicator.pause()
save_button_pause = save_button.pause()
reader = SimpleRFID()
indicator.change_color('b', 3)
save_button.init(1.5, _handler)

while True:
    if flag:
        save(pause)
        flag = False
    auth = reader.auth()
    if auth == 'Authorized':
        indicator.change_color('g', 3)
        sm.open(True)
    elif auth == 'Not Authorized':
        indicator.blink('r', 3)
        sm.open(False)
    elif not auth:
        indicator.change_color('b', 3)
        sm.open(False)
