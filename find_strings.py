import os

with open("bj7700_fw.bin", "rb") as f:
    data = f.read()

# Pesquisar strings de texto na interface
print("--- Todas as strings com mais de 4 caracteres legíveis ---")
s_list = []
cur = []
pos = 0
for i, b in enumerate(data):
    if 32 <= b <= 126:
        if not cur:
            pos = i
        cur.append(chr(b))
    else:
        if len(cur) >= 4:
            s = "".join(cur)
            # Filtrar para ver strings de menu e tela
            s_list.append((pos, s))
        cur = []

# Exibir as mais interessantes
for pos, s in s_list:
    if any(c.isupper() for c in s) and len(s) >= 4:
        # Se contem letras legiveis
        if any(w in s for w in ["VOL", "BAT", "SQL", "STEP", "TXP", "SAVE", "VOX", "ABR", "TDR", "BEEP", "TOT", "ROGER", "BT-", "V1.", "MODE", "SCAN"]):
            print(f"0x{pos:06X} (Flash: 0x{0x08003000 + pos:08X}): {s}")
