# general Libs 
import machine
from machine import SoftI2C, Pin
import math
from time import sleep

# LCD Libs 
from lcd_api import LcdApi
from i2c_lcd import I2cLcd

# Temp and humidity sensor lib 
import am2320

# Defines Dir calcuating the dewpoint 
DEWPOINT_MIN_DIFF = 5.0
HYSTERESIS = 1.0
TEMP1_MIN = 10.0
TEMP2_MIN = -10.0

# correction values for the sensors 
SENS1_CORR_H = 0
SENS1_CORR_T = 0
SENS2_CORR_H = 0
SENS2_CORR_T = 0

# Define I2C address and row/columns of the Display
I2C_ADDR = 0x27
ROWS = 4
COLUMNS = 20
# Define I2C Pins for the Display 
DISP_SCL_PIN = Pin(21)
DISP_SDA_PIN = Pin(25)

# Define Masking for the I2C multipexer to read different channels 
maskSensor_1 = b'\x01'
maskSensor_2 = b'\x02'

# init I2C for sensors 
i2c = SoftI2C(scl=Pin(32), sda=Pin(26))
sensor_1 = am2320.AM2320(i2c)
sensor_2 = am2320.AM2320(i2c)

# init I2C for the display
disp_i2c = SoftI2C(scl=DISP_SCL_PIN, sda=DISP_SDA_PIN, freq=400000)     

# init display 
lcd = I2cLcd(disp_i2c, I2C_ADDR, ROWS, COLUMNS)

# Fan Relais 
relay_1 = Pin(19, Pin.OUT)
relay_2 = Pin(22, Pin.OUT)

def calculateDewPoint(temp, rel_hum):
    a = 17.625
    b = 243.04
    # The algorith used is based on Magnus-tetens formula
    # research by Mark G Lawrence for calculating the dewpoint
    # it is accurate ~ 0.35 C, for a range between -45 and 60 C
    alpha = ((a * temp) / (b + temp)) + math.log(rel_hum/100.0)
    ts = (b * alpha) / (a - alpha)
    return ts

def controlRelay(deltaDP):
    if (deltaDP > DEWPOINT_MIN_DIFF + HYSTERESIS):
        relay_1.on()
        relay_2.on()
        return 1
    else:
        relay_1.off()
        relay_2.off()
        return 0
                
def readSensor(sensor):
    sensor.measure()
    temp = sensor.temperature()
    hum = sensor.humidity() 
    return temp, hum

def i2cDisableChannels(i2c):
    # disable all 8 channels
    i2c.writeto(0x70, b'\x00')
    
def i2cReadFrom(i2c):
    # read which channels are enabled?
    device = i2c.readfrom(0x70, 1)
    # b'\x05' - channels 0 and 2 (0x05 == 0b_0000_0101)
    print("device enabled: ", device)

def i2cEnableChannel(i2c, mask):
    # disable all channels
    i2cDisableChannels(i2c)
    # enable channel 0 (SD0,SC0)
    i2c.writeto(0x70, mask)
    i2c.scan()
    
def calculateDewPointFromSensor(i2c, mask):
    # Enable masked channel 
    i2cEnableChannel(i2c, mask)
    # Read sensor values from specific channel 
    temp, hum = readSensor(sensor_1)
    # Disable all channels again for next read
    i2cDisableChannels(i2c)
    
    dewPoint = calculateDewPoint(temp, hum)
    result = [temp, hum, dewPoint]
    return result

def printScreen(sensor_1, sensor_2, delta, relayState):
    # Write first row of the display
    lcd.move_to(0, 0)
    lcd.putstr("S1")
    lcd.putstr(createPrintString(sensor_1))
    # Write second row of the display
    lcd.move_to(0, 1)
    lcd.putstr("S2")
    lcd.putstr(createPrintString(sensor_2))
    # Write third row of the display
    lcd.move_to(0, 2)
    s = '{}{:.1f}'.format('delta ', delta)
    lcd.putstr(str(s))
    # Write forth row of the display
    lcd.move_to(0, 3)
    if(relayState == 1):
        lcd.putstr('Relay is ON')
    else:
        lcd.putstr('Relay is OFF')
    
def createPrintString(values):
    # format a string with given temperature, humidity, and dewpoint
    temp = ' T'
    hum = ' H'
    dp = ' dp'
    s = '{}{:.1f}{}{:.1f}{}{:.1f}'.format(temp, values[0], hum, values[1], dp, values[2])
    return s

lcd.clear()
lcd.backlight_on()
      
flag = 50
while(flag > 0):
    
    # read values the sensors and calculate the dewpoint 
    dewPoint_1 = calculateDewPointFromSensor(i2c, maskSensor_1)
    dewPoint_2 = calculateDewPointFromSensor(i2c, maskSensor_2)
    
    # calculate delta for switching the relay
    delta = dewPoint_2[2] - dewPoint_1[2]
    relayState = controlRelay(delta)
    
    # print the LCD screen 
    printScreen(dewPoint_1, dewPoint_2, delta, relayState)
    
    sleep(0.5)
    flag -= 1 



    
    
    



