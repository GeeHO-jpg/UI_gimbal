from tkinter import Frame, Button, Label
from tkinter.ttk import Notebook
from controller.crc import encode_packet

class CalibrationConfig:
    def __init__(self, parent, log_console=None, serial_controller=None):
        self.frame = Frame(parent)
        self.frame.pack(fill="both", expand=True)

        self.log_console = log_console
        self.serial_controller = serial_controller   # ✅ เก็บ serial_controller ไว้
        self.step = 0
        self.total_steps = 6

        self.create_accel_tab()

    def create_accel_tab(self):
        Label(self.frame, text="Calibration", font=("Arial", 14)).pack(pady=10)

        # ✅ สร้าง container สำหรับปุ่มต่าง ๆ
        button_frame = Frame(self.frame)
        button_frame.pack(pady=10)

        # ✅ ปุ่มแคล Accel
        self.start_btn = Button(button_frame, text="Start Accel Calibration", width=20, command=self.calibration_ACC)
        self.start_btn.pack(side="left", padx=10)

        # ✅ ปุ่มแคล Gyro (เริ่มต้น disabled)
        self.gyro_btn = Button(button_frame, text="Start Gyro Calibration", width=20, state="disabled", command=self.calibration_gyro)
        self.gyro_btn.pack(side="left", padx=10)

        # ✅ ปุ่ม Reset
        self.reset_btn = Button(button_frame, text="Reset Calibration", width=20, command=self.reset_calibration)
        self.reset_btn.pack(side="left", padx=10)


    def calibration_ACC(self):
        if self.step < self.total_steps:
            message = f"[CALIB] Step {self.step + 1} of {self.total_steps} in progress..."
            if self.log_console:
                self.log_console.log(message)

             # ✅ ส่งผ่าน Serial
            self.send_calibration_flag(cmd=0x01, data=[0.0],flags=0x01)
            self.step += 1
        else:
            self.log_console.log("[CALIB] ✅ Accel Calibration Completed.")
            self.accel_done = True
            self.step = 0
            self.start_btn.config(state="disabled")     # 🔒 ล็อกปุ่ม Accel
            self.gyro_btn.config(state="normal")        # 🔓 ปลดล็อก Gyro

    def calibration_gyro(self):
        if not self.accel_done:
            self.log_console.log("[CALIB] ⚠️ Please finish Accel calibration first.")
            return

        self.log_console.log("[CALIB] ⚙️ Starting Gyro Calibration...")
        self.send_calibration_flag(cmd=0x02, data=[0.0], flags=0x01)
        self.gyro_done = True
        self.gyro_btn.config(state="disabled")          # 🔒 ล็อกปุ่ม Gyro
        self.log_console.log("[CALIB] ✅ Gyro Calibration Sent.")

    def reset_calibration(self):
        self.log_console.log("[RESET] 🔁 Resetting Calibration State...")
        self.step = 0
        self.accel_done = False
        self.gyro_done = False
        self.start_btn.config(state="normal")
        self.gyro_btn.config(state="disabled")
        self.send_calibration_flag(cmd=0x03, data=[0.0], flags=0x01)
        self.log_console.log("[RESET] ♻️ All Calibration States Reset.")
        self.log_console.log("[RESET] Please press the reset bottom on the board <T_T>")


    def send_calibration_flag(self,cmd, data,flags):
        if self.serial_controller:
            packet = encode_packet(cmd, data,flags)  # ค่า float 1.0 เพื่อให้ encode_packet ทำงานได้
            self.serial_controller.send(packet)
        else:
            self.log_console.log("[ERROR] Serial not connected.")