from tkinter import Frame, Label, StringVar, OptionMenu, LEFT
import serial.tools.list_ports

class SerialConfig:
    def __init__(self, parent, default_baud="115200"):
        # สร้างเฟรมย่อยสำหรับวาง Port/baudrate dropdown ในบรรทัดเดียว
        self.frame = Frame(parent)
        self.frame.pack(side="left", padx=10, pady=5)

        # ---------- COM Port Dropdown ----------

        # StringVar สำหรับเก็บค่าที่ผู้ใช้เลือกจาก dropdown
        self.port_var = StringVar()

        # เรียกฟังก์ชันเพื่อดึง dict {"COM3": "COM3 (CH340)", ...}
        self.port_dict = self.get_ports_with_description()

        # เอาค่า value จาก dict มาทำรายการให้ OptionMenu แสดงผล
        port_list_display = list(self.port_dict.values())

        # ถ้ามี COM อย่างน้อย 1 ตัว ให้เลือกอันแรกเป็นค่าเริ่มต้น
        self.port_var.set(port_list_display[0] if port_list_display else "No COM Found")

        # ป้ายข้อความ "Port:"
        Label(self.frame, text="Port:").pack(side=LEFT)

        # Dropdown สำหรับเลือก COM Port + ชื่อ
        OptionMenu(self.frame, self.port_var, *port_list_display).pack(side=LEFT, padx=5)

        # ---------- Baudrate Dropdown ----------

        # StringVar สำหรับ baudrate dropdown
        self.baud_var = StringVar()

        # รายการ baudrate ที่กำหนดไว้ล่วงหน้า
        self.baud_options = ["9600", "19200", "38400", "57600", "115200"]

        # กำหนดค่า default
        self.baud_var.set(default_baud)

        # ป้าย "Baudrate:"
        Label(self.frame, text="Baudrate:").pack(side=LEFT, padx=(10, 2))

        # Dropdown สำหรับเลือก baudrate
        OptionMenu(self.frame, self.baud_var, *self.baud_options).pack(side=LEFT, padx=5)

    def get_ports_with_description(self):
        """
        ดึงรายการ COM Port ทั้งหมด พร้อมคำอธิบาย เช่น:
        {'COM3': 'COM3 (CH340)', 'COM4': 'COM4 (Bluetooth)'}
        """
        ports = serial.tools.list_ports.comports()
        return {port.device: f"{port.device} ({port.description})" for port in ports}

    def get_selected(self):
        """
        คืนค่า (port, baudrate) ที่ผู้ใช้เลือก เช่น:
        ('COM3', '115200')
        """
        # หาค่า device (COMx) จาก label ที่ถูกเลือก
        display_value = self.port_var.get()
        for device, label in self.port_dict.items():
            if label == display_value:
                return device, self.baud_var.get()

        # ถ้าไม่เจอ ให้คืน None และ baudrate ปัจจุบัน
        return None, self.baud_var.get()
