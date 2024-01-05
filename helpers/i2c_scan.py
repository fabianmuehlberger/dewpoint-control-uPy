# simple helper to scan i2c bus for devices
# this is not directly needed for running the project, but can be used to check if the i2c bus is working


from machine import SoftI2C, Pin

## Grove Connector 
# sdaPIN = Pin(26)
# sclPIN = Pin(32)

## Pin Out 
sdaPIN = Pin(25)
sclPIN = Pin(21)


i2c=SoftI2C(sda=sdaPIN, scl=sclPIN)   

devices = i2c.scan()
if len(devices) == 0:
 print("No i2c device !")
else:
 print('i2c devices found:',len(devices))
for device in devices:
 print("At address: ",hex(device))