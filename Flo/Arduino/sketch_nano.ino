#include <SPI.h>
#include "LCD_Driver.h"
#include "GUI_Paint.h"
#include "image.h"

UWORD BACKGROUND_COLOR = ((0xff >> 3) << 11) | ((0xea >> 2) << 5) | (0x03 >> 3);

UWORD centerX = LCD_WIDTH / 2;
UWORD centerY = LCD_HEIGHT / 3;
UWORD centerY2 = (LCD_HEIGHT / 3) * 2;
UWORD radius = min(centerX, centerY);
unsigned long previousMillis = 0;  // will store the last time the blink function was updated
unsigned long sleepTimerMillis = 0;

void setup()
{
  
  
  Config_Init();
  LCD_Init();
  LCD_SetBacklight(1000);
  Paint_NewImage(LCD_WIDTH, LCD_HEIGHT, 0, BACKGROUND_COLOR);
  Paint_Clear(BACKGROUND_COLOR);
  Paint_DrawCircle(centerX,centerY, 20, BLACK ,DOT_PIXEL_2X2,DRAW_FILL_FULL);
  Paint_DrawCircle(centerX,centerY2, 20, BLACK ,DOT_PIXEL_2X2,DRAW_FILL_FULL);

  // Comms with Raspberry PI
  // Start serial communication at 9600 bps:
  Serial.begin(57600);
}
void loop()
{
  
  if (Serial.available() > 0) {
      String data = Serial.readStringUntil('\n');

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

void blink()
{
  Paint_WipeScreen(BLACK);
  delay(500);
  Paint_UnwipeScreen(BACKGROUND_COLOR, centerX, centerY, centerY2);
}

void sleep()
{
  LCD_SetBacklight(50);
}

void wake()
{
  LCD_SetBacklight(1000);
}



/*********************************************************************************************************
  END FILE
*********************************************************************************************************/
