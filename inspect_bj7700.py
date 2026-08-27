import os

btu_path = r"C:\Users\Maiesque\Downloads\BJ7700 NO BT\BJ7700_5W_V1.07_251103.BTU"
with open(btu_path, "rb") as f:
    btu_data = f.read()

header = btu_data[:16]
fw_bin = btu_data[16:]

print(f"File: {btu_path}")
print(f"Total size: {len(btu_data)} bytes")
print(f"Header: {header.hex()}")
print(f"Firmware binary size: {len(fw_bin)} bytes")

# Salvar como binario
with open("bj7700_fw.bin", "wb") as f:
    f.write(fw_bin)

# Procurar todas as strings ASCII legíveis
strings = []
current = []
pos = 0
str_positions = []
for i, b in enumerate(fw_bin):
    if 32 <= b <= 126:
        if not current:
            pos = i
        current.append(chr(b))
    else:
        if len(current) >= 3:
            s = "".join(current)
            strings.append((pos, s))
        current = []

print(f"\nTotal strings encontradas: {len(strings)}")
print("\n--- Strings de Modelo e Abertura ---")
for offset, s in strings:
    if any(k in s.lower() for k in ["7700", "8200", "8000", "900", "bintolk", "radtel", "bajeton", "welcome", "v1.", "v0."]):
        print(f"Offset 0x{offset:06X} (+0x08003000 = 0x{0x08003000 + offset:08X}): {s}")

print("\nPrimeiras 30 strings do firmware:")
for offset, s in strings[:30]:
    print(f"0x{offset:06X}: {s}")
