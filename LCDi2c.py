import smbus
import time

class LCDi2c:
    def __init__(self):
        self.__I2C_ADDR = 0x3f
        self.__LCD_WIDTH = 16

        self.__LCD_CHR = 1
        self.__LCD_CMD = 0

        self.__LCD_LINE_1 = 0x80
        self.__LCD_LINE_2 = 0xC0

        self.__BACKLIGHT = 0x08

        self.__ENABLE = 0b00000100

        self.__E_PULSE = 0.005
        self.__E_DELAY = 0.005

        self.__bus = smbus.SMBus(1)

        self.__lcd_init()

    def __lcd_init(self):
        self.__lcd_byte(0x33,self.__LCD_CMD) # 110011 Initialise
        self.__lcd_byte(0x32,self.__LCD_CMD) # 110010 Initialise
        self.__lcd_byte(0x06,self.__LCD_CMD) # 000110 Cursor move direction
        self.__lcd_byte(0x0C,self.__LCD_CMD) # 001100 Display On,Cursor Off, Blink Off
        self.__lcd_byte(0x28,self.__LCD_CMD) # 101000 Data length, number of lines, font size
        self.__lcd_byte(0x01,self.__LCD_CMD) # 000001 Clear display
        time.sleep(self.__E_DELAY)

    def __lcd_byte(self, bits, mode):
        bits_high = mode | (bits & 0xF0) | self.__BACKLIGHT
        bits_low = mode | ((bits<<4) & 0xF0) | self.__BACKLIGHT

        self.__bus.write_byte(self.__I2C_ADDR, bits_high)
        self.lcd_toggle_enable(bits_high)

        self.__bus.write_byte(self.__I2C_ADDR, bits_low)
        self.lcd_toggle_enable(bits_low)

    def lcd_toggle_enable(self, bits):
        time.sleep(self.__E_DELAY)
        self.__bus.write_byte(self.__I2C_ADDR, (bits | self.__ENABLE))
        time.sleep(self.__E_PULSE)
        self.__bus.write_byte(self.__I2C_ADDR,(bits & ~self.__ENABLE))
        time.sleep(self.__E_DELAY)

    def lcd_string(self, message, line):

        message = message.ljust(self.__LCD_WIDTH," ")
        if line == 1:
            self.__lcd_byte(self.__LCD_LINE_1, self.__LCD_CMD)
        elif line == 2:
            self.__lcd_byte(self.__LCD_LINE_2, self.__LCD_CMD)

        for i in range(self.__LCD_WIDTH):
            self.__lcd_byte(ord(message[i]),self.__LCD_CHR)