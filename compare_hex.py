import os

def analyze_hex(path):
    print(f"\n=== Analyzing {path} ===")
    min_addr = 0xFFFFFFFF
    max_addr = 0
    total_data_bytes = 0
    upper_addr = 0
    records = 0

    with open(path, "r") as f:
        for line in f:
            line = line.strip()
            if not line.startswith(":"):
                continue
            records += 1
            length = int(line[1:3], 16)
            addr = int(line[3:7], 16)
            rectype = int(line[7:9], 16)
            data = line[9:9+length*2]

            if rectype == 0:  # Data record
                full_addr = upper_addr + addr
                min_addr = min(min_addr, full_addr)
                max_addr = max(max_addr, full_addr + length)
                total_data_bytes += length
            elif rectype == 4:  # Extended Linear Address
                upper_addr = int(data, 16) << 16
            elif rectype == 1:  # End of file
                break

    print(f"Records: {records}")
    print(f"Address Range: 0x{min_addr:08X} - 0x{max_addr:08X}")
    print(f"Total Data Bytes: {total_data_bytes} bytes ({total_data_bytes / 1024:.2f} KB)")

analyze_hex(r"D:\radio px\keil_project\Radtel_RT900 20250305\work\EDIE\build\Target 1\WT_BT_8000.hex")
analyze_hex(r"D:\radio px\keil_project\build_gcc\firmware.hex")
