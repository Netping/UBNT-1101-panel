#!/usr/bin/python3
from cpanel import *




def main():
    Panel = CPanel()
    Panel.LEDSet('POWER', 'ON')
    Panel.LEDSet('OK', 'ON')

    if Panel.isPushed():
        print('Button is pressed')
    else:
        print('Button is not pressed')

if __name__ == "__main__":
    main()
