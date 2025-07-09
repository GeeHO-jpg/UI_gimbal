from tkinter import Frame, Label, OptionMenu, StringVar, Button,Scale, IntVar ,Entry, HORIZONTAL, LEFT, X 
from controller.crc import encode_packet

class MotorConfig:
    def __init__(self, parent, log_console=None, serial_controller=None):
        self.frame = Frame(parent)
        self.frame.pack(fill="both", expand=True)

        self.log_console = log_console
        self.serial_controller = serial_controller

        self.pole_vars = {}
        self.yaw_hold_active = False  # 🆕 state สำหรับ hold button
        self.yaw_repeat_job = None

        Label(self.frame, text="MOTOR Configuration", font=("Arial", 12, "bold")).pack(pady=(10, 5))

        self.create_pole_section()
        self.create_torque_section()  
        self.create_yaw_align_section()

    def create_pole_section(self):
        pole_box = Frame(self.frame, bd=2, relief="groove", padx=10, pady=10)
        pole_box.pack(padx=10, pady=5, fill=X)

        Label(pole_box, text="Pole", font=("Arial", 10, "bold")).pack(anchor="w")

        axis_frame = Frame(pole_box)
        axis_frame.pack()

        for axis in ["Roll", "Pitch", "Yaw"]:
            col = Frame(axis_frame, padx=10)
            col.pack(side=LEFT)
            Label(col, text=axis).pack()
            self.pole_vars[axis.lower()] = StringVar(value="0")
            OptionMenu(col, self.pole_vars[axis.lower()],*map(str, range(0, 51))).pack()

        Button(pole_box, text="Submit", command=self.submit_pole).pack(pady=10)

    def create_torque_section(self):
        torque_box = Frame(self.frame, bd=2, relief="groove", padx=10, pady=10)
        torque_box.pack(padx=10, pady=5, fill=X)

        Label(torque_box, text="Percent Torque Configuration", font=("Arial", 10, "bold")).pack(anchor="w")

        axis_frame = Frame(torque_box)
        axis_frame.pack()

        self.torque_vars = {}

        for axis in ["Roll", "Pitch", "Yaw"]:
            col = Frame(axis_frame, padx=10)
            col.pack(side=LEFT)

            Label(col, text=axis, font=("Arial", 10)).pack()

           # ตัวแปรผูก Scale กับ Entry
            var = IntVar(value=0)
            self.torque_vars[axis.lower()] = var

            # Entry box
            entry = Entry(col, textvariable=var, width=5, justify='center')
            entry.pack(pady=2)

            # Scale bar
            scale = Scale(
                col,
                from_=0, to=100,
                orient=HORIZONTAL,
                variable=var,
                length=120
            )
            scale.pack()

        Button(torque_box, text="Submit", command=self.submit_torque).pack(pady=10)

    def create_yaw_align_section(self):
        align_box = Frame(self.frame, bd=2, relief="groove", padx=10, pady=10)
        align_box.pack(padx=10, pady=5, fill=X)

        Label(align_box, text="Align the yaw axis", font=("Arial", 10, "bold")).pack(anchor="w")

        button_row = Frame(align_box)
        button_row.pack(pady=5)

        arrows = ["<<<", "<<", "<", "...", ">", ">>", ">>>"]
        for label in arrows:
            btn = Button(button_row, text=label, width=4)
            btn.pack(side=LEFT, padx=2)

            # 🆕 bind กด-ปล่อย
            btn.bind("<ButtonPress-1>", lambda e, l=label: self.start_yaw_align(l))
            btn.bind("<ButtonRelease-1>", lambda e: self.stop_yaw_align())

    def submit_pole(self):
        values = {axis: int(var.get()) for axis, var in self.pole_vars.items()}
        data = [values["roll"], values["pitch"], values["yaw"]]
        packet = encode_packet(cmd=0x06, data=data, flags=0x01)

        if self.serial_controller:
            self.serial_controller.send(packet)
        if self.log_console:
            self.log_console.log(f"[SUBMIT] Pole: {values}")

    def start_yaw_align(self, label):
        self.yaw_hold_active = True
        self.repeat_yaw_command(label)

    def repeat_yaw_command(self, label):
        if not self.yaw_hold_active:
            return
        value = self.label_to_value(label)
        packet = encode_packet(cmd=0x05, data=[value], flags=0x01)
        if self.serial_controller:
            self.serial_controller.send(packet)
        if self.log_console:
            self.log_console.log(f"[ALIGN] Sending yaw: {label} → {value}")

        # repeat every 100 ms while holding
        self.yaw_repeat_job = self.frame.after(100, lambda: self.repeat_yaw_command(label))

    def stop_yaw_align(self):
        self.yaw_hold_active = False
        if self.yaw_repeat_job:
            self.frame.after_cancel(self.yaw_repeat_job)
            self.yaw_repeat_job = None

        # 🆕 ส่งค่า 0 เมื่อปล่อยปุ่ม
        packet = encode_packet(cmd=0x05, data=[0], flags=0x01)
        if self.serial_controller:
            self.serial_controller.send(packet)
        if self.log_console:
            self.log_console.log(f"[ALIGN] Stopped yaw control → sent 0")

    def label_to_value(self, label):
        """
        แปลงข้อความปุ่มเป็นค่าควบคุม เช่น <<< → -3, >> → +2
        """
        mapping = {
            "<<<": -5,
            "<<": -3,
            "<": -1,
            "...": 0,
            ">": 1,
            ">>": 3,
            ">>>": 5
        }
        return mapping.get(label, 0)
    
    def submit_torque(self):
        values = {axis: var.get() for axis, var in self.torque_vars.items()}
        data = [values["roll"], values["pitch"], values["yaw"]]
        packet = encode_packet(cmd=0x07, data=data, flags=0x01)

        if self.serial_controller:
            self.serial_controller.send(packet)
        if self.log_console:
            self.log_console.log(f"[SUBMIT] Percent Torque: {values}")
