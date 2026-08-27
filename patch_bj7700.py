import os
import subprocess
import glob

# Testar se podemos gerar .hex do bj7700_fw.bin e rodar ARCEncryptTools.exe
# Binario comeca em 0x08003000

TOOLCHAIN_BIN = r"D:\radio px\toolchain\xpack-arm-none-eabi-gcc-13.2.1-1.1\bin"
OBJCOPY = os.path.join(TOOLCHAIN_BIN, "arm-none-eabi-objcopy.exe")
ENCRYPT_TOOL = r"Tools\ARCEncryptTools.exe"
ENCRYPT_KEY = "QzBtDzKjYxGsWalkieTalkieBt8000OpenDate20241202"

# 1. Carregar bj7700_fw.bin original
with open("bj7700_fw.bin", "rb") as f:
    orig_fw = bytearray(f.read())

# 2. Modificar as strings de abertura para "MAIESQUE    "
# Offset 0x0003E0
# Offset 0x0007E0
custom_text = b"MAIESQUE    \x00" # 13 bytes

print("Original em 0x0003E0:", bytes(orig_fw[0x0003E0:0x0003E0+13]))
print("Original em 0x0007E0:", bytes(orig_fw[0x0007E0:0x0007E0+13]))

orig_fw[0x0003E0:0x0003E0+13] = custom_text
orig_fw[0x0007E0:0x0007E0+13] = custom_text

print("Novo em 0x0003E0:", bytes(orig_fw[0x0003E0:0x0003E0+13]))
print("Novo em 0x0007E0:", bytes(orig_fw[0x0007E0:0x0007E0+13]))

# 3. Salvar binario modificado
custom_bin = "bj7700_maiesque.bin"
with open(custom_bin, "wb") as f:
    f.write(orig_fw)

# 4. Converter bin para hex com base 0x08003000
custom_hex = "bj7700_maiesque.hex"
cmd = [OBJCOPY, "-I", "binary", "-O", "ihex", "--change-addresses", "0x08003000", custom_bin, custom_hex]
res = subprocess.run(cmd, capture_output=True, text=True)
print("Objcopy result:", res.returncode, res.stderr)

# 5. Encriptar para BTU
if os.path.exists("firmware.btu"):
    os.remove("firmware.btu")

cmd_enc = [ENCRYPT_TOOL, custom_hex, ENCRYPT_KEY]
res_enc = subprocess.run(cmd_enc, capture_output=True, text=True)
print("Encrypt result:", res_enc.stdout, res_enc.stderr)

btus = glob.glob("*.btu") + glob.glob("*.BTU")
print("BTU gerado:", btus)
if os.path.exists("firmware.btu"):
    out_final = "BJ7700_MAIESQUE_CUSTOM.BTU"
    if os.path.exists(out_final):
        os.remove(out_final)
    os.rename("firmware.btu", out_final)
    print(f"\n>>> SUCESSO! {out_final} gerado ({os.path.getsize(out_final)} bytes) <<<")
