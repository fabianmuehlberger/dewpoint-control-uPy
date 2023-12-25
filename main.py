# general Libs 
import machine
from machine import I2C, SoftI2C, Pin
import sht31
import math
from time import sleep

# LCD Libs 
from lcd_api import LcdApi
from i2c_lcd import I2cLcd

# Defines Dir calcuating the dewpoint 
DEWPOINT_MIN_DIFF = 3.0
HYSTERESIS = 1.0
TEMP1_MIN = 5.0
TEMP2_MIN = -10.0

# correction values for the sensors 
SENS1_CORR_H = 2
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

# Define I2C pins for the Sensors
I2C_SENS_SDA = Pin(26)
I2C_SENS_SCL = Pin(32)

# init I2C for sensors 
i2c = I2C(1, scl=I2C_SENS_SCL, sda=I2C_SENS_SDA,freq=400000)
th_sensor = sht31.SHT31(i2c, addr=0x44)

# init I2C for the display
disp_i2c = SoftI2C(scl=DISP_SCL_PIN, sda=DISP_SDA_PIN, freq=400000)     

# init display 
lcd = I2cLcd(disp_i2c, I2C_ADDR, ROWS, COLUMNS)

# Fan Relais 
relay1 = Pin(19, Pin.OUT)
relay2 = Pin(22, Pin.OUT)

def calculateDewPoint(temp, rel_hum):
    a = 17.625
    b = 243.04
    # The algorith used is based on Magnus-tetens formula
    # research by Mark G Lawrence for calculating the dewpoint
    # it is accurate ~ 0.35 C, for a range between -45 and 60 C
    alpha = ((a * temp) / (b + temp)) + math.log(rel_hum/100.0)
    ts = (b * alpha) / (a - alpha)
    return ts

def controlRelay(deltaDP, sens_1, sens_2):
    if (sens_1[0] < TEMP1_MIN) or (sens_2[0] < TEMP2_MIN):
        relay1.off()
        return 0
    elif (deltaDP < DEWPOINT_MIN_DIFF):
        relay1.off()
    elif (deltaDP > DEWPOINT_MIN_DIFF + HYSTERESIS):
        relay1.on()
        return 1
    else:
        relay1.off()
        return 0

def maskI2CMultipexer(mask):
    # disable all channels of the i2c multiplexer
    i2c.writeto(0x70, b'\x00')
    #i2c.writeto(0x70, b'\x01')
    i2c.writeto(0x70, mask)

def getSensorValue(mask):
    maskI2CMultipexer(mask)
    th = th_sensor.get_temp_humi()
    return list(th)
     
def printScreen(sensor_1, sensor_2, delta, relayState):
    lcd.move_to(0, 0)
    lcd.putstr("S1")
    lcd.putstr(createPrintString(sensor_1))
    
    lcd.move_to(0, 1)
    lcd.putstr("S2")
    lcd.putstr(createPrintString(sensor_2))
    
    lcd.move_to(0, 2)
    s = '{}{:.1f}'.format('delta ', delta)
    lcd.putstr(str(s))
    
    lcd.move_to(0, 3)   
    if(relayState == 1):
        lcd.putstr('Relay is ON  ')
    else:
        lcd.putstr('Relay is OFF')
    
def createPrintString(values):
    temp = ' T'
    hum = ' H'
    dp = ' dp'
    s = '{}{:.1f}{}{:.1f}{}{:.1f}'.format(temp, values[0], hum, values[1], dp, values[2])
    return s

lcd.clear()
lcd.backlight_on()
      
flag = 50
while(1):
    
    thd_Sensor_1 = getSensorValue(maskSensor_1)
    dewPoint_1 = calculateDewPoint(thd_Sensor_1[0], thd_Sensor_1[1])
    thd_Sensor_1.append(dewPoint_1)

    
    thd_Sensor_2 = getSensorValue(maskSensor_2)
    dewPoint_2 = calculateDewPoint(thd_Sensor_2[0], thd_Sensor_2[1])
    thd_Sensor_2.append(dewPoint_2)
    
    # correct temp and hum values
    #dewPoint_1[1] += SENS1_CORR_H
    
    delta = thd_Sensor_1[2] - thd_Sensor_2[2]
    relayState = controlRelay(delta, thd_Sensor_1, thd_Sensor_2)
    printScreen(thd_Sensor_1, thd_Sensor_2, delta, relayState)
    
    
    print("sensor_1", thd_Sensor_1)
    print("sensor_2", thd_Sensor_2)
    
    sleep(0.5)



    
    
    




