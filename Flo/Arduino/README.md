> :warning: **This project is still under testing**: The installation instructions are yet to be verified on a fresh install. Please proceed with caution.

# Arduino Nano & Waveshare LCD Project

This project involves connecting a Waveshare 1.28 round LCD to Arduino Nanos via SPI.

## Hardware Requirements

- Arduino Nanos: These are available from a variety of sources, including Amazon. It's recommended to use name brand real ones to avoid programming issues often associated with knock-offs.
- Waveshare 1.28 round LCDs: These can be found and purchased on [Waveshare's website](https://www.waveshare.com/1.28inch-lcd-module.htm) or on Amazon.

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