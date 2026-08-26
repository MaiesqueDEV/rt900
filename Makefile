# Target name
TARGET = firmware

# Toolchain definitions
CC = arm-none-eabi-gcc
AS = arm-none-eabi-gcc
LD = arm-none-eabi-gcc
OBJCOPY = arm-none-eabi-objcopy
SIZE = arm-none-eabi-size

# Build directory
BUILD_DIR = build

# C flags
CFLAGS = -Os -Wall -mcpu=cortex-m1 -fno-builtin -fshort-enums -fno-delete-null-pointer-checks -std=c11 -MMD -MP -flto
CFLAGS += -DUSE_FULL_ASSERT=1
CFLAGS += -DUSE_STDPERIPH_DRIVER
CFLAGS += -Wno-unused-variable
CFLAGS += -Wno-maybe-uninitialized
CFLAGS += -Wno-format
CFLAGS += -Wno-switch
CFLAGS += -Wno-attributes
CFLAGS += -Wno-pointer-sign
CFLAGS += -Wno-unused-but-set-variable
CFLAGS += -D__nop=__NOP

# Assembler flags
ASFLAGS = -mcpu=cortex-m1 -x assembler-with-cpp

# Linker flags
LDFLAGS = -mcpu=cortex-m1 -nostartfiles -Wl,-T,firmware.ld -flto
LDFLAGS += -Wl,-Map=$(BUILD_DIR)/$(TARGET).map,--cref
LDFLAGS += -specs=nano.specs -specs=nosys.specs

# Include directories
INCLUDES = \
    -IApp \
    -IBSP \
    -ICommon \
    -ICore \
    -ICPS \
    -IDriver \
    -IGui \
    -IInterface \
    -ILibraries \
    -ILibraries/CMSIS/Include \
    -ILibraries/StdPeriph_Driver/inc \
    -IVoice \
    -I.

# Source files
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
    BSP/Board.c \
    BSP/BoardFun.c \
    BSP/bt32f0x_it.c \
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
    Common/BitMap.c \
    Common/Delay.c \
    Common/Globe.c \
    Common/assert_failed_stub.c \
    Core/Functions.c \
    Core/Radio.c \
    Core/RadioTask.c \
    CPS/ProgromFlash.c \
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

S_SOURCES = \
    Libraries/CMSIS/Device/startup_bt32f0x.s

C_OBJS = $(patsubst %.c, $(BUILD_DIR)/%.o, $(C_SOURCES))
S_OBJS = $(patsubst %.s, $(BUILD_DIR)/%.o, $(S_SOURCES))
OBJS = $(C_OBJS) $(S_OBJS)

DEPS = $(OBJS:.o=.d)

all: $(BUILD_DIR)/$(TARGET).bin $(BUILD_DIR)/$(TARGET).hex

$(BUILD_DIR)/%.o: %.c
	@mkdir -p $(dir $@)
	$(CC) $(CFLAGS) $(INCLUDES) -c $< -o $@

$(BUILD_DIR)/%.o: %.s
	@mkdir -p $(dir $@)
	$(CC) $(ASFLAGS) $(INCLUDES) -c $< -o $@

$(BUILD_DIR)/$(TARGET).elf: $(OBJS) firmware.ld
	$(LD) $(LDFLAGS) $(OBJS) -o $@ $(LIBS)
	$(SIZE) $@

$(BUILD_DIR)/$(TARGET).bin: $(BUILD_DIR)/$(TARGET).elf
	$(OBJCOPY) -O binary $< $@

$(BUILD_DIR)/$(TARGET).hex: $(BUILD_DIR)/$(TARGET).elf
	$(OBJCOPY) -O ihex $< $@

clean:
	rm -rf $(BUILD_DIR)

.PHONY: all clean
