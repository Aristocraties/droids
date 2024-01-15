#Notes regarding Florence

#Connecting the waveshare 1.28 round LCD to the Arduino nanos by SPI:


The DEV_Config.h file defines the pinout.  The default, which I'm not using, is commented out in that file and my pinout is defined.  Feel free to use either or your own. 

Starts on Line 47
/**
 * GPIO config
**/
//#define DEV_CS_PIN  10
//#define DEV_DC_PIN  7
//#define DEV_RST_PIN 8
//#define DEV_BL_PIN  9
#define DEV_CS_PIN  9
#define DEV_DC_PIN  8
#define DEV_RST_PIN 7
#define DEV_BL_PIN  6


#Custom painting functions
I added the wipe and unwipe functions to the GUI_Paint.cpp file and then made sure the signatures of the new functions were also added to GUI_Paint.h.  Both functions were written by AI.  I had to go back and forth with it a bit explaining what worked and what didn't work until it got to a place I was reasonably happy.  I never defined the LCD driver type to it.  It would have done better if I had.  This was deliberately quick and dirty.  I just copied in at one point the contents of the GUI_Paint.cpp so it could see the methods available to it. 