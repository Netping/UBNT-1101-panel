import parallel
import time
from threading import Thread
from threading import Lock




class CPanel:
    LPT_Map = {
                'POWER' : 1,
                'RUNNING' : 2,
                'FAILED' : 4,
                'OK' : 8
            }

    LEDState = 0
    blink_thread = None
    blink_mutex = Lock()
    blink_map = 0
    blink_delay = 0.5

    def __init__(self):
        self.__port = None

        try:
            self.__port = parallel.Parallel()
            self.__port.setDataStrobe(0)

            if not CPanel.blink_thread:
                CPanel.blink_thread = Thread(target=self.__poll, args=())
                CPanel.blink_thread.start()

        except Exception as e:
            print(e)

    def LEDSet(self, ledname, state):
        if ledname.upper() == 'STB' or ledname.upper() == 'START':
            print('Bad name for LED (' + ledname + ')')
            return

        if state.upper() != 'ON' and state.upper() != 'OFF' and state.upper() != 'BLINK':
            print('Bad name for state (' + state + ')')
            return

        l = list(CPanel.LPT_Map.keys())

        if not ledname in l:
            print('Bad name for LED (' + ledname + ')')
            return

        if state.upper() == 'ON':
            self.__writeBit(CPanel.LPT_Map[ledname], 1)
        elif state.upper() == 'OFF':
            self.__writeBit(CPanel.LPT_Map[ledname], 0)
        elif state.upper() == 'BLINK':
            #print('That state is not working yet')
            CPanel.blink_mutex.acquire()
            CPanel.blink_map = CPanel.blink_map | CPanel.LPT_Map[ledname]
            CPanel.blink_mutex.release()

    def isPushed(self):
        if self.__port:
            value = self.__port.getInError()

            if value:
                return False

        return True

    def __writeBit(self, led, value):
        if self.__port:
            CPanel.blink_mutex.acquire()
            CPanel.blink_map = CPanel.blink_map & ~led
            CPanel.blink_mutex.release()

            if value == 1:
                self.LEDState = self.LEDState | led
            elif value == 0:
                self.LEDState = self.LEDState & ~led
            else:
                print('Bad value for setting bit')
                
            self.__port.setData(self.LEDState)
            self.__port.setDataStrobe(1)
            time.sleep(0.1)
            self.__port.setDataStrobe(0)

    def __poll(self):
        while (1):
            CPanel.blink_mutex.acquire()
            m = CPanel.blink_map
            CPanel.blink_mutex.release()

            #blinking
            self.__port.setData(m)
            self.__port.setDataStrobe(1)
            time.sleep(0.1)
            self.__port.setDataStrobe(0)

            time.sleep(CPanel.blink_delay)

            self.__port.setData(~m & 0xff)
            self.__port.setDataStrobe(1)
            time.sleep(0.1)
            self.__port.setDataStrobe(0)
