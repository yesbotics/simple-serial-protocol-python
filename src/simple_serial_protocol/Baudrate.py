from enum import Enum


class Baudrate(int, Enum):
    BAUD_115200 = 115200
    BAUD_57600 = 57600
    BAUD_38400 = 38400
    BAUD_19200 = 19200
    BAUD_9600 = 9600
    BAUD_4800 = 4800
    BAUD_2400 = 2400
    BAUD_1800 = 1800
    BAUD_1200 = 1200
    BAUD_600 = 600
    BAUD_300 = 300
    BAUD_200 = 200
    BAUD_150 = 150
    BAUD_134 = 134
    BAUD_110 = 110
    BAUD_75 = 75
    BAUD_50 = 50
