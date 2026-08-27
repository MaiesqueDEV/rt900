import os

btu_path = r"C:\Users\Maiesque\Downloads\original\BT_8200_MH_V0.18_241214.BTU"
with open(btu_path, "rb") as f:
    btu_data = f.read()

header = btu_data[:16]
fw_bin = btu_data[16:]

print(f"Header (16 bytes): {header.hex()}")
print(f"Firmware binary size: {len(fw_bin)} bytes")

# Salvar binario original desembalado
with open("original_firmware.bin", "wb") as f:
    f.write(fw_bin)

# Procurar strings no binario original
strings = []
current = []
for b in fw_bin:
    if 32 <= b <= 126:
        current.append(chr(b))
    else:
        if len(current) >= 4:
            strings.append("".join(current))
        current = []

print("\n--- Strings encontradas no firmware original BT-8200 ---")
for s in strings:
    if any(k in s.lower() for k in ["radtel", "bt", "bintolk", "v0.", "welcome", "power"]):
        print(" ->", s)

print("\nPrimeiras 20 strings:")
for s in strings[:20]:
    print(" ", s)
