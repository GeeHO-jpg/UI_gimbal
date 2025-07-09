import struct
import crcmod

# สร้าง CRC function แบบ STM32 HAL (no reverse, no final xor)
stm32_crc32 = crcmod.mkCrcFun(
    poly=0x104C11DB7,     # ⬅️ 0x04C11DB7 + 1 leading bit
    initCrc=0xFFFFFFFF,   # ⬅️ Default ของ HAL
    rev=False,            # ⬅️ STM32 ใช้ non-reversed
    xorOut=0x00000000     # ⬅️ ไม่มี final xor
)

def encode_packet(cmd: int, data: list[float], flags: int = 0x00) -> bytes:
    header = bytes([0xAA])  # SOF
    cmd_byte = struct.pack("<B", cmd)
    flags_byte = struct.pack("<B", flags)
    data_bytes = struct.pack(f"<{len(data)}f", *data)

    payload = cmd_byte + flags_byte + data_bytes
    crc = stm32_crc32(payload)
    crc_bytes = struct.pack("<I", crc)

    length = len(payload) + len(crc_bytes)  # ✅ รวม CRC ด้วย
    len_byte = struct.pack("<B", length)

    packet = header + len_byte + payload + crc_bytes

    # Debug print
    print("\n📦 Final Encoded Packet (hex):")
    print(' '.join(f'0x{b:02X}' for b in packet))
    print(f"🔐 CRC32: 0x{crc:08X}")

    return packet

