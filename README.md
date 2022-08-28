# resMon
## What is it?
resMon is relativly simple project with Arduino and OLED screen with small custom python code, that displays you PC usage (CPU, RAM and up to 2 harddrives´s free space). This is how it looks:

![resMonIMAGE](OLED2.png)
## Installation
### Requirements
- Arduino of your choice
- 128x64 I2C OLED display 
- bunch of wires for OLED
- Arduino IDE
- Python 3.x
### How to
It is quite a simple process. First, you'll need to [connect an OLED display to Arduino of your choice](https://i0.wp.com/randomnerdtutorials.com/wp-content/uploads/2019/05/oled-display-arduino.png?resize=828%2C605&quality=100&strip=all&ssl=1). Then, download this repo as zip, or clone it. Open the `.ino` file in Arduino IDE, select your board and COM port and upload the sketch. Take a note of your COM port, you will need to set it later in the Python script. If you want to verify that the sketch is working, open the serial monitor and on 9600 baud, there should be a long string of data sent roughly every second. 
If that is working, you can now close Arduino IDE and open resMon.py in your favourite text editor. Scroll down to (line 50)[https://github.com/ApplePie420/resMon/blob/master/resMon.py#L50) and set the variable to whatever COM port number you've set in Arduino IDE. 
That should be everything, all pythons' libraries come preinstalled, so you can run the script:
`python3 resMon.py`
## Arduino 
I chose Arduino over countless other platforms because almost everyone own one, and if not, it can be bought for really cheap. Its programming language may not be the fastest and most reliable, but its really simple to use and understand and it have **giant** community and library support. I used default *wire.h* library with [**u8glib**](https://github.com/olikraus/u8glib). I paired it with chinese 128x64 OLED display interfacing throught I2C bus, to keep simplicity. Thus you can utilize Arduino Pro Micro, an OLED display, 4 wires and custom [**3D printed case**](https://www.tinkercad.com/things/kKZvLYCUVjT) to create really tiny and cute USB powered PC usage monitor!
## Python
I created very simple python code using [**pySerial**](https://pypi.org/project/pyserial/) and [**psutil**](https://pypi.org/project/psutil/) libraries to create simple, not demanding software that gathers CPU and RAM usage alongside with free HDD/SSD space counter and send it to Arduino via *serial interface*. 
## Help me
Feel free to fork it, tweak it, fix it, do stuff. If you find a **bug** or possibility to improve, leave an *Issue* or comment and I´ll take a look at it :)  Almost every line is commented, so there is very close to no way you won´t understand, what is going on. Just take a look...
## To-do list
- [x] 3D Case design [**LINK**](https://www.tinkercad.com/things/kKZvLYCUVjT)
- [x] Optimize (and proferably clean) the code (actually it was pretty well written from beggining.. open to any suggestions tho)
- [ ] HDDmon  
- [ ] Add second screen with temperature readings  
- [ ] Plot graphs  
- [x] Make an YouTube video [**LINK**](https://www.youtube.com/watch?v=c-p6RKaEpBU)  
## Libraries, links
[**u8glib**](https://github.com/olikraus/u8glib)  
[**pySerial**](https://pypi.org/project/pyserial/)  
[**psutil**](https://pypi.org/project/psutil/)  
[**YouTube Video**](https://www.youtube.com/watch?v=c-p6RKaEpBU)  
