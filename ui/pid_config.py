from tkinter import Frame, Label, Entry, Scale, DoubleVar, HORIZONTAL, LEFT, RIGHT, X, Button
from controller.crc import encode_packet


class PIDConfig:
    def __init__(self, parent, log_console=None, serial_controller=None):
        self.frame = Frame(parent)
        self.frame.pack(fill='both', expand=True)

        self.log_console = log_console
        self.serial_controller = serial_controller

        self.pid_vars = {}
        self.filter_vars = {}

        self.create_labeled_section("Filter Settings", self.create_filter_section)
        self.create_labeled_section("PID Parameters", self.create_pid_section)

        # 🔘 ปุ่มบันทึก / ส่งค่า
        save_btn = Button(self.frame, text="Save and Send", command=self.save_and_send)
        save_btn.pack(pady=10)

    def create_labeled_section(self, title, content_fn):
        """Wrapper ใส่กรอบ+หัวข้อด้านบน"""
        outer = Frame(self.frame, bd=2, relief="groove")
        outer.pack(fill=X, padx=10, pady=5)

        # ย้ายหัวข้อไว้บนกรอบ
        Label(outer, text=title, font=('Arial', 10, 'bold'), anchor='w').pack(anchor='w', padx=5, pady=(0, 2))

        # กรอบด้านในสำหรับเนื้อหา
        inner = Frame(outer)
        inner.pack(fill=X, padx=10, pady=5)
        content_fn(inner)

    def create_filter_section(self, parent):
        
        row = Frame(parent)
        row.pack(fill=X)

        # ✅ ค่าตั้งต้นของ Filter
        default_filter_values = {
            "alpha_gyro": 0.1,
            "alpha_output": 0.1
        }

        for name in ["Alpha Gyro", "Alpha Output"]:
            key = name.lower().replace(" ", "_")
            var = DoubleVar(value=default_filter_values.get(key, 1.0)) #fallback = 1.0 ,“ค่าที่จะใช้เป็น ค่าเริ่มต้นสำรอง” ในกรณีที่ไม่พบ key ใน dict ของค่าตั้งต้น
            self.filter_vars[key] = var

            group = Frame(row)
            group.pack(side=LEFT, padx=10)

            Label(group, text=name + ":").pack(anchor='w')
            Entry(group, textvariable=var, width=6).pack(anchor='w', pady=(0, 2))
            Scale(group, from_=0.0, to=1.0, resolution=0.001, orient=HORIZONTAL, variable=var, length=100).pack(anchor='w')

    def create_pid_section(self, parent):
        grid = Frame(parent)
        grid.pack()

        # ✅ ค่าตั้งต้นของ PID แต่ละแกน
        default_pid_values = {
            "Roll_P": 0.0, "Roll_I": 0.0, "Roll_D": 0.0, "Roll_K": 0.0,
            "Pitch_P": 0.0, "Pitch_I": 0.0, "Pitch_D": 0.0, "Pitch_K": 0.0,
            "Yaw_P": 0.0, "Yaw_I": 0.0, "Yaw_D": 0.0, "Yaw_K": 0.0
        }


        # Header
        Label(grid, text="").grid(row=0, column=0)
        for j, axis in enumerate(['Roll', 'Pitch', 'Yaw']):
            Label(grid, text=axis).grid(row=0, column=1 + j * 2, columnspan=2)

        for i, param in enumerate(['P', 'I', 'D', 'K']):
            Label(grid, text=f"{param}:", anchor='e').grid(row=1 + i, column=0, padx=5, sticky='e')
            for j, axis in enumerate(['Roll', 'Pitch', 'Yaw']):
                key = f"{axis}_{param}"
                default_value = default_pid_values.get(key, 1.0)  #fallback = 1.0 ,“ค่าที่จะใช้เป็น ค่าเริ่มต้นสำรอง” ในกรณีที่ไม่พบ key ใน dict ของค่าตั้งต้น
                var = DoubleVar(value=default_value)
                self.pid_vars[key] = var

                Entry(grid, textvariable=var, width=6).grid(row=1 + i, column=1 + j * 2, padx=(10, 20))
                Scale(grid, from_=0.0, to=30.0, resolution=0.001,orient=HORIZONTAL, variable=var, length=100).grid(row=1 + i, column=2 + j * 2, padx=(15, 15))

    def save_and_send(self):

        # print("DEBUG: Save and Send button clicked")
        # รวมค่าทั้งหมด
        params = {k: v.get() for k, v in self.pid_vars.items()}
        filters = {k: v.get() for k, v in self.filter_vars.items()}

        # log preview
        if self.log_console:
            self.log_console.log("[SAVE] PID Parameters:")
            # for k, v in params.items():
            #     self.log_console.log(f"  {k}: {v:.3f}")
            # self.log_console.log("[SAVE] Filter:")
            # for k, v in filters.items():
            #     self.log_console.log(f"  {k}: {v:.3f}")

        # ส่งผ่าน serial (สมมุติใช้ cmd 0x10 และ flags 0x01)
        if self.serial_controller:
            data = list(params.values()) + list(filters.values())
            packet = encode_packet(cmd=0x04, data=data, flags=0x01)
            self.serial_controller.send(packet)
