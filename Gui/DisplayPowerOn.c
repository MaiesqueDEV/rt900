#include "includes.h"

extern void UI_DisplayPowerOn(void)
{
    // Limpa a tela com fundo preto (0x0000)
    LCD_ClearArea(0, 0, 160, 128, 0x0000);
    LcdBackLightSwitch(LED_ON);

    // Exibe "MAIESQUE" em destaque grande (Amarelo 0xFFE0 em fundo Preto 0x0000)
    LCD_DisplayText(48, 35, (U8 *)"MAIESQUE", FONTSIZE_16x16, 0xFFE0, 0x0000, 0);

    // Exibe "BINTOLK RT900" (Ciano 0x07FF)
    LCD_DisplayText(40, 65, (U8 *)"BINTOLK RT900", FONTSIZE_6x12, 0x07FF, 0x0000, 0);

    // Exibe "CUSTOM FIRMWARE" (Verde 0x07E0)
    LCD_DisplayText(34, 85, (U8 *)"CUSTOM FIRMWARE", FONTSIZE_6x12, 0x07E0, 0x0000, 0);

    // Mantém a mensagem de abertura na tela por 1.5 segundos ao ligar
    DelayMs(1500);
}
