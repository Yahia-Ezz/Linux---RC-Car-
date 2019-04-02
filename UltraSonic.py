#import os to use linux shell Commands from within the python code.
import os

#import time for delay and pulse
import time 

#Initialize the GPIO of the ultrasonic driver to output/input and set it to low.
def Init_Sonic():
	os.system("echo \"24\" > /sys/class/gpio/export")
	os.system("echo \"out\" > /sys/class/gpio/gpio24/direction")
	os.system("echo \"0\" > /sys/class/gpio/gpio24/value ")

	os.system("echo \"23\" > /sys/class/gpio/export")
	os.system("echo \"in\" > /sys/class/gpio/gpio23/direction")
#Function that triggers the ultrasonic module and print a reading out on the terminal 
def Get_Distance():
	initial_Time=0			#set initial starting time to 0.
	end_Time=0			#Set the end pulse  time to 0
	distance=0			#Set initial distance to 0.
	x=0				#loop variable for a for multiple averaged readings.
	while x < 3:
	 #Send a pulse to trigger the Ultrasonic Module
		os.system("echo \"1\" > /sys/class/gpio/gpio24/value ")			
		time.sleep(0.000001)
		os.system("echo \"0\" > /sys/class/gpio/gpio24/value ")
	 #Set initial starting time to current system time.
		initial_Time= time.time()
		
	 #keep setting endtime variable to current system time untill the echo pin is low
		while int(open("/sys/class/gpio/gpio23/value","r").read().strip()) == 1:
			end_Time= time.time()
	 #Take the speed of sound and set an average for 3 readings then print it on the sceen. 		
		distance +=((end_Time-initial_Time) * 17150 ) 
		x+=1
	distance=distance/3
	#if distance > 2 and distance < 400:
	print("Distance = "+str(int(distance)) + " cm\r\n")
