# dewpoint-control-uPy
dew point controller using m5stack Atom switch, 20x4 LCD Display, AM2315 Sensors.

## How it works
Dewpoint is the temperature at which the air is saturated with water vapor. When the air cools below its dewpoint, water vapor condenses into liquid water. This is why you see condensation on your windows in the morning, when the outside air is cooler than the inside air.

In the winter, when you heat your garage, the absolute humidity in the air increases. This is because warm air can hold more water vapor than cold air. When you turn off the heat, the air cools down and the relative humidity increases. If the relative humidity gets high enough, the air will become saturated and water will condense on surfaces.

This condensation can lead to corrosion on metal, and can also damage other materials, such as wood and drywall.

A dewpoint controller can help to prevent condensation by ventilating the garage when the dewpoint inside is higher than the dewpoint outside. This brings in drier air from outside, which helps to reduce the humidity inside the garage.

[wiki](https://en.wikipedia.org/wiki/Dew_point)

## Concept
The main idea came from [make](https://www.heise.de/select/make/2022/1/2135511212557842576). The source code can be found [here](https://github.com/MakeMagazinDE/Taupunktluefter)

The main difference to the original project is the use of micropython instead of the arduino framework. This was my first micropython project and I wanted to try it out.

## Hardware
- MCU [M5Stack ATOM Lite ESP32 Development Kit](https://shop.m5stack.com/products/atom-lite-esp32-development-kit)
- Relays [ATOM SWITCH](https://shop.m5stack.com/products/atom-hub-switch-kit) 
- I2C Hub [Grove I2C Hub](https://wiki.seeedstudio.com/Grove-8-Channel-I2C-Multiplexer-I2C-Hub-TCA9548A/)
- Display Generic 4x16 LCD Display with I2C interface
- Sensors [AM2315](https://www.adafruit.com/product/1293) discontinued, but there are many alternatives
- Power Supply [Meanwell IRM 30-5st](https://www.meanwell-web.com/en-gb/ac-dc-single-output-encapsulated-power-supply-irm--30--5st)

The enclosure is not important, I used a normal plastic junction box to house the electronics with a cutout for the display. 

### Assembly
The advantage of using the m5stack Atom Switch with the Atom lite mcu has the advantage that the relays are already connected to the mcu. 
Since the 3 i2c devices are connected, an additional i2c hub is necessary for easier distribution and connection of the sensors and the display.

I used a fully encapsulated powersupply to power the Microcontroller for additional safety and ease of use. 

## Software
Written in python, using the MicroPython Aosong AM2320 I2C driver for the temperatur and humidity sensor.

The easiest way to install the software is to use [Thonny](https://thonny.org/). It is a python IDE with a build in file transfer tool.

