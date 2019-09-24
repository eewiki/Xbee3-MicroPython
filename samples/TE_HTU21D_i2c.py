# Micropython code example for Digi International Xbee3
# 802.15.4 module interface to TE Weather Shield HTU21D
# digital humidity and temperature sensor over I2C
# XB3 mounted in Grove dev board 
#  
#
 


from micropython import const
import utime
import ustruct
import machine

# set register format for HTU21D
REGISTER_FORMAT = '>h' # ">" big endian, "h" 2 bytes
REGISTER_SHIFT = 4 # rightshift 4 for 12 bit resolution

r_user = const(0xE7) # read user register command
w_user = const(0xE6) # write user register command
t_temp = const(0xE3) # trigger temperature measurement, hold master
t_humi = const(0xE5) # trigger humidity measurement, hold master


# set i2c clock to 100KHz
# TE HTU21D i2c adress = 0x40
i2c = machine.I2C(1, freq=100000) 
slave_addr = 0x40  

# scan i2c bus for active addresses
def scan_I2C():
  devices = i2c.scan()
  return devices



#read user register command 0xE7, default value = 0x02
# default resolution RH 12bit, T 14bit
def read_user():
  data = bytearray([r_user])
  i2c.writeto(slave_addr, data)
  value = i2c.readfrom(slave_addr, 1)
  return value

print ('user register: ',read_user())

#read temperature: send trigger temp command 0xE3
# read 2 temp bytes and shift 2 places for 14bit
def read_temp():
  data = bytearray([t_temp])
  i2c.writeto(slave_addr, data)
  raw_t = i2c.readfrom(slave_addr, 2)
  REGISTER_SHIFT = 2
  temp = ustruct.unpack(REGISTER_FORMAT, raw_t)[0] >> REGISTER_SHIFT
  value = ((temp/16384)*175.72) - 46.85 # calculate temp in celsius
  return value



#read rh: send trigger rh command 0xE5
def read_rh():
  data = bytearray([t_humi])
  i2c.writeto(slave_addr, data)
  raw_rh = i2c.readfrom(slave_addr, 2) # raw RH is 2 bytes
  raw_value = int.from_bytes(raw_rh, "big") # use builtin to convert to integer
  rh_tc = (-0.15)*(25 - read_temp())# RH temp compensation
  rh_value = (((raw_value/65536)*125) - 6) + rh_tc # calculate RH
  return rh_value
  



# **************** Main Program *********************************

print ('i2c scan addresses found: ',scan_I2C())
print ('user register: ',read_user())

while True:
  print ('temp in celsius: ','%.1fC' % read_temp())
  print ('relative humidity: ', '%.1f percent' % read_rh())
  utime.sleep(5.0)
  










