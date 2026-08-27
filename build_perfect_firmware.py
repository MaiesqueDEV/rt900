import os
import subprocess
import sys
import glob

TOOLCHAIN_BIN = r"D:\radio px\toolchain\xpack-arm-none-eabi-gcc-13.2.1-1.1\bin"
CC = os.path.join(TOOLCHAIN_BIN, "arm-none-eabi-gcc.exe")
OBJCOPY = os.path.join(TOOLCHAIN_BIN, "arm-none-eabi-objcopy.exe")
SIZE = os.path.join(TOOLCHAIN_BIN, "arm-none-eabi-size.exe")

SRC_ROOT = r"D:\radio px\keil_project\Radtel_RT900 20250305\work\source"
BUILD_DIR = r"D:\radio px\keil_project\build_perfect"
TARGET = "firmware"
ENCRYPT_TOOL = r"D:\radio px\rt900\Tools\ARCEncryptTools.exe"
ENCRYPT_KEY = "QzBtDzKjYxGsWalkieTalkieBt8000OpenDate20241202"

INCLUDES = [
    f"-I{SRC_ROOT}/App",
    f"-I{SRC_ROOT}/BSP",
    f"-I{SRC_ROOT}/Common",
    f"-I{SRC_ROOT}/Core",
    f"-I{SRC_ROOT}/CPS",
    f"-I{SRC_ROOT}/Driver",
    f"-I{SRC_ROOT}/Gui",
    f"-I{SRC_ROOT}/Interface",
    f"-I{SRC_ROOT}/Libraries",
    f"-I{SRC_ROOT}/Voice",
    f"-I{SRC_ROOT}",
    f"-I{SRC_ROOT}/Libraries/CMSIS/Include",
    f"-I{SRC_ROOT}/Libraries/StdPeriph_Driver/inc"
]

CFLAGS = [
    "-Os", "-Wall", "-mcpu=cortex-m0", "-mthumb",
    "-ffunction-sections", "-fdata-sections",
    "-fno-builtin", "-fshort-enums", "-fno-delete-null-pointer-checks",
    "-std=c11", "-DUSE_FULL_ASSERT=1", "-DUSE_STDPERIPH_DRIVER",
    "-Wno-unused-variable", "-Wno-maybe-uninitialized", "-Wno-format",
    "-Wno-switch", "-Wno-attributes", "-Wno-pointer-sign",
    "-Wno-unused-but-set-variable", "-Wno-implicit-function-declaration",
    "-D__nop=__NOP"
]

LDFLAGS = [
    "-mcpu=cortex-m0", "-mthumb", "-nostartfiles",
    r"-Wl,-T,D:\radio px\rt900\firmware.ld",
    "-Wl,--gc-sections",
    f"-Wl,-Map={BUILD_DIR}/{TARGET}.map",
    "-specs=nano.specs", "-specs=nosys.specs"
]

C_SOURCES = [
    f"{SRC_ROOT}/Libraries/StdPeriph_Driver/src/bt32f0x_adc.c",
    f"{SRC_ROOT}/Libraries/StdPeriph_Driver/src/bt32f0x_comp.c",
    f"{SRC_ROOT}/Libraries/StdPeriph_Driver/src/bt32f0x_crc.c",
    f"{SRC_ROOT}/Libraries/StdPeriph_Driver/src/bt32f0x_dbgmcu.c",
    f"{SRC_ROOT}/Libraries/StdPeriph_Driver/src/bt32f0x_divqsrt.c",
    f"{SRC_ROOT}/Libraries/StdPeriph_Driver/src/bt32f0x_dma.c",
    f"{SRC_ROOT}/Libraries/StdPeriph_Driver/src/bt32f0x_exti.c",
    f"{SRC_ROOT}/Libraries/StdPeriph_Driver/src/bt32f0x_flash.c",
    f"{SRC_ROOT}/Libraries/StdPeriph_Driver/src/bt32f0x_gpio.c",
    f"{SRC_ROOT}/Libraries/StdPeriph_Driver/src/bt32f0x_i2c.c",
    f"{SRC_ROOT}/Libraries/StdPeriph_Driver/src/bt32f0x_iwdg.c",
    f"{SRC_ROOT}/Libraries/StdPeriph_Driver/src/bt32f0x_misc.c",
    f"{SRC_ROOT}/Libraries/StdPeriph_Driver/src/bt32f0x_opa.c",
    f"{SRC_ROOT}/Libraries/StdPeriph_Driver/src/bt32f0x_pwr.c",
    f"{SRC_ROOT}/Libraries/StdPeriph_Driver/src/bt32f0x_rcc.c",
    f"{SRC_ROOT}/Libraries/StdPeriph_Driver/src/bt32f0x_rtc.c",
    f"{SRC_ROOT}/Libraries/StdPeriph_Driver/src/bt32f0x_spi.c",
    f"{SRC_ROOT}/Libraries/StdPeriph_Driver/src/bt32f0x_syscfg.c",
    f"{SRC_ROOT}/Libraries/StdPeriph_Driver/src/bt32f0x_tim.c",
    f"{SRC_ROOT}/Libraries/StdPeriph_Driver/src/bt32f0x_usart.c",
    f"{SRC_ROOT}/Libraries/StdPeriph_Driver/src/bt32f0x_wwdg.c",
    f"{SRC_ROOT}/Libraries/StdPeriph_Driver/src/system_bt32f0x.c",
    f"{SRC_ROOT}/App/main.c",
    f"{SRC_ROOT}/App/AppAlarm.c",
    f"{SRC_ROOT}/App/AppDtmf.c",
    f"{SRC_ROOT}/App/AppFm.c",
    f"{SRC_ROOT}/App/AppMain.c",
    f"{SRC_ROOT}/App/AppMenu.c",
    f"{SRC_ROOT}/App/AppMoni.c",
    f"{SRC_ROOT}/App/AppScan.c",
    f"{SRC_ROOT}/App/AppScanQT.c",
    f"{SRC_ROOT}/App/AppSearch.c",
    f"{SRC_ROOT}/App/AppTask.c",
    f"{SRC_ROOT}/App/AppWeather.c",
    f"{SRC_ROOT}/App/Battery.c",
    f"{SRC_ROOT}/App/DualStandby.c",
    f"{SRC_ROOT}/BSP/Board.c",
    f"{SRC_ROOT}/BSP/BoardFun.c",
    f"{SRC_ROOT}/BSP/bt32f0x_it.c",
    f"{SRC_ROOT}/Common/BitMap.c",
    f"{SRC_ROOT}/Common/Delay.c",
    f"{SRC_ROOT}/Common/Globe.c",
    r"D:\radio px\rt900\Common\assert_failed_stub.c",
    f"{SRC_ROOT}/Core/Functions.c",
    f"{SRC_ROOT}/Core/Radio.c",
    f"{SRC_ROOT}/Core/RadioTask.c",
    f"{SRC_ROOT}/CPS/ProgromFlash.c",
    f"{SRC_ROOT}/Driver/crc.c",
    f"{SRC_ROOT}/Driver/DevBK4819.c",
    f"{SRC_ROOT}/Driver/DevBK4819Data.c",
    f"{SRC_ROOT}/Driver/FlashFont.c",
    f"{SRC_ROOT}/Driver/key_ptt.c",
    f"{SRC_ROOT}/Driver/keyboard.c",
    f"{SRC_ROOT}/Driver/NorFlash.c",
    f"{SRC_ROOT}/Driver/RadioDataReset.c",
    f"{SRC_ROOT}/Driver/RadioDataStorage.c",
    f"{SRC_ROOT}/Driver/Rda5807.c",
    f"{SRC_ROOT}/Driver/st7735s.c",
    f"{SRC_ROOT}/Driver/Systick.c",
    f"{SRC_ROOT}/Gui/DisplayBattery.c",
    f"{SRC_ROOT}/Gui/DisplayDtmf.c",
    f"{SRC_ROOT}/Gui/DisplayFm.c",
    f"{SRC_ROOT}/Gui/DisplayInputbox.c",
    f"{SRC_ROOT}/Gui/DisplayMain.c",
    f"{SRC_ROOT}/Gui/DisplayMenu.c",
    f"{SRC_ROOT}/Gui/DisplayPowerOn.c",
    f"{SRC_ROOT}/Gui/DisplayScanQT.c",
    f"{SRC_ROOT}/Gui/DisplaySearch.c",
    f"{SRC_ROOT}/Gui/DisplayWeather.c",
    f"{SRC_ROOT}/Gui/LcdFillDot.c",
    f"{SRC_ROOT}/Interface/i2c.c",
    f"{SRC_ROOT}/Voice/Beep.c",
    f"{SRC_ROOT}/Voice/VoiceBroadcast.c"
]

S_SOURCES = [
    r"D:\radio px\rt900\Libraries\CMSIS\Device\startup_bt32f0x.s"
]

def main():
    os.makedirs(BUILD_DIR, exist_ok=True)
    objs = []

    print("[1/5] Compilando arquivos C otimizados...")
    for src in C_SOURCES:
        if not os.path.exists(src):
            print(f"ERRO: Arquivo nao encontrado: {src}")
            return 1
        rel_obj = os.path.join(BUILD_DIR, os.path.splitext(os.path.basename(src))[0] + ".o")
        cmd = [CC] + CFLAGS + INCLUDES + ["-c", src, "-o", rel_obj]
        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode != 0:
            print(f"\nERRO ao compilar {src}:")
            print(res.stderr)
            print(res.stdout)
            return 1
        objs.append(rel_obj)

    print("[2/5] Compilando arquivo Assembly...")
    for src in S_SOURCES:
        rel_obj = os.path.join(BUILD_DIR, os.path.splitext(os.path.basename(src))[0] + ".o")
        cmd = [CC, "-mcpu=cortex-m0", "-mthumb", "-x", "assembler-with-cpp"] + INCLUDES + ["-c", src, "-o", rel_obj]
        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode != 0:
            print(f"\nERRO ao compilar {src}:")
            print(res.stderr)
            return 1
        objs.append(rel_obj)

    elf_file = os.path.join(BUILD_DIR, f"{TARGET}.elf")
    bin_file = os.path.join(BUILD_DIR, f"{TARGET}.bin")
    hex_file = os.path.join(BUILD_DIR, f"{TARGET}.hex")

    print("[3/5] Linkando com eliminacao de dead code e stack pointer correto...")
    link_cmd = [CC] + LDFLAGS + objs + ["-o", elf_file]
    res = subprocess.run(link_cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"\nERRO na linkagem:")
        print(res.stderr)
        return 1

    subprocess.run([SIZE, elf_file])

    print("[4/5] Gerando binario e hex...")
    subprocess.run([OBJCOPY, "-O", "binary", elf_file, bin_file], check=True)
    subprocess.run([OBJCOPY, "-O", "ihex", elf_file, hex_file], check=True)

    print(f"firmware.bin gerado: {os.path.getsize(bin_file)} bytes")
    print(f"firmware.hex gerado: {os.path.getsize(hex_file)} bytes")

    print("[5/5] Criptografando com chave oficial da Radtel...")
    cmd_enc = [ENCRYPT_TOOL, hex_file, ENCRYPT_KEY]
    subprocess.run(cmd_enc, capture_output=True, text=True)

    # Pegar o .btu gerado
    btu_src = os.path.join(BUILD_DIR, f"{TARGET}.btu")
    out_final = r"D:\radio px\BINTOLK_MAIESQUE_CUSTOM.BTU"
    if os.path.exists(btu_src):
        if os.path.exists(out_final):
            os.remove(out_final)
        os.rename(btu_src, out_final)
        print(f"\n=======================================================")
        print(f" >>> SUCESSO TOTAL! FIRMWARE GERADO COM SUCESSO! <<<")
        print(f" Arquivo: {out_final}")
        print(f" Tamanho: {os.path.getsize(out_final)} bytes")
        print(f"=======================================================")
        return 0
    else:
        btus = glob.glob(r"D:\radio px\*.btu")
        print("BTUs encontrados:", btus)

    return 0

if __name__ == "__main__":
    sys.exit(main())
