from machine import Pin, PWM, Timer
from utime import sleep_ms

class HoldButton:
    def __init__(self, pin):
        self._bt = Pin(pin, Pin.IN, Pin.PULL_UP)
        self._counter = 0
        self._timer = Timer()
        
    def _handler(self, timer):
        if self._bt.value() == 0:
            self._counter +=1
        else: self._counter = 0
        if self._counter == self._times:
            self._func1()
    
    def init(self, time, func1):
        self._func1 = func1
        self._times = int(time*10)
        self._timer.init(period = 100, callback = self._handler)
        
    def deinit(self):
        self._timer.deinit()
        del self._func
        del self._times
        
class PulseLED:
    def __init__(self, red, green, blue):
        self._red = red
        self._green = green
        self._blue = blue
        self.pwm = self.values()
        self._time = None
        self.current_led = None
        self.blink_led = None
        self._timer = Timer()
        self.last_color = None
    
    def standart(self):
        self.last_color = None
        self.change_color('b', 2)
        self._timer.init(period = self._time, callback = self.pulse)
    
    def values(self):
        while True:
            for i in range(0, 65535, 327):
                yield i
            for i in range(65535, 0, -327):
                yield i
    
    def pulse(self, timer):
        self.current_led.duty_u16(next(self.pwm))
    
    def reset(self, pin=None):
        self.pwm = self.values()
        if self.current_led:
            self.current_led.duty_u16(0)
        if pin:
            self.current_led = PWM(Pin(pin, Pin.OUT))
            self.current_led.freq(1000)
            
            
    def change_color(self, led, time):
        flag = 0
        if led.upper()[0] == 'R' and self.last_color != led.upper()[0]:
            flag = 1
            self.reset(self._red)
        elif led.upper()[0] == 'G' and self.last_color != led.upper()[0]:
            flag = 1
            self.reset(self._green)
        elif led.upper()[0] == 'B' and self.last_color != led.upper()[0]:
            flag = 1
            self.reset(self._blue)
        if int(time*5) != self._time:
            flag = 1
            self.reset()
            self._time = int(time*5)
            self._timer.init(period = self._time, callback = self.pulse)
        if flag:
            self.last_color = led.upper()[0]
        
    def toggle(self):
        if self.blink_led.duty_u16()>100:
            self.blink_led.duty_u16(0)
        else:
            self.blink_led.duty_u16(-2)
    
    def blink(self, color, times):
        self._timer.deinit()
        self.reset()
        if color.upper()[0] == 'R':
            pin = self._red
        elif color.upper()[0] == 'G':
            pin = self._green
        elif color.upper()[0] == 'B':
            pin = self._blue    
        for _ in range(2*times-1):
            Pin(pin, Pin.OUT).toggle()
            sleep_ms(200)
        Pin(pin, Pin.OUT).toggle()
        self.standart()
            
        
            
class Servo:

    def __init__(self, pin, opened = 1000000, closed = 2000000, init_closed = True):
        self._closed = self._max = closed
        self._opened = self._min = opened
        self._flag_open = False
        self._step = 10000
        self._pos = self._values()
        self._sm = PWM(Pin(pin))
        self._sm.freq(50)
        self._timer = Timer()
        self._timer.init(period = 10, callback = self._cover)
        if init_closed:
            self._sm.duty_ns(self._closed)
            
    def _values(self):
        while True:
            #abrindo
            for i in range(self._closed, self._opened, -self._step):
                yield i
            self._clear()
            #fechando
            for i in range(self._opened, self._closed+self._step, self._step):
                yield i
            
    def _clear(self):
        self._closed = self._max
        self._opened = self._min
        
    
    def _cover(self, timer):
        if self._flag_open:
            if self._sm.duty_ns() > self._opened:
                self._sm.duty_ns(next(self._pos))
        else:
            if self._sm.duty_ns() < self._closed:
                self._sm.duty_ns(next(self._pos))
                
    def open(self, stats):
        if self._sm.duty_ns() != self._closed and stats:
            self._closed = self._sm.duty_ns()
            self._pos = self._values()
            next(self._pos)
        self._flag_open = stats
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
        
            
            

               