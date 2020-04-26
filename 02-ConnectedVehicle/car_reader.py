import serial
import time
ser = serial.Serial('/dev/cu.usbserial', 38400, timeout=1, bytesize=8, parity=serial.PARITY_NONE)
time.sleep(1)
ser.write("atz\r\n")
print(ser.readline())
rpm = 0
speed = 0
temp = 0
initializing = True
time.sleep(1)

# Import SDK packages
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient

myMQTTClient = AWSIoTMQTTClient("myClientID-kombi-rasp-23121231")
myMQTTClient.configureEndpoint("a2p4fyajwx9lux-ats.iot.us-east-1.amazonaws.com", 8883)
myMQTTClient.configureCredentials("/Users/vsenger/Documents/root-CA.crt", "/Users/vsenger/Downloads/a48c4c65d8-private.pem.key", "/Users/vsenger/Downloads/a48c4c65d8-certificate.pem.crt")
myMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
myMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
myMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
myMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec
myMQTTClient.connect()



while initializing:
	ser.write("010c\r\n")
	r = ser.readline();
	if(r.startswith("010c")):
		initializing= False
	else:
		time.sleep(2)

while True:
	ser.write("010c\r\n")
	rpm_h = ser.readline()
	#print(rpm_h)
	#print(len(rpm_h))
	if(rpm_h.startswith("010c")):
		try:
			rpm_1 = rpm_h[11:13]
			rpm_2 = rpm_h[14:16]
			rpm = int(rpm_1 + rpm_2, 16)/4
			print("rpm " + str(rpm))
		except ValueError:
			print("valor errado")			
	else:
		print("bus initializing")
	time.sleep(1)
	ser.write("010d\r\n")
	speed_h = ser.readline()
	#print(speed_h)
	#print(len(speed_h))
	if(speed_h.startswith("010d")):
		try:
			speed_1 = speed_h[11:13]
			speed = int(speed_1, 16)
			print("speed " + str(speed))
		except ValueError:
			print("valor errado")
	else:
		print("bus initializing.")
	time.sleep(1)
	
	ser.write("0105\r\n")
	temp_h = ser.readline()
	#print(speed_h)
	#print(len(speed_h))
	if(temp_h.startswith("0105")):
		try:
			temp_1 = temp_h[11:13]
			temp = int(temp_1, 16) - 40
			print("temperature " + str(temp))
		except ValueError:
			print("valor errado")
	else:
		print("bus initializing...")

	
	myMQTTClient.publish("connected_vehicle",'{ "rpm" : ' + str(rpm) + ', "speed" : ' + str(speed) + ',"temperature : ' + str(temp) + '}', 0)
	time.sleep(1)


