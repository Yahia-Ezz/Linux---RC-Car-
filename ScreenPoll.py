#Imports UltraSonic Functions from UltraSonic.py
from  UltraSonic import Get_Distance,Init_Sonic

#import os to use linux shell Commands from within the python code.
import os

#import time for delay and pulse
import time

#import curses for terminal  character polling
import curses



# Max delay time  0.01  for a resonable Responnse time
# Min delay time  0.001 for a resonable Responnse time
# Tilt Fix = 0.0001 within the delay function to compensate for motors physical asymmetry

#Hardware Connections :
#		GPIO4  ->>  CH3
#		GPIO17 ->>  CH1
#		GPIO27 ->>  CH2
# 		GPIO22 ->>  CH4

#Initialize the GPIO of the driver to output and set it to low.
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



#Run the RC car forward by setting a pulse with the set delay. and the time.sleep function is to compensate for the tilt of the motors. 
def PULSE_FWD(delay):
	os.system("echo \"1\" > /sys/class/gpio/gpio4/value")
        os.system("echo \"1\" > /sys/class/gpio/gpio27/value")
	time.sleep(delay)
 	os.system("echo \"0\" > /sys/class/gpio/gpio4/value")
	time.sleep(0.0001)
	os.system("echo \"0\" > /sys/class/gpio/gpio27/value")


#Run the RC car backward by setting a pulse with the set delay. and the time.sleep function is to compensate for the tilt of the motors.
def PULSE_BKWD(delay):
	os.system("echo \"1\" > /sys/class/gpio/gpio22/value")
        os.system("echo \"1\" >/sys/class/gpio/gpio17/value")
        time.sleep(delay)
        os.system("echo \"0\" > /sys/class/gpio/gpio22/value")
        time.sleep(0.0001)
        os.system("echo \"0\" >/sys/class/gpio/gpio17/value")
        

#Run the RC car to turn right by setting a pulse with that runs both motors in different directions opposing to each other.
def PULSE_RIGHT(delay):
	os.system("echo \"1\" >/sys/class/gpio/gpio22/value")
	os.system("echo \"1\" >/sys/class/gpio/gpio4/value")
        time.sleep(delay)
        os.system("echo \"0\" >/sys/class/gpio/gpio22/value")
 	os.system("echo \"0\" >/sys/class/gpio/gpio4/value")  


#Run the RC car to turn left by setting a pulse with that runs both motors in different directions opposing to each other.	     	
def PULSE_LEFT(delay):
	os.system("echo \"1\" > /sys/class/gpio/gpio27/value")
        os.system("echo \"1\" > /sys/class/gpio/gpio17/value")
	time.sleep(delay)
        os.system("echo \"0\" > /sys/class/gpio/gpio27/value")
        os.system("echo \"0\" > /sys/class/gpio/gpio17/value")



									#Program Start Here#
#-------------------------------------------------------------------------------------------------------------------------------#
screen = curses.initscr()	#Initialize Curses on current terminal
curses.noecho()				#Turn Keyboard echo off
curses.cbreak()				#Turn on instant key response (no waiting)  
screen.keypad(True)			#Use special values for cursor keys


GPIO_voidInitialize()		#Initialize GPIO
Init_Sonic()				#Initialize Ultrasonic

Current_Speed=0				#Set starting speed with 0 (lowest)
Race_Mode=1					#Set RaceMode flag as disabled (Inverted Logic)
Reading_Interval=0			#Take an UltraSonic reading after a certain Number of Characters is read  

try:
        
	while True:
	    Reading_Interval += 1							#After each character read from terminal increment Counter by 1.
            if Reading_Interval > 100 and Race_Mode:	#After a 100 Readings call the ultrasonic function and prinnt the read value on the screen.
	    	Get_Distance()								#Read Value. 	
            	Reading_Interval=0						#Reset Counter
	    char = screen.getch()							#Store typed character into a variable.
           													
            if char == ord('q'):						#If input character is the "q" key
                break									#Quit Control Script.
           
            elif char == curses.KEY_UP:					#If input character is the "q" key
                PULSE_FWD(0.001*Current_Speed)				#Call the pulse forward function with a (Speed*Constant Number)
		#if screen.getch()== curses.KEY_RIGHT:
			#print("Swing")
			#PULSE_FWD(0.001*(Speed))
		#else:
	    elif char == curses.KEY_DOWN:					#If input character is the DOWN key
                PULSE_BKWD(0.001*Current_Speed)				#Call the pulse backward function with a (Speed*Constant Number) 
          
            elif char == curses.KEY_RIGHT:				#If input character is the RIGHT key
           	PULSE_RIGHT(0.001*Current_Speed) 				#Call the pulse RIGHT function with a (Speed*Constant Number)
	    
	    elif char == curses.KEY_LEFT:					#If input character is the LEFT key
                PULSE_LEFT(0.001*Current_Speed)				#Call the pulse LEFT function with a (Speed*Constant Number)
        
            elif char == 10:							#If input character is the ENTER key
		Get_Distance()										#Take an instant reading from the ultrasonic.
	    
	    elif char == 97:								#If input character is the "a" key
		
		if Current_Speed < 10:								 #Checks if the Speed variable is less than the max Gear(10),IF true 
			Current_Speed +=1								 		#Increase speed by 1 .
			print("Current Speed ="+str(Current_Speed)+"\r")		#Print on the screen the current Speed Gear Value.
		else :
			print("Max Speed Reached Gear 10\r")					#If Max speed is already reached, Notify the user that this is the max speed.
	    
	    elif char == 122:									#Checks if the Speed variable is higher than the max Gear(0),IF true.

		if Current_Speed > 0:									#Checks if the Speed vairable is bigger than 0 ,IF true 
			Current_Speed -=1										#Decrease speed variable by 1.  
			print("Current Speed ="+str(Current_Speed)+"\r")		#Print the current speed gear for the user.
		else :
			print("Minimum Speed Reached Gear 0 \r")			#If Min speed is already reached, Notify the user that this is the min speed.
	    
	    elif char == 114:									#IF te input character is the "r" key.  
	    	if Race_Mode == 1:									#checks if the race mode flag is set
			print("Race Mode Armed\r")							 #Notify the user that the Race mode is activated and max speed is set.
			Race_Mode = 0
			Current_Speed=10 
 										
		else:												 #checks if the race mode flag is cleared.       
			print("Race Mode Disarmed\r")					#Notify the user that the Race Mode has been disabled and minimum speed has been set 
			Race_Mode = 1
			Current_Speed=0 								

			
finally:
    #Close down curses properly, inc turn echo back on!
    curses.nocbreak(); 
    screen.keypad(0); 
    curses.echo()
    curses.endwin()
