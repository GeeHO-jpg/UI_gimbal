from apply import setup_ui

if __name__ == "__main__":
    setup_ui()



# import crcmod

# stm32_crc32 = crcmod.mkCrcFun(
#     poly=0x104C11DB7,     # CRC-32 กับ implicit bit
#     initCrc=0xFFFFFFFF,
#     rev=False,
#     xorOut=0x00000000
# )

# # สร้าง input byte array ตาม endian ที่ตรงกับ STM32 (little endian 32-bit)
# data = (
#     b'\x01\x00\x00\x00' +
#     b'\x00\x00\x80\x3F'  

# )

# crc = stm32_crc32(data)
# print(f"✅ STM32 compatible CRC: 0x{crc:08X}")
    
# # import serial
# # print(serial.__file__)
# # print(serial.Serial)