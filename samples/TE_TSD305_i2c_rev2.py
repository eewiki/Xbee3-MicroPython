# Micropython code example for Digi International Xbee3
# 802.15.4 module interface to TE Weather Shield TSD305
# contactless temperature sensor over I2C
# 


from micropython import const
import utime
import ustruct
import machine

# set i2c clock to 100KHz
# TE TSD305 i2c adress = 0x1E
i2c = machine.I2C(1, freq=100000) 
slave_addr = 0x1E  


# scan i2c bus for active addresses
def scan_I2C():
  devices = i2c.scan()
  return devices
  
print ('i2c address scan = ', scan_I2C())  


def unsign16(): # read 16 bit unsigned data from eeprom
  i2c.writeto(slave_addr, data) 
  utime.sleep(0.001)
  rawdata = i2c.readfrom(slave_addr, 3) #1 ack byte and 2 data bytes
  value = int.from_bytes(rawdata, "big") # use builtin to convert to integer
  value = value & 0xFFFF # zero out 1st ack byte
  return value


def sign16(): # read 16 bit signed data from eeprom
  i2c.writeto(slave_addr, data) 
  utime.sleep(0.001)
  rawdata = i2c.readfrom(slave_addr, 3) #1 ack byte and 2 data bytes
  value = ustruct.unpack_from('>h', rawdata, 1)[0] #use 2nd and 3rd bytes for signed integer
  return value


# read and print lot#
data = bytearray([const(0x00)])
print ('lot# ', unsign16())

# read and print serial#
data = bytearray([const(0x01)])
print ('serial# ', unsign16())

# read and print max sensor temp
data = bytearray([const(0x1B)])
max_st = sign16()
print ('max sensor temp ', max_st)

# read and print min sensor temp
data = bytearray([const(0x1A)])
min_st = sign16()
print ('min sensor temp ', min_st) 

# read eeprom: min object temperature
data = bytearray([const(0x1C)])
min_obj = sign16()
print ('min object temp ', min_obj) 

# read eeprom: max object temperature
data = bytearray([const(0x1D)])
max_obj = sign16()
print ('max object temp ', max_obj) 

# read eeprom temp coefficient (32 bit floating point)
data = bytearray([const(0x1E)])
H_word = sign16()
data = bytearray([const(0x1F)])
L_word = sign16()
test = ustruct.pack('hh',L_word, H_word) #32 bit float format (L-word, H-word)
temp_c = ustruct.unpack('f', test)[0] #this works!!!!!!!![0] turns result into value
print ('temp coef = ',temp_c)

# read eeprom reference temp (32 bit floating point)
data = bytearray([const(0x20)])
H_word = sign16()
data = bytearray([const(0x21)])
L_word = sign16()
test = ustruct.pack('hh',L_word, H_word) #32 bit float format (L-word, H-word)
ref_t = ustruct.unpack('f', test)[0] #this works!!!!!!!![0] turns result into value
print ('reftemp = ',ref_t)


# read eeprom comp coef k4 (32 bit floating point)
data = bytearray([const(0x22)])
H_word = sign16()
data = bytearray([const(0x23)])
L_word = sign16()
test = ustruct.pack('hh',L_word, H_word) #32 bit float format (L-word, H-word)
cc_k4 = ustruct.unpack('f', test)[0] #turns result into value
print ('cc k4 = ',cc_k4)


# read eeprom comp coef k3 (32 bit floating point)
data = bytearray([const(0x24)])
H_word = sign16()
data = bytearray([const(0x25)])
L_word = sign16()
test = ustruct.pack('hh',L_word, H_word) #32 bit float format (L-word, H-word)
cc_k3 = ustruct.unpack('f', test)[0] #turns result into value
print ('cc k3 = ',cc_k3)

# read eeprom comp coef k2 (32 bit floating point)
data = bytearray([const(0x26)])
#print ('H-word ',sign16())
H_word = sign16()
data = bytearray([const(0x27)])
#print ('L-word ',sign16())
L_word = sign16()
test = ustruct.pack('hh',L_word, H_word) #32 bit float format (L-word, H-word)
cc_k2 = ustruct.unpack('f', test)[0] #turns result into value
print ('cc k2 = ',cc_k2)

# read eeprom comp coef k1 (32 bit floating point)
data = bytearray([const(0x28)])
H_word = sign16()
data = bytearray([const(0x29)])
L_word = sign16()
test = ustruct.pack('hh',L_word, H_word) #32 bit float format (L-word, H-word)
cc_k1 = ustruct.unpack('f', test)[0] #turns result into value
print ('cc k1 = ',cc_k1)

# read eeprom comp coef k0 (32 bit floating point)
data = bytearray([const(0x2A)])
H_word = sign16()
data = bytearray([const(0x2B)])
L_word = sign16()
test = ustruct.pack('hh',L_word, H_word) #32 bit float format (L-word, H-word)
cc_k0 = ustruct.unpack('f', test)[0] #turns result into value
print ('cc k0 = ',cc_k0)

# read eeprom ADC coef k4 (32 bit floating point)
data = bytearray([const(0x2E)])
H_word = sign16()
data = bytearray([const(0x2F)])
L_word = sign16()
test = ustruct.pack('hh',L_word, H_word) #32 bit float format (L-word, H-word)
a_k4 = ustruct.unpack('f', test)[0] #turns result into value
print ('adc k4 = ',a_k4)

# read eeprom ADC coef k3 (32 bit floating point)
data = bytearray([const(0x30)])
H_word = sign16()
data = bytearray([const(0x31)])
L_word = sign16()
test = ustruct.pack('hh',L_word, H_word) #32 bit float format (L-word, H-word)
a_k3 = ustruct.unpack('f', test)[0] #turns result into value
print ('adc k3 = ',a_k3)

# read eeprom ADC coef k2 (32 bit floating point)
data = bytearray([const(0x32)])
H_word = sign16()
data = bytearray([const(0x33)])
L_word = sign16()
test = ustruct.pack('hh',L_word, H_word) #32 bit float format (L-word, H-word)
a_k2 = ustruct.unpack('f', test)[0] #turns result into value
print ('adc k2 = ',a_k2)

# read eeprom ADC coef k1 (32 bit floating point)
data = bytearray([const(0x34)])
H_word = sign16()
data = bytearray([const(0x35)])
L_word = sign16()
test = ustruct.pack('hh',L_word, H_word) #32 bit float format (L-word, H-word)
a_k1 = ustruct.unpack('f', test)[0] #turns result into value
print ('adc k1 = ',a_k1)

# read eeprom ADC coef k0 (32 bit floating point)
data = bytearray([const(0x36)])
H_word = sign16()
data = bytearray([const(0x37)])
L_word = sign16()
test = ustruct.pack('hh',L_word, H_word) #32 bit float format (L-word, H-word)
a_k0 = ustruct.unpack('f', test)[0] #turns result into value
print ('adc k0 = ',a_k0)



#  #############################  main loop  ##########################################


while True:
  i2c.writeto(slave_addr, b'\xAF') #read ADC command
  utime.sleep(0.1) #wait for ADC
  r_adc = i2c.readfrom(slave_addr, 7) #store ADC (1 ack byte, 3 object temp bytes, 3 sensor temp bytes)
  s_adc = r_adc[4]*65536 + r_adc[5]*256 + r_adc[6] #raw sensor temp
  t_sens = ((s_adc)/16777216 * 105) - 20 # sensor temp
  TCF = 1 + ((t_sens - ref_t) * temp_c) #Temperature Correction Factor
  Offset = (cc_k4 * (t_sens**4)) + (cc_k3 * (t_sens**3)) + (cc_k2 * (t_sens**2)) + (cc_k1 * t_sens) + cc_k0
  Offset = Offset * TCF
  o_adc = r_adc[1]*65536 + r_adc[2]*256 + r_adc[3] # object temp adc value
  c_adc = (Offset + o_adc - 8388608)/TCF #ADCcompTCF
  t_obj = (a_k4 * (c_adc**4)) + (a_k3 * (c_adc**3)) + (a_k2 * (c_adc**2)) + (a_k1 * c_adc) + a_k0
  print ('sensor temp = ', t_sens)
  print ('object temp = ', t_obj)
  utime.sleep(2.0)






