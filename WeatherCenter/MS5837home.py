# Micropython code example for Digi International Xbee3
# Zigbee module interface to TE MS5837-02BA
# digital barometric pressure sensor over I2C
#  


from micropython import const
import utime
import ustruct
import machine
import sys
import xbee



#Zigbee coordinator adddress Digi-Key coordinator
#TARGET_64BIT_ADDR = b'\x00\x13\xA2\x00\x41\xA7\xAD\xBC'
#Zigbee coordinator adddress Home coordinator
TARGET_64BIT_ADDR = b'\x00\x13\xA2\x00\x41\xAA\xCB\xBA'


# list of commands in hex for MS5837
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


# set i2c clock to 100KHz
# TE MS5837 i2c adress = 0x76
i2c = machine.I2C(1, freq=100000) 
slave_addr = 0x76  

# reset device to make sure PROM loaded
data = bytearray([c_reset])
i2c.writeto(slave_addr, data)


# check zigbee connection
while xbee.atcmd("AI") != 0:
    print("#Trying to Connect...")
    utime.sleep(0.5)

print("#Online...")




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
  
# read PROM calibration data  
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

#read ADC
def read_adc(): #read ADC 24 bits unsigned
  data = bytearray([r_adc])
  i2c.writeto(slave_addr, data)
  adc = i2c.readfrom(slave_addr, 3) #ADC is 3 bytes
  value = int.from_bytes(adc, "big") # use builtin to convert to integer
  return value


# **************** Main Program *********************************
print ('FW version: MS5837home.py')
print ('i2c scan addresses found: ',scan_I2C())

while True:
  try:
    # read ms5837
    slave_addr = 0x76
    start_d1() # start D1 conversion
    utime.sleep(1.0) # short delay during conversion
    raw_d1 = read_adc()
    start_d2() # start D2 conversion
    utime.sleep(1.0) 
    raw_d2 = read_adc()
    dT = raw_d2 - (C5 * 256) # difference between actual and ref temp
    Temp = 2000 + (dT * (C6/8388608)) #actual temperature is /100
    OFF = (C2*131072) + (C4*dT/64) # offset at actual temperature
    SENS = (C1*65536) + (C3*dT/128) # pressure offset at actual temperature
    # need to add second order temp compensation if <20C
    if Temp < 2000: # add 2nd order correction when temp < 20C
      Ti = 11*dT**2/34359738368
      OFFi = (31*(Temp - 2000)**2)/8
      SENSi = (63*(Temp - 2000)**2)/32
    else:
      Ti = 0
      OFFi = 0
      SENSi = 0
    print ('Ti = ', Ti)
    SENS = SENS - SENSi
    OFF = OFF - OFFi
    Pres = (raw_d1*SENS/2097152 - OFF)/3276800 # barometric pressure
    # 
    
    Temp = Temp/100
    fTemp = (Temp*9/5) + 32
    print ('Temp = ', '%.1fC' % Temp)
    print ('Temp = ', '%.1fF' % fTemp)
    print ('Pressure = ', '%.1f ' % Pres)
  except:
    print('ms5837 read failed')
  
  # build ms5837 sensor data payload
  try:
    time_snapshot = str(utime.ticks_cpu())
    #print_TH = "T9602:" + time_snapshot + ":Humidity:" + str(t96h) + "%:Temp:" + str(fTemp) + "F:#" #T9602 humidity and temp
    print_PT = "MS5837:" + time_snapshot + ":Press:" + str(Pres) + "mB:Temp:" + str(fTemp) + "F:#" # MS5837 sensor payload
    print(print_PT)
  except:
    print("sensor payload build failed")
    
   
  #transmit Temp Humidity data over Zigbee to coordinator
  try:
    xbee.transmit(TARGET_64BIT_ADDR, print_PT)
    #xbee.transmit(ROUTER_64BIT_x1B2D, print_TH)
    print("send data to coordinator")
  except:
    print("xbee coordinator transmit failed")

  utime.sleep(10.0) #delay between sensors
    
  


  
  utime.sleep(15.0)
  















