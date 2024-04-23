#include <SPI.h>
#include "LCD_Driver.h"
#include "GUI_Paint.h"
#include "image.h"

void setup()
{
  Config_Init();
  LCD_Init();
  LCD_Clear(WHITE);
  LCD_SetBacklight(1000);
  Paint_NewImage(LCD_WIDTH, LCD_HEIGHT, 0, WHITE);
  Paint_Clear(WHITE);
  Paint_SetRotate(180);

  Paint_DrawImage(gImage_40X40, 25, 32, 100, 62); 

  

}
void loop()
{
  
}



/*********************************************************************************************************
  END FILE
*********************************************************************************************************/
