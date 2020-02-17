# Micropython code example for Digi International Xbee3
# Zigbee module interface to TE MS8607 Grove dev boaad -
# digital barometric pressure and humidity sensor over I2C
#  and MCP9808
# FR version .....r3  fix MCP9808 sign bit
# ...r4 send MS8607 dT over Zigbee to test
# ...r5 add 2nd order temp correction when < 20C
# '''r6 update 2nd order corrections 

from micropython import const
import utime
import ustruct
import machine
import sys
import xbee

FWver = "FW version Zigbee_MCP9808_MS8607_i2c_r6"

# list of commands in hex for MCP9808 sensor
r_mid = const(0x06) # pointer to MPC9808 Mfr ID register
r_cfg = const(0x01) # pointer to MPC9808 configuration register
r_id = const(0x07) # pointer to MCP9808 device ID register
r_temp = const(0x05) # pointer to temperature register
i2c_MCP9808 = 0x18 #MCP9808 i2c address

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
h_reset = const(0xFE) # reset command 
h_address = 0x40 #humidty sensor i2c address
r_user = const(0xE7) # read user register command
w_user = const(0xE6) # write user register command
t_temp = const(0xE3) # trigger temperature measurxbee.transmit(TARGET_64BIT_ADDR, print_PTH)ement, hold master
t_humi = const(0xE5) # trigger humidity measurement, hold master
h_user = const(0x00) # set humidity user register defaault to 0x00
# set register format 
REGISTER_FORMAT = '>h' # ">" big endian, "h" 2 bytes
REGISTER_SHIFT = 4 # rightshift 4 for 12 bit resolution

#Zigbee x1B2D router address
ROUTER_64BIT_RTR = b'\x00\x13\xA2\x00\x41\x98\x1B\x84'
#Zigbee coordinator adddress
TARGET_64BIT_ADDR = b'\x00\x13\xA2\x00\x41\xA7\xAD\xBC'

# set i2c clock to 100KHz
i2c = machine.I2C(1, freq=100000) 
#slave_addr = 0x76

def read_9reg(): #read MCP9808 register
  i2c.writeto(slave_addr, data)
  raw_9808 = i2c.readfrom(slave_addr, 2) #raw_9808 is 2 bytes
  return raw_9808



# reset MS8607 pressure sensor
def reset_ps():
  slave_addr = p_address
  data = bytearray([c_reset])
  i2c.writeto(slave_addr, data)
  return data
  
# reset MS8607 humidity sensor
def reset_hs():
  slave_addr = h_address
  data = bytearray([h_reset])
  i2c.writeto(slave_addr, data)
  return data  
  
# scan i2c bus for active addresses
def scan_I2C():
  devices = i2c.scan()
  return devices

def read_c1(): #read MS8607 PROM value C1
  data = bytearray([r_c1])
  i2c.writeto(slave_addr, data)
  raw_c = i2c.readfrom(slave_addr, 2) #raw C is 2 bytes
  value = int.from_bytes(raw_c, "big") # use builtin to convert to integer
  return value

def read_c2(): #read MS8607 PROM value C2
  data = bytearray([r_c2])
  i2c.writeto(slave_addr, data)
  raw_c = i2c.readfrom(slave_addr, 2) #raw C is 2 bytes
  value = int.from_bytes(raw_c, "big") # use builtin to convert to unsigned integer
  return value

def read_c3(): #read MS8607 PROM value C3
  data = bytearray([r_c3])
  i2c.writeto(slave_addr, data)
  raw_c = i2c.readfrom(slave_addr, 2) #raw C is 2 bytes
  value = int.from_bytes(raw_c, "big") # use builtin to convert to unsigned integer
  return value

def read_c4(): #read MS8607 PROM value C4
  data = bytearray([r_c4])
  i2c.writeto(slave_addr, data)
  raw_c = i2c.readfrom(slave_addr, 2) #raw C is 2 bytes
  value = int.from_bytes(raw_c, "big") # use builtin to convert to unsigned integer
  return value

def read_c5(): #read MS8607 PROM value C5
  data = bytearray([r_c5])
  i2c.writeto(slave_addr, data)
  raw_c = i2c.readfrom(slave_addr, 2) #raw C is 2 bytes
  value = int.from_bytes(raw_c, "big") # use builtin to convert to unsigned integer
  return value

def read_c6(): #read MS8607 PROM value C6
  data = bytearray([r_c6])
  i2c.writeto(slave_addr, data)
  raw_c = i2c.readfrom(slave_addr, 2) #raw C is 2 bytes
  value = int.from_bytes(raw_c, "big") # use builtin to convert to unsigned integer
  return value
  
# start MS8607 D1 conversion - pressure (24 bit unsigned)
def start_d1():
  #print ('start D1 ')
  data = bytearray([r_d1])
  i2c.writeto(slave_addr, data)

# start MS8607 D2 conversion - temperature (24 bit unsigned)  
def start_d2():
  #print ('start D2 ')
  data = bytearray([r_d2])
  i2c.writeto(slave_addr, data) 

#read MS8607 pressure sensor ADC
def read_adc(): #read ADC 24 bits unsigned
  data = bytearray([r_adc])
  i2c.writeto(slave_addr, data)
  adc = i2c.readfrom(slave_addr, 3) #ADC is 3 bytes
  value = int.from_bytes(adc, "big") # use builtin to convert to integer
  return value
  
#read MS8607 humidity sensor user register command 0xE7, default value = 0x02
# default resolution RH 12bit, T 14bit
def read_user():
  data = bytearray([r_user])
  i2c.writeto(slave_addr, data)
  value = i2c.readfrom(slave_addr, 1)
  return value


def write_user():
  data = bytearray([w_user])
  i2c.writeto(slave_addr, data)
#  value = i2c.readfrom(slave_addr, 1)
#  return value
  
 #read rh: send trigger rh command 0xE5
def read_rh():
  data = bytearray([t_humi])
  print('RH command',data)
  i2c.writeto(slave_addr, data)
  print('RH command sent', 'slave address= ',slave_addr)
  raw_rh = i2c.readfrom(slave_addr, 2) # raw RH is 2 bytes
  raw_value = int.from_bytes(raw_rh, "big") # use builtin to convert to integer
  #rh_tc = (-0.15)*(25 - read_temp())# RH temp compensation
  rh_value = (((raw_value/65536)*125) - 6)  # calculate RH
  return rh_value
  
  

# **************** Main Program *********************************
print(FWver) #print firmware version

print ('i2c scan addresses found: ',scan_I2C())

print ('perform reset on pressure sensor, code = ',reset_ps())
print ('perform reset on humidity sensor, code = ',reset_hs())

# read and print humidity sensor user register
slave_addr = h_address #set humidity sensor i2c address
# set default humidity user register
data = bytearray([t_humi])
write_user()

print ('user register: ',read_user())

# read press sensor calibration PROM
slave_addr = p_address
C1 = read_c1()
C2 = read_c2()
C3 = read_c3()
C4 = read_c4()
C5 = read_c5()
C6 = read_c6()

# check zigbee connection
while xbee.atcmd("AI") != 0:
    print("#Trying to Connect...")
    utime.sleep(0.5)

print("#Online...")

print ('PROM C1 = ', C1)
print ('PROM C2 = ', C2)
print ('PROM C3 = ', C3)
print ('PROM C4 = ', C4)
print ('PROM C5 = ', C5)
print ('PROM C6 = ', C6)

while True:
  #start on D1 conversion for pressure sensor
  try:
    slave_addr = p_address #set i2c address to pressure sensor
    start_d1() # start D1 conversion
    utime.sleep(1.0) # short delay during conversion
    raw_d1 = read_adc()
    print("D1= ",raw_d1)
  except:
    print("D1 conversion failed")
  
  #start D2 conversion for temperature
  try:
    start_d2() # start D2 conversion
    utime.sleep(1.0)
    raw_d2 = read_adc()
    print("D2= ",raw_d2)
  except:
    print("D2 conversion failed")
   
  #calulate pressure and temperature
  try:
    # difference between actual and ref P temp
    dT = raw_d2 - (C5 * 256)
    print("dT= ",dT)
    #Temp = (2000 + (dT * (C6/8388608)))/100 #actual P temperature in C
    Temp = 2000 + (dT * (C6/8388608))
    if Temp < 2000: # add 2nd order correction when temp < 20C
      T2 = 3*dT**2/8589934592
    else:
      T2 = 5*dT**2/274877906944
    Temp = (2000 -T2 + (dT * (C6/8388608)))/100
    fTemp = (Temp*9/5) + 32
    OFF = (C2*131072) + (C4*dT/64) # offset at actual P temperature
    print("OFF= ",OFF)
    SENS = (C1*65536) + (C3*dT/128) # pressure offset at actual temperature
    print("SENS= ",SENS)
    Pres = (raw_d1*SENS/2097152 - OFF)/3276800 # barometric pressure
    print ('P Temp = ', '%.1fC' % Temp)
    print ('P Temp = ', '%.1fF' % fTemp)
    print ('T2 = ', T2)
    print ('Pressure = ', '%.1f ' % Pres)
    utime.sleep(1.0)
  except:
    print("Temp and Pressure calculation failed")
   
  # start on humidity sensor
  try:
    slave_addr =h_address
    RH = read_rh() - 3.6 - (0.18 * Temp)
    print ('relative humidity: ', '%.1f percent' % RH) #temp compensated humidity
  except:
    print("humidity sensor conversion failed")
  

  
  #read and calcuate MCP9808 temperature
  try:
    slave_addr = i2c_MCP9808 #set i2c address to MCP9808
    data = bytearray([r_temp]) # set MCP9808 temp register pointer
    reg = read_9reg() # read temp register
    msb = reg[0] & 0x1F # clear temp alert settings in msb
    lsb = reg[1]
    print('9808Temp[msb] = ',msb)
    print('9808Temp[lsb] = ',lsb)
    if msb & 0x10 == 0x10: #check if temp negative
      print('negative')
      msb = msb & 0xF # clear sign bit
      temp9 = (msb*16 + lsb/16) - 256 #calcuate negative temp
    else:
      print('positive')
      temp9 = msb*16 + lsb/16 #calculate positive temp
    ftemp9 = (temp9*9/5) +32
    #M_temp = 'MCP9808 temp = ' + str(ftemp9) + "  MS8607 temp = " + str(fTemp)# build MCP9808 temp packet
    M_temp = 'MS8607 dT = ' + str(dT) # build dT test packet
    print(M_temp)
  except:
    print("MCP9808 temp read failed")
    
  
  # build PTH sensor data payload
  try:
    time_snapshot = str(utime.ticks_cpu())
    print_PTH = "PTH_sensor:" + time_snapshot + ":Press:" + str(Pres) + "mB:Temp:" + str(fTemp) + "F:Temp1:" + str(ftemp9) + "F:Humidity:" + str(RH) + "%:#"
    print(print_PTH)
  except:
    print("sensor payload build failed")
    
   
  #transmit PTH data over Zigbee to coordinator
  try:
    xbee.transmit(TARGET_64BIT_ADDR, print_PTH)
    #xbee.transmit(ROUTER_64BIT_x1B2D, print_PTH)
    #
  except:
    print("xbee coordinator transmit failed")
  
  utime.sleep(5.0) #short delay between transmit
  
  #transmit temperature data over Zigbee to router
  try:
    #xbee.transmit(TARGET_64BIT_ADDR, print_PTH)
    xbee.transmit(ROUTER_64BIT_RTR, M_temp)
    print("xbee rtr = ",ROUTER_64BIT_RTR)
    #
  except:
    print("xbee router transmit failed") 
  utime.sleep(5.0)
  






































