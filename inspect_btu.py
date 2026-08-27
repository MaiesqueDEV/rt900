import os

orig_path = r"C:\Users\Maiesque\Downloads\original\BT_8200_MH_V0.18_241214.BTU"
with open(orig_path, "rb") as f:
    data = f.read()

print(f"File: {orig_path}")
print(f"Size: {len(data)} bytes")
print("Hex head:", data[:64].hex())
print("Hex tail:", data[-64:].hex())
