# below 802.15.4 wireless protocol code based on Digi International
# example code for network communication between nodes for end device
import xbee, time
# Utility functions to perform XBee3 802.15.4 operations
from machine import Pin
# pin function needed for sensor
def format_eui64(addr):
	return ':'.join('%02x' % b for b in addr)

def format_packet(p):
	type = 'Broadcast' if p['broadcast'] else 'Unicast'
	print("%s message from EUI-64 %s (network 0x%04X)" % 
		(type, format_eui64(p['sender_eui64']), p['sender_nwk']))
	print("from EP 0x%02X to EP 0x%02X, Cluster 0x%04X, Profile 0x%04X:" %
		(p['source_ep'], p['dest_ep'], p['cluster'], p['profile']))
	print(p['payload'],"\n")

def network_status():
	# If the value of AI is non zero, the module is not connected to a network
	return xbee.atcmd("AI")
print("Joining network as an end device...")
xbee.atcmd("NI", "End Device")
network_settings = {"CE": 0, "A1": 4, "CH": 0x13, "ID": 0x3332, "EE": 0}
for command, value in network_settings.items():
	xbee.atcmd(command, value)
xbee.atcmd("AC")  # Apply changes
time.sleep(1)

while network_status() != 0:
	time.sleep(0.1)
print("Connected to Network\n")

last_sent = time.ticks_ms()
interval = 1000  # How often to send a message in ms

# read digital input D12 and set D19 output
D12 = Pin("D12", Pin.IN, Pin.PULL_UP)
D19 = Pin("D19", Pin.OUT, value=0)

# Start the transmit/receive loop
print("Sending temp data every {} seconds".format(interval/1000))
while True:
	p = xbee.receive()
	if p:
		format_packet(p)
	else:
		# Transmit sensor state if ready
		if time.ticks_diff(time.ticks_ms(), last_sent) > interval:
				# TE sensor state is monitored by D12 input
				sensor = str(D12.value())
				D19.value(D12.value())
				print("\tsending sensor state= " + sensor)
				try:
					xbee.transmit(xbee.ADDR_COORDINATOR, sensor)
				except Exception as err:
					print(err)
				last_sent = time.ticks_ms()
		time.sleep(0.25)






