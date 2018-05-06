"""
"   resMon - PC monitoring HW/SW
"   using Arduino UNO, 128x64 monochromatic OLED display and custom Python script
"   Display your PC´s usage easily with these simple programs and very simple HW
"   ---WIRING---
"   Plug your OLED display into breadboard. Connect Vdd of OLED to +5V on Arduino, GND to GND of Arduino, SCL to A5 and SDA to A4
"   ---GETTING IT TO WORK---
"   Download U8Glib from https://github.com/olikraus/u8glib 
"   Upload *resMon_NUMS* code to your Arduino board, DO NOT open serial monitor
"   Open and configure *this* file, then execute it
"   You should have everything, enjoy :)
"   ---OPEN SOURCE LICENSE---
"                               MIT License
"              
"              Copyright (c) 2018 Radovan "N3ttX" Behýl
"              
"              Permission is hereby granted, free of charge, to any person obtaining a copy
"              of this software and associated documentation files (the "Software"), to deal
"              in the Software without restriction, including without limitation the rights
"              to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
"              copies of the Software, and to permit persons to whom the Software is
"              furnished to do so, subject to the following conditions:
"              
"              The above copyright notice and this permission notice shall be included in all
"              copies or substantial portions of the Software.
"              
"              THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
"              IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
"              FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
"              AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
"              LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
"              OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
"              SOFTWARE.
"""
"""
"   ---CONFIGURATION GUIDE---
"   1.) !!RECOMMENDED to leave DEFAULT!! Set your baudrate (ser.baudrate) to your value (choosen as well in Arduino script file, they HAVE TO BE THE SAME)
"   2.) Set your COM port (ser.port) to COM port that Arduino is connected to. You can get this information here -> http://bit.do/arduinoComPortGuide
"   3.) If you have only 1 drive, delete lines marked with three x´s ("XXX") abd from "serialDataStr" delete "hddStr"
"   4.) If you have more than 2 drives, you are unlucky, because no more information can be fitted onto OLED screen. I am working on version with multiple HDDs as well as standalone diskMon software
"""

#import libraries (psutil for monitoring PC and pyserial for sending data throught serial interface
import psutil
import serial

#pySerial settings
ser = serial.Serial()                                           #make instance of Serial
ser.baudrate = 9600                                             #set baud to 9600 (9600b/s)
ser.port = "COM6"                                               #replace COM6 with your Arduino port; set serial port
ser.open()                                                      #open the port

#system info that doesn´t need to be refreshed
coreCount = psutil.cpu_count(logical = False)                   #get number of PHYSICAL cores
cores = "(" + str(coreCount) + "C)"                             #make it as a string with () and "C"
totalMem = round(psutil.virtual_memory().total / 1073741824)    #get total memory size, which is divided by 1073741824 (GIGI constant, actual binary size) and rounded up (so it wont work properly with systems that have less than 1GB RAM)
if totalMem < 10:
    totalMemStr = " (" + str(totalMem) + "G)"                   #if RAM is less that 10GB, put artificial character (space) before actual text (keeps arduino code simpler)
else:
    totalMemStr = "(" + str(totalMem) + "G)"                    #if RAM is more or equal than 10GB, write it without space (i defined 5 characters per information (if not stated else) INCLUDING parenthesis "()")

while(1):                                                       #infinite loop, we don´t want to stop this program.. and don´t worry, it will not consume lot of resources, read next line to understand why
    cpu = psutil.cpu_percent(interval=1.2)                      #get usage of CPU in percentage with interval of 1.2s (that actually slow our entire code to be executed once in 1.2s so thats why ^ works). 1.2s is set due to Arduino´s serial buffer being pretty slow and it takes a lot of time to read from it.. also it takes time to redraw the OLED and NOTHING below 1.2s will properly work (at least on Arduino UNO)
    mem = psutil.virtual_memory().percent                       #get usage of RAM in percentage
    sdd = 100-psutil.disk_usage("C:").percent                   #get used space of C: disk (in my case SSD); since we get USED space, we need to substract it from 100(%) and we got FREE space
    hdd = 100-psutil.disk_usage("D:").percent                   #   XXX    the same here, i have 2 drives (SSD and HDD)
                                                                #we need to parse floats (decimal numbers from psutil) to strings
    if cpu < 10:
        cpuStr = "  " + str(cpu)                                #if CPU usage is under 10%, put 2 artificial characters (spaces) before the value.. as i mentioned, i set every information to be 5 characters including parenthesis and/or decimal places, so we need to fill resot of the space with spaces (also, its prettier)
    elif cpu < 100:
        cpuStr = " " + str(cpu)                                 #here the same, but only 1 space. because 98.5 have only 4 characters.. 
    else:
        cpuStr = str(cpu)                                       #100.0 is 5 characters so there is no need to put spaces in before..

    if mem < 10:
        memStr = "  " + str(mem)                                #the same as in CPU
    elif mem < 100:
        memStr = " " + str(mem)
    else:
        memStr = str(mem)

    if hdd < 10:                                                #   XXX
        hddStr = "  " + str(hdd)                                #   XXX
    elif hdd < 100:                                             #   XXX
        hddStr = " " + str(hdd)                                 #   XXX
    else:                                                       #   XXX
        hddStr = str(hdd)                                       #   XXX

    if sdd < 10:
        sddStr = "  " + str(sdd)
    elif sdd < 100:
        sddStr = " " + str(sdd)
    else:
        sddStr = str(sdd)
    
    serialDataStr = cpuStr + memStr + sddStr + hddStr + cores + totalMemStr        #now we concenate all strings together by using "+" operand. By this, we´ll got one long string of data
    serialDataBytes = serialDataStr.encode("UTF-8")             #since we want to send string as series of BYTES, we wncode it to UTF-8 standart. This will put "b" before string, indicating that values are 1B each 

    print(serialDataBytes)                                      #here we print our serial string, used for debugging, can be commented out
    ser.write(serialDataBytes)                                  #send our long encoded string throught serial interface

ser.close()                                                     #this will never execute, because while loop will go forever. But i like to leave it here to prevent some bugs and bad stuff that could happen, also for you, if you want to include some way of getting out of the COM port
