import subprocess
import os

tool_path = r"D:\radio px\rt900\Tools\ARCEncryptTools.exe"

# Vamos extrair todas as strings legíveis do executável .NET
with open(tool_path, "rb") as f:
    data = f.read()

strings = []
cur = []
for b in data:
    if 32 <= b <= 126:
        cur.append(chr(b))
    else:
        if len(cur) >= 4:
            strings.append("".join(cur))
        cur = []

print(f"Total strings no ARCEncryptTools.exe: {len(strings)}")
for s in strings:
    if any(k in s.lower() for k in ["btu", "encrypt", "crc", "key", "aes", "sha", "md5", "bt8000", "header", "pack"]):
        print(" ->", s)
