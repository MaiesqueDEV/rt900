import os

# 1. Carregar BTU original de 143.288 bytes
orig_btu_path = r"C:\Users\Maiesque\Downloads\BJ7700 NO BT\BJ7700_5W_V1.07_251103.BTU"
with open(orig_btu_path, "rb") as f:
    orig_btu_data = bytearray(f.read())

header = orig_btu_data[:16]
fw_data = orig_btu_data[16:]

print(f"Header: {header.hex()}")
print(f"FW Size: {len(fw_data)} bytes")

# 2. Localizar onde fica "BT-7900" no BTU completo (com header de 16 bytes)
# Offset no binario: 0x0003E0 e 0x0007E0
# Offset no BTU: 16 + 0x0003E0 = 0x0003F0
# Offset no BTU: 16 + 0x0007E0 = 0x0007F0

pos1 = 16 + 0x0003E0
pos2 = 16 + 0x0007E0

print("Bytes originais em pos1:", orig_btu_data[pos1:pos1+16])
print("Bytes originais em pos2:", orig_btu_data[pos2:pos2+16])

# 3. Substituir por "MAIESQUE    \0"
custom_name = b"MAIESQUE    \x00"
orig_btu_data[pos1:pos1+len(custom_name)] = custom_name
orig_btu_data[pos2:pos2+len(custom_name)] = custom_name

print("Bytes modificados em pos1:", orig_btu_data[pos1:pos1+16])
print("Bytes modificados em pos2:", orig_btu_data[pos2:pos2+16])

# 4. Salvar o arquivo BTU customizado final
output_btu = "BJ7700_MAIESQUE_CUSTOM.BTU"
with open(output_btu, "wb") as f:
    f.write(orig_btu_data)

print(f"\n>>> SUCESSO! Arquivo gerado: {output_btu} ({len(orig_btu_data)} bytes) <<<")
