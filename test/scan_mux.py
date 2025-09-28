import os
import time

# Alle Multiplexer-Adressen, die bei dir existieren
MUX_ADDRS = [0x70, 0x71]

def scan_mux():
    for mux in MUX_ADDRS:
        for channel in range(8):
            print(f"\n=== Multiplexer 0x{mux:02X}, Kanal {channel} ===")
            # Aktiviere genau einen Kanal
            os.system(f"i2cset -y 1 0x{mux:02X} 0x{1<<channel:02X}")
            time.sleep(0.1)
            # Scanne jetzt den Bus
            os.system("i2cdetect -y 1")

    # Zum Schluss wieder alle Kanäle deaktivieren
    for mux in MUX_ADDRS:
        os.system(f"i2cset -y 1 0x{mux:02X} 0x00")

if __name__ == "__main__":
    scan_mux()
