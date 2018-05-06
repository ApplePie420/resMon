/*
*   resMon - PC monitoring HW/SW
*   using Arduino UNO, 128x64 monochromatic OLED display and custom Python script
*   Display your PC´s usage easily with these simple programs and very simple HW
*   ---WIRING---
*   Plug your OLED display into breadboard. Connect Vdd of OLED to +5V on Arduino, GND to GND of Arduino, SCL to A5 and SDA to A4
*   ---GETTING IT TO WORK---
*   Download U8Glib from https://github.com/olikraus/u8glib 
*   Upload *this* code to your Arduino board, DO NOT open serial monitor
*   Open and configure *resMon.py*, then execute it
*   You should have everything, enjoy :)
*   ---OPEN SOURCE LICENSE---
*                               MIT License
*              
*              Copyright (c) 2018 Radovan "N3ttX" Behýl
*              
*              Permission is hereby granted, free of charge, to any person obtaining a copy
*              of this software and associated documentation files (the "Software"), to deal
*              in the Software without restriction, including without limitation the rights
*              to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
*              copies of the Software, and to permit persons to whom the Software is
*              furnished to do so, subject to the following conditions:
*              
*              The above copyright notice and this permission notice shall be included in all
*              copies or substantial portions of the Software.
*              
*              THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
*              IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
*              FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
*              AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
*              LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
*              OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
*              SOFTWARE.
*/
#include "U8glib.h"                           //library for interfacing OLED

U8GLIB_SSD1306_128X64 OLED(U8G_I2C_OPT_NONE); //create instance of U8glib. For different OLED types/resolutions, check U8glib documentation. I used 128x64 monochromatic OLED display with I2C interface

long int rewrite = 0;                         //this will hold our last rewritten time from millis() function
const short firstRow = 12;                    //some constants that define where the rows will be
const short secondRow = 27;
const short thirdRow = 42;
const short fourthRow = 57;
const short width = 128;                      //also constant variable containing width of the screen, if you are using different display type you will have to tinker with those values

void setup(void) {
  Serial.begin(9600);                         //open serial interface with baud of 9600 (have to be the same as in python script)
}

String serialReceive;                         //some Strings, that will contain values got from Serial buffer. First one will contain the entire data string, others will contain only substrings that belongs to them
String CPUstat;
String RAMstat;
String HDDspace;
String SSDspace;
String CPUcores;
String RAMtotal;

void loop(void) {
  if(Serial.available() > 0) {                //if any data is available in serial buffer
    serialReceive = Serial.readString();      //read it as string and put into serialReceive variable
  }

  CPUstat = serialReceive.substring(0, 5);    //split the long ass received string to substrings. Values i used are those that i defined (5 characters/information) if not stated else
  RAMstat = serialReceive.substring(5, 10);
  HDDspace = serialReceive.substring(10, 15);
  SSDspace = serialReceive.substring(15, 20);
  CPUcores = serialReceive.substring(20, 24);
  RAMtotal = serialReceive.substring(24, 29);
    
  if (millis()-rewrite > 100) {               //OLED handler statement.. 
    OLED.firstPage();                         //go to the first page of OLED
    do {
      drawOLED();                             //our function that draws OLED display
    } while( OLED.nextPage() );
    rewrite = millis();                       //this piece of code can be found on different sites as recommended way to display stuff on OLED, if you are interested in how it works, just google it
  }
  
  delay(10);                                  //wait for 10ms, as OLED needs some time to get refreshed
}

void drawOLED(void) {
  OLED.setFont(u8g_font_unifontr);            //set font to monospace type (15x15 px). "r" on the end means REDUCED, this fontset uses only 1.1kb while full version (without "r") is some 5.5kb large... 
  OLED.setPrintPos(0, firstRow);              //set printing position to edge of screen, first row
  OLED.print("CPU:");                         //print legend text
  OLED.setPrintPos(35, firstRow);             //set printing position to a bit further
  OLED.print(CPUstat);                        //print the value received and split from the Serial
  OLED.setPrintPos(70, firstRow);             //set printing position to a bit further
  OLED.print(" %");                           //print percent sign
  OLED.setPrintPos(90, firstRow);             //set printing position to a bit further
  OLED.print(CPUcores);                       //print additional information

  OLED.drawLine(0, firstRow + 2, width, firstRow + 2);  //draw vertical line between each row, so it´s more clear to read

  OLED.setPrintPos(0, secondRow);             //and basically the same for everything repeats..
  OLED.print("RAM:");
  OLED.setPrintPos(35, secondRow);
  OLED.print(RAMstat);
  OLED.setPrintPos(70, secondRow);
  OLED.print(" %");
  OLED.setPrintPos(90, secondRow);
  OLED.print(RAMtotal);

  OLED.drawLine(0, secondRow + 2, width, secondRow + 2);

  OLED.setPrintPos(0, thirdRow);
  OLED.print("SSD:");
  OLED.setPrintPos(35, thirdRow);
  OLED.print(SSDspace);
  OLED.setPrintPos(70, thirdRow);
  OLED.print(" %");
  OLED.setPrintPos(90, thirdRow);
  OLED.print("(C:/)");

  OLED.drawLine(0, thirdRow + 2, width, thirdRow + 2);

  OLED.setPrintPos(0, fourthRow);
  OLED.print("HDD:");
  OLED.setPrintPos(35, fourthRow);
  OLED.print(HDDspace);
  OLED.setPrintPos(70, fourthRow);
  OLED.print(" %");
  OLED.setPrintPos(90, fourthRow);
  OLED.print("(D:/)");
}
