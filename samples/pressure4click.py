# Micropython code example for Digi International Xbee3
# cellular module interface to Bosch BMP280 based
# Mikroelektronika Pressure 4 Click board barometric sensor 
# sensor 
#
# Wiring Diagram:
# XBee ->  Pressure 4 Click
#  19  SCL  12 
#   7  SDA  11 
#   1  Vcc  7 (+3.3V)
#  10  GND  8,9 


import utime
import ustruct
import machine


# set i2c clock to 100KHz
# Bosch i2c adress = 1110110 (0x76)
# SDO pin set to GND
i2c = machine.I2C(1, freq=100000) 
slave_addr = 0x76  

# read chip id, one byte, value=0x58
def read_chipid():
  REGISTER_FORMAT = '>b'
  data = i2c.readfrom_mem(slave_addr, 0xD0, 1)
  value = ustruct.unpack(REGISTER_FORMAT, data)[0]
  return value

# scan i2c bus for active addresses
def scan_I2C():
  devices = i2c.scan()
  return devices

# read 24 calibration bytes starting at 0x88
def read_calib():  
  cdata = i2c.readfrom_mem(slave_addr, 0x88, 24)
  return cdata
  
# read raw temp and pressure bytes starting at 0xF7  
def read_raw():
  data = i2c.readfrom_mem(slave_addr, 0xF7, 8)
  return data
  
# unpack raw temperature bytes 
def calc_rawt():
  REGISTER_FORMAT = '>i' # big endian 4 bytes
  rawdata = read_raw()
  raw_temp = ustruct.unpack_from(REGISTER_FORMAT, rawdata, 3)[0] >> 12
  return raw_temp

# unpack raw pressure bytes
def calc_rawp():
  REGISTER_FORMAT = '>i' # big endian 4 bytes
  rawdata = read_raw()
  raw_pres = ustruct.unpack_from(REGISTER_FORMAT, rawdata, 0)[0] >> 12
  return raw_pres
 
# calculate and continuously display temperature and pressure every 2 seconds 
def display_continuous(): 
  while True: 
    adc_t = calc_rawt()  # raw temperature
    #calculate temperature
    var1 = ((adc_t / 16384) - (dig_T1 / 1024 ))* dig_T2 # t formula line 1
    var2 = (adc_t / 131072) - (dig_T1 / 8192) # t formula line 2
    var2 = var2 * var2 * dig_T3 # t formula line 2
    tfine = var1 + var2 # t formula line 3
    T_c = tfine/5120
    print('temp is ','%.2fC' % (T_c))
    #calculate pressure
    adc_p = calc_rawp()  # raw pressure
    pvar1 = (tfine/2) - 64000 # p formula line 1
    pvar2 = (pvar1 * pvar1 * dig_P6)/32768 # p formula line 2
    pvar2 = pvar2 + (pvar1 * dig_P5 * 2)  # p formula line 3
    pvar2 = (pvar2/4) + (dig_P4 * 65536)  # p formula line 4
    pvar1 = (dig_P3 * pvar1 * pvar1 / 524288) + (dig_P2 * pvar1) # p formula line 5
    pvar1 = pvar1/524288 # p formula line 5
    pvar1 = (1 + pvar1/32768) * dig_P1 # p formula line 6
    p = 1048576 - adc_p # p formula line 7
    p = (p - (pvar2/4096)) * 6250 / pvar1 # p formula line 8
    pvar1 = dig_P9 * p * p / 2147483648 # p formula line 9
    pvar2 = p * dig_P8 / 32768 # p formula line 10
    p = p + (pvar1 + pvar2 + dig_P7)/16 # p formula line 11
    print('pressure is ','%.2fPa' % (p))
    utime.sleep(2)
  
  
# ##### Main Program ##########

print ('scan I2C addresses = ',scan_I2C())  # scan and print I2C addresses 
print ('chip id: ',read_chipid())  

#set device data acquisition options
# write ctrl_meas register 0xF4
# bit 7,6,5 001 - set temp oversampling x1
# bit 4,3,2 001 - set pres oversampling x1
# bit 1,0    11 - set power mode to normal mode
buf = b'\x27' # write 001 001 11 to 0xF4
i2c.writeto_mem(slave_addr, 0xF4, buf)

  
caldata = read_calib()  # read calibration data
# unpack calibration data
REGISTER_FORMAT = '<h'  # < = little endian h=2 bytes
dig_T1 = ustruct.unpack_from(REGISTER_FORMAT, caldata, 0)[0]
# convert dig_T1 to unsigned
dig_T1 = dig_T1 & 0xFFFF
dig_T2 = ustruct.unpack_from(REGISTER_FORMAT, caldata, 2)[0]
dig_T3 = ustruct.unpack_from(REGISTER_FORMAT, caldata, 4)[0]
# convert P1 to unsigned
dig_P1 = ustruct.unpack_from(REGISTER_FORMAT, caldata, 6)[0] 
dig_P1 = dig_P1 & 0xFFFF
dig_P2 = ustruct.unpack_from(REGISTER_FORMAT, caldata, 8)[0]
dig_P3 = ustruct.unpack_from(REGISTER_FORMAT, caldata, 10)[0]
dig_P4 = ustruct.unpack_from(REGISTER_FORMAT, caldata, 12)[0]
dig_P5 = ustruct.unpack_from(REGISTER_FORMAT, caldata, 14)[0]
dig_P6 = ustruct.unpack_from(REGISTER_FORMAT, caldata, 16)[0]
dig_P7 = ustruct.unpack_from(REGISTER_FORMAT, caldata, 18)[0]
dig_P8 = ustruct.unpack_from(REGISTER_FORMAT, caldata, 20)[0]
dig_P9 = ustruct.unpack_from(REGISTER_FORMAT, caldata, 22)[0]

# print out calibration parameters
print ('dig_T1= ',dig_T1)
print ('dig_T2= ',dig_T2)
print ('dig_T3= ',dig_T3)
print ('dig_P1= ',dig_P1)
print ('dig_P2= ',dig_P2)
print ('dig_P3= ',dig_P3)
print ('dig_P4= ',dig_P4)
print ('dig_P5= ',dig_P5)
print ('dig_P6= ',dig_P6)
print ('dig_P7= ',dig_P7)
print ('dig_P8= ',dig_P8)
print ('dig_P9= ',dig_P9)



# print pressure and temperature in continuous loop
display_continuous()


























