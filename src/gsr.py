import sys
import glob
import serial

def serial_ports():
    """ Lists serial port names

        This method is borrowed from a stackexchange answer.
        https://stackoverflow.com/a/14224477
        Original Author: Thomas (https://stackoverflow.com/users/300783/thomas)

        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
    """
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result


class GSRSensor(object):            
    def __init__(self):
        self.active_port = "COM7"
        self.gsr = None

    def openPort(self):
        try:
            self.gsr = serial.Serial(self.active_port, 9600, timeout=.1)
            return True
        except (OSError, serial.SerialException):
            pass
        return False

    def closePort(self):
        self.gsr.close()
        self.gsr = None

    def readVal(self):
        return self.gsr.readline()[:-2]

    def listAvailablePorts(self):
        print(serial_ports())