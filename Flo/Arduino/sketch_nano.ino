// Include necessary libraries
#include <SPI.h>
#include "LCD_Driver.h"
#include "GUI_Paint.h"
#include "image.h"

// Define colors in RGB565 format
UWORD BACKGROUND_COLOR = ((0xff >> 3) << 11) | ((0xea >> 2) << 5) | (0x03 >> 3);
UWORD SLEEP_COLOR = ((0x7F >> 3) << 11) | ((0x8F >> 2) << 5) | (0x07 >> 3);
UWORD CURRENT_COLOR; // Variable to hold the current color based on the state of the device

// Define the center and radius for the eyes
UWORD centerX = LCD_WIDTH / 2;
UWORD centerY = LCD_HEIGHT / 3;
UWORD centerY2 = (LCD_HEIGHT / 3) * 2;
UWORD radius = min(centerX, centerY);

void setup()
{
  // Initialize the LCD and set the backlight
  Config_Init();
  LCD_Init();
  LCD_SetBacklight(1000);

  // Set the current color to the "awake" background color
  CURRENT_COLOR = BACKGROUND_COLOR;

  // Wake up the device
  wake();

  // Comms with Raspberry PI
  // Start serial communication at 9600 bps:
  Serial.begin(57600);
}
void loop()
{
  // Check if there's any data available on the serial port
  if (Serial.available() > 0) {
      String data = Serial.readStringUntil('\n');

      // Perform actions based on the received data
      if (data == "blink") {
        blink();
      }

      if (data == "sleep") {
        sleep();
      }

      if (data == "wake") {
        wake();
      }
  }
}

// Function to make the device blink
void blink()
{
  Paint_WipeScreen(BLACK);
  delay(500);
  Paint_UnwipeScreen(CURRENT_COLOR, centerX, centerY, centerY2);
}

// Function to make the device sleep (dimmed eyes)
void sleep()
{
  CURRENT_COLOR = SLEEP_COLOR;
  Paint_NewImage(LCD_WIDTH, LCD_HEIGHT, 0, CURRENT_COLOR);
  Paint_Clear(CURRENT_COLOR);
  Paint_DrawCircle(centerX,centerY, 20, BLACK ,DOT_PIXEL_2X2,DRAW_FILL_FULL);
  Paint_DrawCircle(centerX,centerY2, 20, BLACK ,DOT_PIXEL_2X2,DRAW_FILL_FULL);
}

// Function to make the device wake (bright eyes)
void wake()
{
  CURRENT_COLOR = BACKGROUND_COLOR;
  Paint_NewImage(LCD_WIDTH, LCD_HEIGHT, 0, CURRENT_COLOR);
  Paint_Clear(CURRENT_COLOR);
  Paint_DrawCircle(centerX,centerY, 20, BLACK ,DOT_PIXEL_2X2,DRAW_FILL_FULL);
  Paint_DrawCircle(centerX,centerY2, 20, BLACK ,DOT_PIXEL_2X2,DRAW_FILL_FULL);
}



/*********************************************************************************************************
  END FILE
*********************************************************************************************************/
