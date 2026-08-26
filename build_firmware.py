import os
import subprocess
import sys
import glob

TOOLCHAIN_BIN = r"D:\radio px\toolchain\xpack-arm-none-eabi-gcc-13.2.1-1.1\bin"
CC = os.path.join(TOOLCHAIN_BIN, "arm-none-eabi-gcc.exe")
OBJCOPY = os.path.join(TOOLCHAIN_BIN, "arm-none-eabi-objcopy.exe")
SIZE = os.path.join(TOOLCHAIN_BIN, "arm-none-eabi-size.exe")

BUILD_DIR = "build"
TARGET = "firmware"
ENCRYPT_TOOL = r"Tools\ARCEncryptTools.exe"
ENCRYPT_KEY = "QzBtDzKjYxGsWalkieTalkieBt8000OpenDate20241202"

INCLUDES = [
    "-IApp",
    "-IBSP",
    "-ICommon",
    "-ICore",
    "-ICPS",
    "-IDriver",
    "-IGui",
    "-IInterface",
    "-ILibraries",
    "-IVoice",
    "-I.",
    "-ILibraries/CMSIS/Include",
    "-ILibraries/StdPeriph_Driver/inc"
]

CFLAGS = [
    "-Os", "-Wall", "-mcpu=cortex-m0", "-mthumb",
    "-fno-builtin", "-fshort-enums", "-fno-delete-null-pointer-checks",
    "-std=c11", "-DUSE_FULL_ASSERT=1", "-DUSE_STDPERIPH_DRIVER",
    "-Wno-unused-variable", "-Wno-maybe-uninitialized", "-Wno-format",
    "-Wno-switch", "-Wno-attributes", "-Wno-pointer-sign",
    "-Wno-unused-but-set-variable", "-Wno-implicit-function-declaration",
    "-D__nop=__NOP"
]

LDFLAGS = [
    "-mcpu=cortex-m0", "-mthumb", "-nostartfiles",
    "-Wl,-T,firmware.ld", f"-Wl,-Map={BUILD_DIR}/{TARGET}.map",
    "-specs=nano.specs", "-specs=nosys.specs"
]

C_SOURCES = [
    "Libraries/StdPeriph_Driver/src/bt32f0x_adc.c",
    "Libraries/StdPeriph_Driver/src/bt32f0x_comp.c",
    "Libraries/StdPeriph_Driver/src/bt32f0x_crc.c",
    "Libraries/StdPeriph_Driver/src/bt32f0x_dbgmcu.c",
    "Libraries/StdPeriph_Driver/src/bt32f0x_divqsrt.c",
    "Libraries/StdPeriph_Driver/src/bt32f0x_dma.c",
    "Libraries/StdPeriph_Driver/src/bt32f0x_exti.c",
    "Libraries/StdPeriph_Driver/src/bt32f0x_flash.c",
    "Libraries/StdPeriph_Driver/src/bt32f0x_gpio.c",
    "Libraries/StdPeriph_Driver/src/bt32f0x_i2c.c",
    "Libraries/StdPeriph_Driver/src/bt32f0x_iwdg.c",
    "Libraries/StdPeriph_Driver/src/bt32f0x_misc.c",
    "Libraries/StdPeriph_Driver/src/bt32f0x_opa.c",
    "Libraries/StdPeriph_Driver/src/bt32f0x_pwr.c",
    "Libraries/StdPeriph_Driver/src/bt32f0x_rcc.c",
    "Libraries/StdPeriph_Driver/src/bt32f0x_rtc.c",
    "Libraries/StdPeriph_Driver/src/bt32f0x_spi.c",
    "Libraries/StdPeriph_Driver/src/bt32f0x_syscfg.c",
    "Libraries/StdPeriph_Driver/src/bt32f0x_tim.c",
    "Libraries/StdPeriph_Driver/src/bt32f0x_usart.c",
    "Libraries/StdPeriph_Driver/src/bt32f0x_wwdg.c",
    "Libraries/StdPeriph_Driver/src/system_bt32f0x.c",
    "App/main.c",
    "App/AppAlarm.c",
    "App/AppDtmf.c",
    "App/AppFm.c",
    "App/AppMain.c",
    "App/AppMenu.c",
    "App/AppMoni.c",
    "App/AppScan.c",
    "App/AppScanQT.c",
    "App/AppSearch.c",
    "App/AppTask.c",
    "App/AppWeather.c",
    "App/Battery.c",
    "App/DualStandby.c",
    "BSP/Board.c",
    "BSP/BoardFun.c",
    "BSP/bt32f0x_it.c",
    "Common/BitMap.c",
    "Common/Delay.c",
    "Common/Globe.c",
    "Common/assert_failed_stub.c",
    "Core/Functions.c",
    "Core/Radio.c",
    "Core/RadioTask.c",
    "CPS/ProgromFlash.c",
    "Driver/crc.c",
    "Driver/DevBK4819.c",
    "Driver/DevBK4819Data.c",
    "Driver/FlashFont.c",
    "Driver/key_ptt.c",
    "Driver/keyboard.c",
    "Driver/NorFlash.c",
    "Driver/RadioDataReset.c",
    "Driver/RadioDataStorage.c",
    "Driver/Rda5807.c",
    "Driver/st7735s.c",
    "Driver/Systick.c",
    "Gui/DisplayBattery.c",
    "Gui/DisplayDtmf.c",
    "Gui/DisplayFm.c",
    "Gui/DisplayInputbox.c",
    "Gui/DisplayMain.c",
    "Gui/DisplayMenu.c",
    "Gui/DisplayPowerOn.c",
    "Gui/DisplayScanQT.c",
    "Gui/DisplaySearch.c",
    "Gui/DisplayWeather.c",
    "Gui/LcdFillDot.c",
    "Interface/i2c.c",
    "Voice/Beep.c",
    "Voice/VoiceBroadcast.c"
]

S_SOURCES = [
    "Libraries/CMSIS/Device/startup_bt32f0x.s"
]

def main():
    os.makedirs(BUILD_DIR, exist_ok=True)
    objs = []

    print("[1/5] Compilando arquivos C...")
    for src in C_SOURCES:
        if not os.path.exists(src):
            print(f"ERRO: Arquivo nao encontrado: {src}")
            return 1
        rel_obj = os.path.join(BUILD_DIR, os.path.splitext(src)[0] + ".o")
        os.makedirs(os.path.dirname(rel_obj), exist_ok=True)
        cmd = [CC] + CFLAGS + INCLUDES + ["-c", src, "-o", rel_obj]
        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode != 0:
            print(f"\nERRO ao compilar {src}:")
            print(res.stderr)
            print(res.stdout)
            return 1
        objs.append(rel_obj)

    print("[2/5] Compilando arquivos Assembly...")
    for src in S_SOURCES:
        rel_obj = os.path.join(BUILD_DIR, os.path.splitext(src)[0] + ".o")
        os.makedirs(os.path.dirname(rel_obj), exist_ok=True)
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

    print("[3/5] Linkando firmware.elf...")
    link_cmd = [CC] + LDFLAGS + objs + ["-o", elf_file]
    res = subprocess.run(link_cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"\nERRO na linkagem:")
        print(res.stderr)
        return 1

    subprocess.run([SIZE, elf_file])

    print("[4/5] Gerando arquivos .bin e .hex...")
    subprocess.run([OBJCOPY, "-O", "binary", elf_file, bin_file], check=True)
    subprocess.run([OBJCOPY, "-O", "ihex", elf_file, hex_file], check=True)

    print(f"firmware.bin gerado: {os.path.getsize(bin_file)} bytes")
    print(f"firmware.hex gerado: {os.path.getsize(hex_file)} bytes")

    print("[5/5] Criptografando firmware com chave oficial -> .BTU...")
    if os.path.exists(ENCRYPT_TOOL):
        cmd = [ENCRYPT_TOOL, hex_file, ENCRYPT_KEY]
        res = subprocess.run(cmd, capture_output=True, text=True)
        print("Output ARCEncryptTools:", res.stdout, res.stderr)
        
        # Procurar .btu gerado
        btus = glob.glob("*.btu") + glob.glob("*.BTU") + glob.glob(os.path.join(BUILD_DIR, "*.btu"))
        if btus:
            btu_file = btus[0]
            out_btu = "RT900_MAIESQUE_CUSTOM.BTU"
            if os.path.exists(out_btu):
                os.remove(out_btu)
            os.rename(btu_file, out_btu)
            print(f"\n=======================================================")
            print(f" >>> SUCESSO TOTAL! FIRMWARE GERADO COM SUCESSO! <<<")
            print(f" Arquivo: {os.path.abspath(out_btu)}")
            print(f" Tamanho: {os.path.getsize(out_btu)} bytes")
            print(f"=======================================================")
            return 0
        else:
            print("Aviso: arquivo .btu nao foi detectado na saida do encriptador.")
    else:
        print(f"Aviso: {ENCRYPT_TOOL} nao encontrado.")

    print("\nFirmware .hex e .bin compilados com sucesso!")
    return 0

if __name__ == "__main__":
    sys.exit(main())
