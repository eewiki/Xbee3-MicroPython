# Micropython code example for Digi International Xbee3
# cellular module interface to Maxim MAX31875R0I2C based
# Mikroelektronika Thermo 6 Click board temp sensor 
#  
#
# Wiring Diagram:
# XBee ->  Thermo 6 Click
#  19  SCL  12 (and connect to pullup resistor)
#   7  SDA  11 (and connect to pullup resistor)
#   1  Vcc  7 (+3.3V)
#  10  GND  8,9 



import utime
import ustruct
import machine

# set register format for MAX31875
REGISTER_FORMAT = '>h' # ">" big endian, "h" 2 bytes
REGISTER_SHIFT = 4 # rightshift 4 for 12 bit resolution

# set i2c clock to 100KHz
# MAX31875R0 i2c adress = 1001000 (0x48)
i2c = machine.I2C(1, freq=100000) 
slave_addr = 0x48  

# scan i2c bus for active addresses
def scan_I2C():
  devices = i2c.scan()
  return devices

# read configuration register
# POR default is x40
def read_config():
  data = i2c.readfrom_mem(slave_addr, 1, 2)
  value = ustruct.unpack(REGISTER_FORMAT, data)[0]
  return value

# read the two temp register bytes and rightshift 4 places
def read_temp():
  tdata = i2c.readfrom_mem(slave_addr, 0, 2)
  value = ustruct.unpack(REGISTER_FORMAT, tdata)[0] >> REGISTER_SHIFT
  temp = value/16
  return temp

# convert temp in C to F  
def convert_c2f(cvalue):
    fvalue = (cvalue * 9 / 5 + 32)
    return fvalue
  
# continuous loop to read and print temp in C and F
def display_continuous():
  while True:
    ctemp = read_temp()
    print('%.1fC' % (ctemp))
    print('%.1fF' % (convert_c2f(ctemp)))
    utime.sleep(4)


print ('i2c scan addresses found: ',scan_I2C())

print ('config register: ',read_config())

display_continuous()
