from tkinter import ttk
from ui.home import HomeTab
from ui.pid_config import PIDConfig
from ui.imu_config import IMUConfig
from ui.motor_config import MotorConfig
from ui.calibration import CalibrationConfig

class TabManager:
    def __init__(self, parent, serial_controller, log_console):
        self.log_console = log_console
        self.serial_controller = serial_controller
        self.notebook = ttk.Notebook(parent)
        self.notebook.pack(expand=True, fill='both')
        self.tab_ids = {}

        # ✅ เพิ่มแท็บ Home (index 0)
        home_tab = HomeTab(self.notebook)
        self.notebook.add(home_tab.frame, text="Home")
        self.tab_ids["home"] = self.notebook.index("end") - 1

        # ✅ เพิ่มแท็บอื่น ๆ
        tabs = [
            ("Calibrate", lambda parent: CalibrationConfig(parent, log_console, serial_controller)),
            ("PID", lambda parent: PIDConfig(parent, log_console, serial_controller)),
            ("Motor", lambda parent: MotorConfig(parent, log_console, serial_controller)),
        ]

        for name, TabClass in tabs:
            tab = TabClass(self.notebook)
            self.notebook.add(tab.frame, text=name)
            self.tab_ids[name.lower()] = self.notebook.index("end") - 1

        # ✅ เริ่มต้นโดยล็อกทุกแท็บ ยกเว้น Home
        self.set_tabs_enabled(False)

    def set_tabs_enabled(self, enabled: bool):
        for key, tab_index in self.tab_ids.items():
            if key == "home":
                continue
            self.notebook.tab(tab_index, state="normal" if enabled else "disabled")

        # ✅ กลับไปที่หน้า Home ถ้ายังไม่ได้เชื่อมต่อ
        if not enabled:
            self.notebook.select(self.tab_ids["home"])
