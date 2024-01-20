> :warning: **This project is still under testing**: The installation instructions are yet to be verified on a fresh install. Please proceed with caution.

# Arduino Nano & Waveshare LCD Project

This project involves connecting a Waveshare 1.28 round LCD to Arduino Nanos via SPI.

## Hardware Requirements

- Arduino Nanos: These are available from a variety of sources, including Amazon. It's recommended to use name brand real ones to avoid programming issues often associated with knock-offs.
- Waveshare 1.28 round LCDs: These can be found and purchased on [Waveshare's website](https://www.waveshare.com/1.28inch-lcd-module.htm) or on Amazon.  Waveshare's documentation [wiki] (https://www.waveshare.com/wiki/1.28inch_LCD_Module#Documents).

## Connection Guide

The DEV_Config.h file defines the pinout.  The default, which I'm not using, is commented out in that file and my pinout is defined.  Feel free to use either or your own. This was my first time using SPI, so the final pinout is simply a reflection of the final thing I found that made it all click in my head.


Starts on Line 47
```
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
```

Once the LCD is wired to the nano, you can use the USB cable to connect to your computer.  

> :warning: You'll ultimately use the USB cables for connecting to the Raspberry PI too (permanently), so make sure you have two if using for two eyes. 

## Software Guide

This installs normally through the Arduino IDE.  Just open all the code files and compile to make sure it builds, then upload.  There are plenty of tutorials on this area.  We can evaluate if more instruction here is needed moving forward.

To add new painting functions for the LCDs, you need to add them to GUI_Paint.cpp.  You'll also need to define the method signature in the GUI_Paint.h file.  If you're using AI to write it, just provide it the contents of the GUI_Paint.cpp file.  I also found it helpful to let the AI know that these use the GC9A01A library driver. 