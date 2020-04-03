# Micropython code example for Digi International Xbee3
# Zigbee module interface to Amphenol T9602 
# humidity/temperature sensor over I2C
# this version just interfaces to T9602 sensor
# and sends readings to Zigbee coordinator
# rev2 modified for home coordinator


from micropython import const
import utime
import ustruct
import machine
import sys
import xbee

FWver = "T9602only_rev2"

# Amphenol T9602 info
a_address = 0x28 #T9602 sensor i2c address
p_zero = 0x00 # "zero" payload



#Zigbee coordinator adddress Digi-Key coordinator
#TARGET_64BIT_ADDR = b'\x00\x13\xA2\x00\x41\xA7\xAD\xBC'
#Zigbee coordinator adddress Home coordinator
TARGET_64BIT_ADDR = b'\x00\x13\xA2\x00\x41\xAA\xCB\xBA'

# set i2c clock to 100KHz
i2c = machine.I2C(1, freq=100000) 

# scan i2c bus for active addresses
def scan_I2C():
  devices = i2c.scan()
  return devices


  

# **************** Main Program *********************************
print(FWver) #print firmware version

print ('i2c scan addresses found: ',scan_I2C())


# check zigbee connection
while xbee.atcmd("AI") != 0:
    print("#Trying to Connect...")
    utime.sleep(0.5)

print("#Online...")



while True:
  #read amphenol T9602 sensor for temp and humidity
  try:
    slave_addr = a_address #set T9602 i2c address
    data = bytearray([p_zero]) 
    i2c.writeto(slave_addr, data) # write "0"
    t96 = i2c.readfrom(slave_addr, 4) #read 4 bytes from T9602
    # first 2 bytes humidity, 2nd 2 bytes temp in C
    t96h = (((t96[0]&0x3F) << 8) + t96[1])/16384*100
    t96t = ((((t96[2] * 64) + (t96[3] >> 2)))/16384*165) - 40
    fTemp = (t96t*9/5) + 32 # convert to fahrenheit
    print ('T9602 Humidity = ', '%.1fRH' % t96h)
    print ('T9602 Temp = ', '%.1fC' % t96t)
    print ('T9602 Temp = ', '%.1fF' % fTemp)
  except:
    print('T9602 read failed')
    
 
  # build TH sensor data payload
  try:
    time_snapshot = str(utime.ticks_cpu())
    print_TH = "T9602:" + time_snapshot + ":Humidity:" + str(t96h) + "%:Temp:" + str(fTemp) + "F:#" #T9602 humidity and temp
    #print_PTH = "PTH_sensor:" + time_snapshot + ":Press:" + str(Pres) + "mB:Temp:" + str(fTemp) + "F:Humidity:" + str(RH) + "%:#" #remove MCP9808
    print(print_TH)
  except:
    print("sensor payload build failed")
    
   
  #transmit Temp Humidity data over Zigbee to coordinator
  try:
    xbee.transmit(TARGET_64BIT_ADDR, print_TH)
    #xbee.transmit(ROUTER_64BIT_x1B2D, print_TH)
    print("send data to coordinator")
  except:
    print("xbee coordinator transmit failed")
  
  utime.sleep(5.0) #short delay between transmit
  

  



















































