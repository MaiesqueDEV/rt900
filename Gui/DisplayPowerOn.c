#include "includes.h"

void UI_DisplayPowerOn(void)
{
    // Limpa a tela com fundo preto (0x0000)
    LCD_ClearArea(0, 0, LCD_WIDTH, LCD_HEIGHT, COLOR_BACKGROUND);
    LcdBackLightSwitch(LED_ON);

    // Exibe "MAIESQUE" em destaque grande (Amarelo 0xFFE0 em fundo Preto)
    LCD_DisplayText(48, 35, (uint08_t *)"MAIESQUE", FONTSIZE_16x16, 0xFFE0, COLOR_BACKGROUND, 0);

    // Exibe "BINTOLK RT900" (Ciano)
    LCD_DisplayText(40, 65, (uint08_t *)"BINTOLK RT900", FONTSIZE_6x12, 0x07FF, COLOR_BACKGROUND, 0);

    // Exibe "CUSTOM FIRMWARE" (Verde)
    LCD_DisplayText(34, 85, (uint08_t *)"CUSTOM FIRMWARE", FONTSIZE_6x12, 0x07E0, COLOR_BACKGROUND, 0);

    // Mantém a mensagem de abertura na tela por 1.5 segundos ao ligar
    DelayMs(1500);
}
