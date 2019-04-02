from  UltraSonic import Get_Distance,Init_Sonic
import os
import time
import curses
#max delay 0.01
#min delay 0.001 Tilt Fix = 0.0001
#connections :
#		GPIO4  ->>  CH3
#		GPIO17 ->>  CH1
#		GPIO27 ->>  CH2
# 		GPIO22 ->>  CH4


def GPIO_voidInitialize():
        os.system("echo \"4\" > /sys/class/gpio/export")
        os.system("echo \"out\" > /sys/class/gpio/gpio4/direction")
	os.system("echo \"0\" > /sys/class/gpio/gpio4/value")
	os.system("echo \"17\" > /sys/class/gpio/export")
	os.system("echo \"out\" > /sys/class/gpio/gpio17/direction")
	os.system("echo \"0\" >/sys/class/gpio/gpio17/value")
	os.system("echo \"27\" > /sys/class/gpio/export")
        os.system("echo \"out\" > /sys/class/gpio/gpio27/direction")
        os.system("echo \"0\" > /sys/class/gpio/gpio27/value")
        os.system("echo \"22\" > /sys/class/gpio/export")
        os.system("echo \"out\" > /sys/class/gpio/gpio22/direction")
        os.system("echo \"0\" >/sys/class/gpio/gpio22/value")

def PULSE_FWD(delay):
	os.system("echo \"1\" > /sys/class/gpio/gpio4/value")
        os.system("echo \"1\" > /sys/class/gpio/gpio27/value")
	time.sleep(delay)
 	os.system("echo \"0\" > /sys/class/gpio/gpio4/value")
	time.sleep(0.0001)
	os.system("echo \"0\" > /sys/class/gpio/gpio27/value")

def PULSE_BKWD(delay):
	os.system("echo \"1\" > /sys/class/gpio/gpio22/value")
        os.system("echo \"1\" >/sys/class/gpio/gpio17/value")
        time.sleep(delay)
        os.system("echo \"0\" > /sys/class/gpio/gpio22/value")
        time.sleep(0.0001)
        os.system("echo \"0\" >/sys/class/gpio/gpio17/value")
        

def PULSE_RIGHT(delay):
	os.system("echo \"1\" >/sys/class/gpio/gpio22/value")
	os.system("echo \"1\" >/sys/class/gpio/gpio4/value")
        time.sleep(delay)
        os.system("echo \"0\" >/sys/class/gpio/gpio22/value")
 	os.system("echo \"0\" >/sys/class/gpio/gpio4/value")       	
def PULSE_LEFT(delay):
	os.system("echo \"1\" > /sys/class/gpio/gpio27/value")
        os.system("echo \"1\" > /sys/class/gpio/gpio17/value")
	time.sleep(delay)
        os.system("echo \"0\" > /sys/class/gpio/gpio27/value")
        os.system("echo \"0\" > /sys/class/gpio/gpio17/value")




# Get the curses window, turn off echoing of keyboard to screen, turn on
# instant (no waiting) key response, and use special values for cursor keys
screen = curses.initscr()
curses.noecho()
curses.cbreak()
screen.keypad(True)
GPIO_voidInitialize()
Init_Sonic()
Speed=0
Race_Mode=1
xqt=0
try:
        
	while True:
	    xqt += 1
            if xqt > 100 and Race_Mode:
	    	Get_Distance()	
            	xqt=0
	    char = screen.getch()
            if char == ord('q'):
                break
            elif char == curses.KEY_UP:
		#if screen.getch()== curses.KEY_RIGHT:
			#print("Swing")
			#PULSE_FWD(0.001*(Speed))
		#else:
                PULSE_FWD(0.001*Speed)
	    elif char == curses.KEY_DOWN:
                PULSE_BKWD(0.001*Speed)
            elif char == curses.KEY_RIGHT:
           	PULSE_RIGHT(0.001*Speed) 
	    elif char == curses.KEY_LEFT:
                PULSE_LEFT(0.001*Speed)
            elif char == 10:
		Get_Distance()
	    elif char == 97:
		if Speed < 10:
			Speed +=1
			print("Current Speed ="+str(Speed)+"\r")
		else :
			print("Max Speed Reached Gear 10\r")
	    elif char == 122:
		if Speed > 0:
			Speed -=1
			print("Current Speed ="+str(Speed)+"\r")
		else :
			print("Minimum Speed Reached Gear 0 \r")
	    elif char == 114:
	    	if Race_Mode == 1:
			print("Race Mode Armed\r")
			Race_Mode = 0 
		else:
			print("Race Mode Disarmed\r")
			Race_Mode = 1
			
finally:
    #Close down curses properly, inc turn echo back on!
    curses.nocbreak(); screen.keypad(0); curses.echo()
    curses.endwin()
