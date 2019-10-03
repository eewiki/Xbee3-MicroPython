# Micropython code example for Digi International Xbee3
# 802.15.4 module interface to TE Weather Shield TSYS01
# digital temperature sensor over I2C
#  


from micropython import const
import utime
import ustruct
import machine

# list of commands in hex for TSYS01
c_reset = const(0x1E) # reset command
r_c1 = const(0xA2) # read PROM C1 command
r_c2 = const(0xA4) # read PROM C2 command
r_c3 = const(0xA6) # read PROM C3 command
r_c4 = const(0xA8) # read PROM C4 command
r_c5 = const(0xAA) # read PROM C5 command
r_c6 = const(0xAC) # read PROM C6 command
r_adc = const(0x00) # read ADC command
r_d1 = const(0x48) # start ADC conversion



# set i2c clock to 100KHz
# TE TSYS01 i2c adress = 0x77
i2c = machine.I2C(1, freq=100000) 
slave_addr = 0x77  

# reset device to make sure PROM loaded
data = bytearray([c_reset])
i2c.writeto(slave_addr, data)

# scan i2c bus for active addresses
def scan_I2C():
  devices = i2c.scan()
  return devices
  
print ('i2c address scan = ', scan_I2C())  
  
def read_c1(): #read PROM value C1
  data = bytearray([r_c1])
  i2c.writeto(slave_addr, data)
  raw_c = i2c.readfrom(slave_addr, 2) #raw C is 2 bytes
  value = int.from_bytes(raw_c, "big") # use builtin to convert to integer
  return value

def read_c2(): #read PROM value C2
  data = bytearray([r_c2])
  i2c.writeto(slave_addr, data)
  raw_c = i2c.readfrom(slave_addr, 2) #raw C is 2 bytes
  value = int.from_bytes(raw_c, "big") # use builtin to convert to unsigned integer
  return value

def read_c3(): #read PROM value C3
  data = bytearray([r_c3])
  i2c.writeto(slave_addr, data)
  raw_c = i2c.readfrom(slave_addr, 2) #raw C is 2 bytes
  value = int.from_bytes(raw_c, "big") # use builtin to convert to unsigned integer
  return value

def read_c4(): #read PROM value C4
  data = bytearray([r_c4])
  i2c.writeto(slave_addr, data)
  raw_c = i2c.readfrom(slave_addr, 2) #raw C is 2 bytes
  value = int.from_bytes(raw_c, "big") # use builtin to convert to unsigned integer
  return value

def read_c5(): #read PROM value C5
  data = bytearray([r_c5])
  i2c.writeto(slave_addr, data)
  raw_c = i2c.readfrom(slave_addr, 2) #raw C is 2 bytes
  value = int.from_bytes(raw_c, "big") # use builtin to convert to unsigned integer
  return value

def read_c6(): #read PROM value C6
  data = bytearray([r_c6])
  i2c.writeto(slave_addr, data)
  raw_c = i2c.readfrom(slave_addr, 2) #raw C is 2 bytes
  value = int.from_bytes(raw_c, "big") # use builtin to convert to unsigned integer
  return value
  

# start ADC conversion - temperature (24 bit unsigned)
def start_d1():
  data = bytearray([r_d1])
  i2c.writeto(slave_addr, data)


#read ADC
def read_adc(): #read ADC 24 bits unsigned
  data = bytearray([r_adc])
  i2c.writeto(slave_addr, data)
  adc = i2c.readfrom(slave_addr, 3) #ADC is 3 bytes
  value = int.from_bytes(adc, "big") # use builtin to convert to integer
  return value


# **************** Main Program *********************************

print ('i2c scan addresses found: ',scan_I2C())

# read and print PROM calibration data  
k4 = read_c1()
k3 = read_c2()
k2 = read_c3()
k1 = read_c4()
k0 = read_c5()
print ('k4 = ', k4)
print ('k3 = ', k3)
print ('k2 = ', k2)
print ('k1 = ', k1)
print ('k0 = ', k0)


while True:
  start_d1() # start ADC conversion
  utime.sleep(1.0) # short delay during conversion
  ADC24 = read_adc() # read ADC
  ADC16 = ADC24/256
  #temperature calculation variables
  T4 = (-2) * 1e-21 * k4 * (ADC16**4) 
  T3 = 4 * 1e-16 * k3 * (ADC16**3)
  T2 = (-2) * 1e-11 * k2 * (ADC16**2)
  T1 = 1e-6 * k1 * ADC16
  T0 = (-1.5) * k0 * 1e-2
  #calculate temperature
  T_calc = T4 + T3 + T2 + T1 + T0
  print ('calc temp = ','%.1fC' %T_calc)
  utime.sleep(1.0)
  
















