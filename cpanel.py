import parallel
import time
#from threading import Thread
#from threading import Lock




class CPanel:
    LPT_Map = {
#                'STB' : 1,
                'POWER' : 3,
                'RUNNING' : 5,
                'FAILED' : 7,
                'OK' : 9,
                'START' : 4
            }

    #blink_busy = []
    #blink_threads = []

    def __init__(self):
        self.__port = None

        try:
            self.__port = parallel.Parallel()
#            self.__writeBit(CPanel.LPT_Map['STB'], 0)
            self.__port.setDataStrobe(0)
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
            print('That state is not working yet')

    def isPushed(self):
        if self.__port:
            value = self.__port.getInError()

            if value:
                return True

        return False

    def __writeBit(self, ledname, value):
        if self.__port:
            #convert index to setDataValue
            i = list(CPanel.LPT_Map.keys()).index(ledname)
            index = 1 << (CPanel.LPT_Map[ledname] - 3 - i)

            if value == 1:
                self.__port.setData(index)
                self.__port.setDataStrobe(1)
                time.sleep(0.1)
                self.__port.setDataStrobe(0)
            elif value == 0:
                self.__port.setData(index & (255 - index))
                self.__port.setDataStrobe(1)
                time.sleep(0.1)
                self.__port.setDataStrobe(0)
            else:
                print('Bad value for setting bit')
