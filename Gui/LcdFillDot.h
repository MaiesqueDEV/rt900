#ifndef __LCD_FILL_DOT_H
#define __LCD_FILL_DOT_H

#include "PublType.h"

/* Cores de tema global da interface */
#define COLOR_FOREGROUND    0xFFFF   /* Branco - cor do texto/icone */
#define COLOR_BACKGROUND    0x0000   /* Preto - fundo da tela */
#define COLOR_WORK_AREA     0x0000   /* Preto - area de trabalho */

/* Tamanhos de fonte */
#define FONTSIZE_6x12       12
#define FONTSIZE_8x16       16
#define FONTSIZE_16x16      16

void LCD_ClearArea(uint16_t posX, uint16_t posY, uint16_t width, uint16_t height, uint16_t backColor);
void LCD_DisplayText(uint16_t posX, uint16_t posY, uint08_t *pString, uint08_t fontSize, uint16_t brushColor, uint16_t backColor, uint08_t divDot);
void LCD_DisplayText5X7(uint16_t posX, uint16_t posY, uint08_t *pString, uint16_t len, uint16_t brushColor, uint16_t backColor);
void LCD_DrawRectangle(uint16_t posX, uint16_t posY, uint16_t width, uint16_t height, uint16_t color);
void LCD_DisplayIcon(uint16_t posX, uint16_t posY, uint16_t width, uint16_t height, const uint08_t *pdat, uint16_t brushColor, uint16_t backColor);
void LCD_DisplayNum6X9(uint16_t posX, uint16_t posY, uint08_t *pString, uint16_t backColor);
void LCD_DisplayNum12x17(uint16_t posX, uint16_t posY, uint08_t *pString, uint16_t backColor);

#endif
