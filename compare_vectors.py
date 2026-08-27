import os

def hex_to_bin(hex_path, start_addr=0x08003000, size=256):
    buf = bytearray(b"\xFF" * size)
    upper = 0
    with open(hex_path, "r") as f:
        for line in f:
            line = line.strip()
            if not line.startswith(":"):
                continue
            length = int(line[1:3], 16)
            addr = int(line[3:7], 16)
            rectype = int(line[7:9], 16)
            data = line[9:9+length*2]
            if rectype == 0:
                full = upper + addr
                for i in range(length):
                    cur = full + i
                    if start_addr <= cur < start_addr + size:
                        buf[cur - start_addr] = int(data[i*2:i*2+2], 16)
            elif rectype == 4:
                upper = int(data, 16) << 16
    return buf

official_vtor = hex_to_bin(r"D:\radio px\keil_project\Radtel_RT900 20250305\work\EDIE\build\Target 1\WT_BT_8000.hex")
gcc_vtor = hex_to_bin(r"D:\radio px\keil_project\build_gcc\firmware.hex")

print("--- Vector Table Oficial (Primeiras 16 entradas de 4 bytes) ---")
for i in range(0, 64, 4):
    val = int.from_bytes(official_vtor[i:i+4], "little")
    val_gcc = int.from_bytes(gcc_vtor[i:i+4], "little")
    print(f"Offset 0x{i:02X} (Vec {i//4:2d}): Oficial = 0x{val:08X}  |  GCC = 0x{val_gcc:08X}")
