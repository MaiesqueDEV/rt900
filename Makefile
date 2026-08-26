TARGET = firmware
CC      = arm-none-eabi-gcc
OBJCOPY = arm-none-eabi-objcopy
SIZE    = arm-none-eabi-size
BUILD_DIR = build

CFLAGS  = -Os -Wall -mcpu=cortex-m0 -mthumb -fno-builtin -fshort-enums
CFLAGS += -fno-delete-null-pointer-checks -std=c11 -MMD -MP
CFLAGS += -DUSE_FULL_ASSERT=1 -DUSE_STDPERIPH_DRIVER
CFLAGS += -Wno-unused-variable -Wno-maybe-uninitialized -Wno-format
CFLAGS += -Wno-switch -Wno-attributes -Wno-pointer-sign
CFLAGS += -Wno-unused-but-set-variable -Wno-implicit-function-declaration
CFLAGS += -D__nop=__NOP

LDFLAGS  = -mcpu=cortex-m0 -mthumb -nostartfiles
LDFLAGS += -Wl,-T,firmware.ld -Wl,-Map=$(BUILD_DIR)/$(TARGET).map
LDFLAGS += -specs=nano.specs -specs=nosys.specs

INCLUDES  = -IApp -IBSP -ICommon -ICore -ICPS -IDriver
INCLUDES += -IGui -IInterface -ILibraries -IVoice -I.
INCLUDES += -ILibraries/CMSIS/Include
INCLUDES += -ILibraries/StdPeriph_Driver/inc

C_SOURCES = \
    Libraries/StdPeriph_Driver/src/bt32f0x_adc.c \
    Libraries/StdPeriph_Driver/src/bt32f0x_comp.c \
    Libraries/StdPeriph_Driver/src/bt32f0x_crc.c \
    Libraries/StdPeriph_Driver/src/bt32f0x_dbgmcu.c \
    Libraries/StdPeriph_Driver/src/bt32f0x_divqsrt.c \
    Libraries/StdPeriph_Driver/src/bt32f0x_dma.c \
    Libraries/StdPeriph_Driver/src/bt32f0x_exti.c \
    Libraries/StdPeriph_Driver/src/bt32f0x_flash.c \
    Libraries/StdPeriph_Driver/src/bt32f0x_gpio.c \
    Libraries/StdPeriph_Driver/src/bt32f0x_i2c.c \
    Libraries/StdPeriph_Driver/src/bt32f0x_iwdg.c \
    Libraries/StdPeriph_Driver/src/bt32f0x_misc.c \
    Libraries/StdPeriph_Driver/src/bt32f0x_opa.c \
    Libraries/StdPeriph_Driver/src/bt32f0x_pwr.c \
    Libraries/StdPeriph_Driver/src/bt32f0x_rcc.c \
    Libraries/StdPeriph_Driver/src/bt32f0x_rtc.c \
    Libraries/StdPeriph_Driver/src/bt32f0x_spi.c \
    Libraries/StdPeriph_Driver/src/bt32f0x_syscfg.c \
    Libraries/StdPeriph_Driver/src/bt32f0x_tim.c \
    Libraries/StdPeriph_Driver/src/bt32f0x_usart.c \
    Libraries/StdPeriph_Driver/src/bt32f0x_wwdg.c \
    Libraries/StdPeriph_Driver/src/system_bt32f0x.c \
    App/main.c \
    App/AppAlarm.c \
    App/AppDtmf.c \
    App/AppFm.c \
    App/AppMain.c \
    App/AppMenu.c \
    App/AppMoni.c \
    App/AppScan.c \
    App/AppScanQT.c \
    App/AppSearch.c \
    App/AppTask.c \
    App/AppWeather.c \
    App/Battery.c \
    App/DualStandby.c \
    BSP/Board.c \
    BSP/BoardFun.c \
    BSP/bt32f0x_it.c \
    Common/BitMap.c \
    Common/Delay.c \
    Common/Globe.c \
    Core/Functions.c \
    Core/Radio.c \
    Core/RadioTask.c \
    CPS/ProgromFlash.c \
    Driver/crc.c \
    Driver/DevBK4819.c \
    Driver/DevBK4819Data.c \
    Driver/FlashFont.c \
    Driver/key_ptt.c \
    Driver/keyboard.c \
    Driver/NorFlash.c \
    Driver/RadioDataReset.c \
    Driver/RadioDataStorage.c \
    Driver/Rda5807.c \
    Driver/st7735s.c \
    Driver/Systick.c \
    Gui/DisplayBattery.c \
    Gui/DisplayDtmf.c \
    Gui/DisplayFm.c \
    Gui/DisplayInputbox.c \
    Gui/DisplayMain.c \
    Gui/DisplayMenu.c \
    Gui/DisplayPowerOn.c \
    Gui/DisplayScanQT.c \
    Gui/DisplaySearch.c \
    Gui/DisplayWeather.c \
    Gui/LcdFillDot.c \
    Interface/i2c.c \
    Voice/Beep.c \
    Voice/VoiceBroadcast.c

S_SOURCES = Libraries/CMSIS/Device/startup_bt32f0x.s

C_OBJS = $(patsubst %.c,$(BUILD_DIR)/%.o,$(C_SOURCES))
S_OBJS = $(patsubst %.s,$(BUILD_DIR)/%.o,$(S_SOURCES))
OBJS   = $(C_OBJS) $(S_OBJS)
DEPS   = $(OBJS:.o=.d)

all: $(BUILD_DIR)/$(TARGET).bin $(BUILD_DIR)/$(TARGET).hex

$(BUILD_DIR)/%.o: %.c
	@mkdir -p $(dir $@)
	$(CC) $(CFLAGS) $(INCLUDES) -c $< -o $@

$(BUILD_DIR)/%.o: %.s
	@mkdir -p $(dir $@)
	$(CC) -mcpu=cortex-m0 -mthumb -x assembler-with-cpp $(INCLUDES) -c $< -o $@

$(BUILD_DIR)/$(TARGET).elf: $(OBJS) firmware.ld
	$(CC) $(LDFLAGS) $(OBJS) -o $@
	$(SIZE) $@

$(BUILD_DIR)/$(TARGET).bin: $(BUILD_DIR)/$(TARGET).elf
	$(OBJCOPY) -O binary $< $@

$(BUILD_DIR)/$(TARGET).hex: $(BUILD_DIR)/$(TARGET).elf
	$(OBJCOPY) -O ihex $< $@

clean:
	rm -rf $(BUILD_DIR)

.PHONY: all clean

-include $(DEPS)
