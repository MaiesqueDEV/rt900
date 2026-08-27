with open("bj7700_fw.bin", "rb") as f:
    data = f.read()

def dump_range(start, end, label=""):
    print(f"\n--- {label} (0x{start:06X} .. 0x{end:06X}) ---")
    chunk = data[start:end]
    for i in range(0, len(chunk), 16):
        row = chunk[i:i+16]
        hex_s = " ".join(f"{b:02X}" for b in row)
        asc_s = "".join(chr(b) if 32 <= b <= 126 else "." for b in row)
        print(f"0x{start+i:06X}: {hex_s:<48} | {asc_s}")

dump_range(0x0007C0, 0x000820, "String de Abertura 1 (0x07E0)")
dump_range(0x0003B0, 0x000410, "String de Abertura 2 (0x03DB)")
dump_range(0x022C70, 0x022D00, "Versao e Strings Finais (0x22C94)")
