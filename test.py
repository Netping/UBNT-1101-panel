#!/usr/bin/python3
from cpanel import *
import time




def main():
    Panel = CPanel()
    Panel.LEDSet('POWER', 'ON')
    
    time.sleep(2)
    Panel.LEDSet('OK', 'ON')
    
    time.sleep(2)
    Panel.LEDSet('FAILED', 'ON')
    
    time.sleep(2)
    Panel.LEDSet('RUNNING', 'ON')

    time.sleep(2)
    Panel.LEDSet('OK', 'OFF')
    
    time.sleep(2)
    Panel.LEDSet('FAILED', 'OFF')
    
    time.sleep(2)
    Panel.LEDSet('RUNNING', 'OFF')

    time.sleep(2)
    Panel.LEDSet('POWER', 'OFF')

    if Panel.isPushed():
        print('Button is pressed')
    else:
        print('Button is not pressed')

if __name__ == "__main__":
    main()
