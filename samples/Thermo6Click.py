# Digi International Xbee3 cellular module interface to
# Mikroelektronika Thermo 6 Click board temp sensor based on
# Maxim MAX31875R0I2C over I2C
#
#
#
# Wiring Diagram:
# XBee ->  Thermo 6 Click
#  19  SCL  12 (and connect to pullup resistor)
#   7  SDA  11 (and connect to pullup resistor)
#   1  Vcc  7 (+3.3V)
#  10  GND  8,9
import machine
import utime
import ustruct
