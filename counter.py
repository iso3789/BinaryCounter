#!/usr/bin/env python3
# 2021 nr@bulme.at
# Ivan Dzido

from gpiozero import Button
from PyQt5.QtCore import Qt, QObject, pyqtSignal
from PyQt5.QtWidgets import (QWidget, QLCDNumber,
    QVBoxLayout, QApplication) 
from gpiozero import LEDBoard
from threading import Thread

DOWN_PIN = 17
RESET_PIN = 22
UP_PIN = 27
leds = LEDBoard(18, 23, 24, 25, pwm=True)

class QtButton(QObject):
    changed = pyqtSignal()

    def __init__(self, pin):
        super().__init__()
        self.button = Button(pin) 
        self.button.when_pressed = self.gpioChange        

    def gpioChange(self):
        self.changed.emit()
        gui.checker()

class Counter(QWidget):
    
    nrButtons = len(leds)
    decMax = 0
    decMin = 0
    
    
    def __init__(self):
        super().__init__()
        self.initUi()
        self.count = 0
        for i in range(self.nrButtons):
            self.decMax += 2**i

    def initUi(self):
        self.lcd = QLCDNumber()
        self.lcd.display(0)

        vbox = QVBoxLayout()
        vbox.addWidget(self.lcd)

        self.setLayout(vbox)
        self.setMinimumSize(400, 200)
        self.setWindowTitle('Counter')
        self.show()


    def countUp(self):
        if (self.count == self.decMax):
            self.count = self.decMin
        else: 
            self.count += 1
        self.lcd.display(self.count)
        
    def countReset(self):
        self.count = self.decMin
        self.lcd.display(self.decMin)
        
    def countDown(self):
        if (self.count == self.decMin):
            self.count = self.decMax
        else: 
            self.count -= 1
        self.lcd.display(self.count)
        
    def checker(self):
        for i in range(self.nrButtons):
            leds[i].off()
            if (self.count & 1<<i):
                leds[i].on()

if __name__ ==  '__main__':
    app = QApplication([])
    gui = Counter()
    buttonUp = QtButton(UP_PIN)
    buttonReset = QtButton(RESET_PIN)
    buttonDown = QtButton(DOWN_PIN)
    buttonReset.changed.connect(gui.countReset)
    buttonDown.changed.connect(gui.countDown)
    buttonUp.changed.connect(gui.countUp)
    app.exec_()

