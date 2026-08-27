import os

def rc4(data: bytes, key: bytes) -> bytes:
    # Key-scheduling algorithm (KSA)
    S = list(range(256))
    j = 0
    for i in range(256):
        j = (j + S[i] + key[i % len(key)]) % 256
        S[i], S[j] = S[j], S[i]
    
    # Pseudo-random generation algorithm (PRGA)
    i = 0
    j = 0
    out = bytearray(len(data))
    for k in range(len(data)):
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        out[k] = data[k] ^ S[(S[i] + S[j]) % 256]
    return bytes(out)

key = b"QzBtDzKjYxGsWalkieTalkieBt8000OpenDate20241202"

# 1. Carregar BTU original de 143.288 bytes
btu_path = r"C:\Users\Maiesque\Downloads\BJ7700 NO BT\BJ7700_5W_V1.07_251103.BTU"
with open(btu_path, "rb") as f:
    btu_data = f.read()

header = btu_data[:16]
payload = btu_data[16:]

print(f"Header: {header.hex()}")
print(f"Payload size: {len(payload)} bytes")

# 2. Testar RC4 por blocos de 1024 bytes (ou stream contínuo)
# No ARCEncryptTools, cada bloco de 1024 bytes reinicia o sbox ou é contínuo?
# Vamos testar contínuo:
dec_full = rc4(payload, key)

# Testar por blocos de 1024 (0x400):
dec_blocks = bytearray()
for chunk_start in range(0, len(payload), 1024):
    chunk = payload[chunk_start:chunk_start+1024]
    dec_blocks.extend(rc4(chunk, key))

print("\n--- Verificando se decriptação contínua gerou vetor ARM Cortex-M0 ---")
print("Contínuo primeiros 16 bytes:", dec_full[:16].hex())
print("Blocos 1024 primeiros 16 bytes:", dec_blocks[:16].hex())
print("Original sem RC4 primeiros 16 bytes:", payload[:16].hex())
