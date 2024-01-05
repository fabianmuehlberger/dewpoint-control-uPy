from machine import Pin, SoftI2C
import sht31
i2c = SoftI2C(scl=Pin(32), sda=Pin(26), freq =400000)
sensor = sht31.SHT31(i2c, addr=0x44)
print(sensor.get_temp_humi())