import os
import time 

def Init_Sonic():
	os.system("echo \"24\" > /sys/class/gpio/export")
	os.system("echo \"out\" > /sys/class/gpio/gpio24/direction")
	os.system("echo \"0\" > /sys/class/gpio/gpio24/value ")

	os.system("echo \"23\" > /sys/class/gpio/export")
	os.system("echo \"in\" > /sys/class/gpio/gpio23/direction")

def Get_Distance():
	initial_Time=0
	end_Time=0
	distance=0
	x=0
	while x < 3:

		os.system("echo \"1\" > /sys/class/gpio/gpio24/value ")
		time.sleep(0.000001)
		os.system("echo \"0\" > /sys/class/gpio/gpio24/value ")
	
		initial_Time= time.time()
		while int(open("/sys/class/gpio/gpio23/value","r").read().strip()) == 1:
			end_Time= time.time()
		
		distance +=((end_Time-initial_Time) * 17150 ) 
		x+=1
	distance=distance/3
	#if distance > 2 and distance < 400:
	print("Distance = "+str(int(distance)) + " cm\r\n")
