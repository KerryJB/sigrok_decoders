/***************************************************
 DFPlayer - A Mini MP3 Player For Arduino
 <https://www.dfrobot.com/product-1121.html>

 ***************************************************
 This example shows the all the function of library for DFPlayer.

 Created 2016-12-07
 By [Angelo qiao](Angelo.qiao@dfrobot.com)

 GNU Lesser General Public License.
 See <http://www.gnu.org/licenses/> for details.
 All above must be included in any redistribution

 ### This version "tweaked" by Kerry Burton ###
 ****************************************************/

/***********Notice and Trouble shooting***************
 1.Connection and Diagram can be found here
<https://www.dfrobot.com/wiki/index.php/DFPlayer_Mini_SKU:DFR0299#Connection_Diagram>
 2.This code is tested on Arduino Uno, Leonardo, Mega boards.
 ****************************************************/

#include "Arduino.h"
#include "SoftwareSerial.h"
#include "DFRobotDFPlayerMini.h"

#define short_delay 0

SoftwareSerial mySoftwareSerial(D5, D6); // RX, TX
DFRobotDFPlayerMini myDFPlayer;
void printDetail(uint8_t type, int value);

void setup()
{
  static unsigned long starttime = millis();

  mySoftwareSerial.begin(9600);
  Serial.begin(115200);

  Serial.println();
  Serial.println(F("DFRobot DFPlayer Mini Demo"));
  Serial.println(F("Initializing DFPlayer ... (May take 3~5 seconds)"));

  while( !myDFPlayer.begin(mySoftwareSerial, false, false) ) {  // Use softwareSerial to communicate with mp3
    if( millis() - starttime > 4000 ) {
      Serial.println(F("Unable to begin:"));
      Serial.println(F("1.Please recheck the connection!"));
      Serial.println(F("2.Please insert the SD card!"));
      while(true);
    }
    delay( 10 );
  }
  Serial.println(F("DFPlayer Mini online."));

  myDFPlayer.setTimeOut(500); //Set serial communication timeout 500ms

  //----Set volume----
  myDFPlayer.volume(20);   //Set volume value (0~30).
  myDFPlayer.volumeUp();   //Volume Up
  myDFPlayer.volumeDown(); //Volume Down

  //----Set different EQ----
  myDFPlayer.EQ(DFPLAYER_EQ_NORMAL);
//  myDFPlayer.EQ(DFPLAYER_EQ_POP);
//  myDFPlayer.EQ(DFPLAYER_EQ_ROCK);
//  myDFPlayer.EQ(DFPLAYER_EQ_JAZZ);
//  myDFPlayer.EQ(DFPLAYER_EQ_CLASSIC);
//  myDFPlayer.EQ(DFPLAYER_EQ_BASS);

  //----Set device - we use SD as default----
//  myDFPlayer.outputDevice(DFPLAYER_DEVICE_U_DISK);  // 0
  myDFPlayer.outputDevice(DFPLAYER_DEVICE_SD);      // 1
//  myDFPlayer.outputDevice(DFPLAYER_DEVICE_AUX);     // 2
//  myDFPlayer.outputDevice(DFPLAYER_DEVICE_SLEEP);   // 3
//  myDFPlayer.outputDevice(DFPLAYER_DEVICE_FLASH);   // 4

  //----Mp3 control----
//  myDFPlayer.sleep();       //sleep
//  myDFPlayer.reset();       //Reset the module
//  myDFPlayer.enableDAC();   //Enable On-chip DAC
//  myDFPlayer.disableDAC();  //Disable On-chip DAC
  //myDFPlayer.outputSetting(true, 15); //output setting, enable the output and set the gain to 15

  //----Mp3 play----

  myDFPlayer.next();                  //Play next mp3
  delay(short_delay);
  myDFPlayer.previous();              //Play previous mp3
  delay(short_delay);
  myDFPlayer.play(1);                 //Play the first mp3
  delay(short_delay);
  myDFPlayer.loop(1);                 //Loop the first mp3
  delay(short_delay);
  myDFPlayer.pause();                 //pause the mp3
  delay(short_delay);
  myDFPlayer.start();                 //start the mp3 from the pause
  delay(short_delay);
  myDFPlayer.playFolder(15, 4);       //play specific mp3 in SD:/15/004.mp3; Folder Name(1~99); File Name(1~255)
  delay(short_delay);
  myDFPlayer.enableLoopAll();         //loop all mp3 files.
  delay(short_delay);
  myDFPlayer.disableLoopAll();        //stop loop all mp3 files.
  delay(short_delay);
  myDFPlayer.playMp3Folder(4);        //play specific mp3 in SD:/MP3/0004.mp3; File Name(0~65535)
  delay(short_delay);
  myDFPlayer.advertise(3);            //advertise specific mp3 in SD:/ADVERT/0003.mp3; File Name(0~65535)
  delay(short_delay);
  myDFPlayer.stopAdvertise();         //stop advertise
  delay(short_delay);
  myDFPlayer.playLargeFolder(2, 999); //play specific mp3 in SD:/02/004.mp3; Folder Name(1~10); File Name(1~1000)
  delay(short_delay);
  myDFPlayer.loopFolder(5);           //loop all mp3 files in folder SD:/05.
  delay(short_delay);
  myDFPlayer.randomAll();             //Random play all the mp3.
  delay(short_delay);
  myDFPlayer.enableLoop();            //enable loop.
  delay(short_delay);
  myDFPlayer.disableLoop();           //disable loop.
  delay(short_delay);
  //----Read information----
  Serial.print( F("State:              ") );
  Serial.println(myDFPlayer.readState());                  //read mp3 state
  delay(25);

  Serial.print( F("Volume:             ") );
  Serial.println(myDFPlayer.readVolume());                 //read current volume

  Serial.print( F("EQ Setting:         ") );
  Serial.println(myDFPlayer.readEQ());                     //read EQ setting

  Serial.print( F("File Count:         ") );
  Serial.println(myDFPlayer.readFileCounts());             //read all file counts in SD card

  Serial.print( F("Current File:       ") );
  Serial.println(myDFPlayer.readCurrentFileNumber());      //read current play file number

  Serial.print( F("Files in Folder 01: ") );
  Serial.println(myDFPlayer.readFileCountsInFolder(1));    //read file counts in folder SD:/01

  Serial.print( F("Files in Folder 02: ") );
  Serial.println(myDFPlayer.readFileCountsInFolder(2));    //read file counts in folder SD:/02

  Serial.print( F("Files in Folder 03: ") );
  Serial.println(myDFPlayer.readFileCountsInFolder(3));    //read file counts in folder SD:/03

  Serial.print( F("Files in Folder 04: ") );
  Serial.println(myDFPlayer.readFileCountsInFolder(4));    //read file counts in folder SD:/04

  myDFPlayer.play(1);  //Play the first mp3
  delay(200);
  Serial.print( F("Current File:       ") );
  Serial.println(myDFPlayer.readCurrentFileNumber());      //read current play file number
}

void loop()
{
  static unsigned long timer = millis();

  if (millis() - timer > 20000) {
    timer = millis();
    myDFPlayer.next();  //Play next mp3 every 20 seconds

    delay(short_delay);
    Serial.print( F("Current File:       ") );
    Serial.println(myDFPlayer.readCurrentFileNumber());    //read current play file number
  }

  if (myDFPlayer.available()) {
    printDetail(myDFPlayer.readType(), myDFPlayer.read()); //Print the detail message from DFPlayer to handle different errors and states.
  }
}

void printDetail(uint8_t type, int value){
  switch (type) {
    case TimeOut:
      Serial.println(F("Time Out!"));
      break;
    case WrongStack:
      Serial.println(F("Stack Wrong!"));
      break;
    case DFPlayerCardInserted:
      Serial.println(F("Card Inserted!"));
      break;
    case DFPlayerCardRemoved:
      Serial.println(F("Card Removed!"));
      break;
    case DFPlayerCardOnline:
      Serial.println(F("Card Online!"));
      break;
    case DFPlayerUSBInserted:
      Serial.println(F("USB Inserted!"));
      break;
    case DFPlayerUSBRemoved:
      Serial.println(F("USB Removed!"));
      break;
    case DFPlayerPlayFinished:
      Serial.print(F("Number:"));
      Serial.print(value);
      Serial.println(F(" Play Finished!"));
      break;
    case DFPlayerError:
      Serial.print(F("DFPlayerError:"));
      switch (value) {
        case Busy:
          Serial.println(F("Card not found"));
          break;
        case Sleeping:
          Serial.println(F("Sleeping"));
          break;
        case SerialWrongStack:
          Serial.println(F("Get Wrong Stack"));
          break;
        case CheckSumNotMatch:
          Serial.println(F("Check Sum Not Match"));
          break;
        case FileIndexOut:
          Serial.println(F("File Index Out of Bound"));
          break;
        case FileMismatch:
          Serial.println(F("Cannot Find File"));
          break;
        case Advertise:
          Serial.println(F("In Advertise"));
          break;
        default:
          break;
      }
      break;
    default:
      break;
  }

}