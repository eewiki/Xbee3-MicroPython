# Micropython code example for Digi International Xbee3
# 802.15.4 module interface to TE Weather Shield MS8607
# digital barometric pressure and humidity sensor over I2C
#  


from micropython import const
import utime
import ustruct
import machine

# list of commands in hex for MS8607 pressure sensor
c_reset = const(0x1E) # reset command 
r_c1 = const(0xA2) # read PROM C1 command
r_c2 = const(0xA4) # read PROM C2 command
r_c3 = const(0xA6) # read PROM C3 command
r_c4 = const(0xA8) # read PROM C4 command
r_c5 = const(0xAA) # read PROM C5 command
r_c6 = const(0xAC) # read PROM C6 command
r_adc = const(0x00) # read ADC command
r_d1 = const(0x44) # convert D1 (OSR=1024)
r_d2 = const(0x54) # convert D2 (OSR=1024)
p_address = 0x76 #pressure sensor i2c address

# list of commands in hex for MS8607 humidity sensor
h_address = 0x40 #humidty sensor i2c address
r_user = const(0xE7) # read user register command
w_user = const(0xE6) # write user register command
t_temp = const(0xE3) # trigger temperature measurement, hold master
t_humi = const(0xE5) # trigger humidity measurement, hold master
# set register format 
REGISTER_FORMAT = '>h' # ">" big endian, "h" 2 bytes
REGISTER_SHIFT = 4 # rightshift 4 for 12 bit resolution

# set i2c clock to 100KHz
i2c = machine.I2C(1, freq=100000) 
#slave_addr = 0x76

# reset pressure sensor
def reset_ps():
  slave_addr = p_address
  data = bytearray([c_reset])
  i2c.writeto(slave_addr, data)
  return data
  



# scan i2c bus for active addresses
def scan_I2C():
  devices = i2c.scan()
  return devices

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
  

# start D1 conversion - pressure (24 bit unsigned)
def start_d1():
  #print ('start D1 ')
  data = bytearray([r_d1])
  i2c.writeto(slave_addr, data)

# start D2 conversion - temperature (24 bit unsigned)  
def start_d2():
  #print ('start D2 ')
  data = bytearray([r_d2])
  i2c.writeto(slave_addr, data) 

#read pressure sensor ADC
def read_adc(): #read ADC 24 bits unsigned
  data = bytearray([r_adc])
  i2c.writeto(slave_addr, data)
  adc = i2c.readfrom(slave_addr, 3) #ADC is 3 bytes
  value = int.from_bytes(adc, "big") # use builtin to convert to integer
  return value
  
#read humidity sensor user register command 0xE7, default value = 0x02
# default resolution RH 12bit, T 14bit
def read_user():
  data = bytearray([r_user])
  i2c.writeto(slave_addr, data)
  value = i2c.readfrom(slave_addr, 1)
  return value




#read rh: send trigger rh command 0xE5
def read_rh():
  data = bytearray([t_humi])
  i2c.writeto(slave_addr, data)
  raw_rh = i2c.readfrom(slave_addr, 2) # raw RH is 2 bytes
  raw_value = int.from_bytes(raw_rh, "big") # use builtin to convert to integer
  #rh_tc = (-0.15)*(25 - read_temp())# RH temp compensation
  rh_value = (((raw_value/65536)*125) - 6)  # calculate RH
  return rh_value
  
  

# **************** Main Program *********************************

print ('i2c scan addresses found: ',scan_I2C())
print ('perform reset on pressure sensor, code = ',reset_ps())

# read and print humidity sensor user register
slave_addr = h_address #set humidity sensor i2c address
print ('user register: ',read_user())

# read press sensor calibration PROM
slave_addr = p_address
C1 = read_c1()
C2 = read_c2()
C3 = read_c3()
C4 = read_c4()
C5 = read_c5()
C6 = read_c6()




print ('PROM C1 = ', C1)
print ('PROM C2 = ', C2)
print ('PROM C3 = ', C3)
print ('PROM C4 = ', C4)
print ('PROM C5 = ', C5)
print ('PROM C6 = ', C6)

while True:
  #start on pressure sensor
  slave_addr = p_address #set i2c address to pressure sensor
  start_d1() # start D1 conversion
  utime.sleep(1.0) # short delay during conversion
  raw_d1 = read_adc()
  start_d2() # start D2 conversion
  utime.sleep(1.0) 
  raw_d2 = read_adc()
  dT = raw_d2 - (C5 * 256) # difference between actual and ref P temp
  Temp = (2000 + (dT * (C6/8388608)))/100 #actual P temperature
  OFF = (C2*131072) + (C4*dT/64) # offset at actual P temperature
  SENS = (C1*65536) + (C3*dT/128) # pressure offset at actual temperature
  Pres = (raw_d1*SENS/2097152 - OFF)/3276800 # barometric pressure
  print ('P Temp = ', '%.1fC' % Temp)
  print ('Pressure = ', '%.1f ' % Pres)
  utime.sleep(1.0)
  # start on humidity sensor
  slave_addr =h_address
  #print ('H temp in celsius: ','%.1fC' % read_temp())
  RH = read_rh() - 3.6 - (0.18 * Temp)
  print ('relative humidity: ', '%.1f percent' % RH) #temp compensated humidity
  utime.sleep(1.0)
  
















