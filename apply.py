from tkinter import Tk, Frame, TOP, BOTTOM, X, BOTH
from ui.serial_config import SerialConfig
from ui.log_console import LogConsole
from ui.button_group import ButtonGroup
from ui.status_console import StatusConsole
from ui.tab_manager import TabManager
from controller.serial_controller import SerialController

def create_main_window():
    window = Tk()
    window.title("Gimbal Config Tool")
    window.geometry("1000x750")
    return window

def create_top_tab(window, serial_controller, log_console):
    """
    สร้างแท็บด้านบนสุดสำหรับการตั้งค่าต่าง ๆ (ผ่าน TabManager)
    """
    top_frame = Frame(window)
    top_frame.pack(side=TOP, fill=BOTH, expand=True)
    return TabManager(top_frame, serial_controller, log_console)

def create_middle_section(window, log_console, serial_controller, tab_manager):
    """
    สร้างส่วนกลาง: Dropdown เลือกพอร์ตและปุ่ม Connect/Clear
    """
    middle_frame = Frame(window)
    middle_frame.pack(side=TOP, fill=X, padx=10, pady=5)

    row_frame = Frame(middle_frame)
    row_frame.pack(side=TOP, fill=X)

    serial_config = SerialConfig(row_frame)
    ButtonGroup(row_frame, log_console, serial_config, serial_controller, tab_manager=tab_manager)

def create_log_console(window):
    """
    สร้างกล่องแสดงข้อความ log (จะนำไป pack ภายหลัง)
    """
    log_console = LogConsole(window)
    # log_console.frame.pack(side=TOP, fill="x", padx=10, pady=(0, 2))
    return log_console

def create_status_bar(window):
    """
    สร้างแถบสถานะด้านล่างสุดของหน้าต่าง
    """
    bottom_frame = Frame(window)
    bottom_frame.pack(side=BOTTOM, fill=X, padx=5, pady=5)
    StatusConsole(bottom_frame)

def setup_ui():
    """
    ฟังก์ชันหลัก เรียกใช้ทุกองค์ประกอบของ UI และจัด layout
    """
    window = create_main_window()

    # ✅ สร้าง log_console ก่อน เพื่อใช้กับ SerialController (แต่ยังไม่ pack)
    log_console = LogConsole(window)
    serial_controller = SerialController(log_callback=log_console.log)

    # ✅ สร้าง UI ส่วนอื่น
    tab_manager = create_top_tab(window, serial_controller, log_console)
    create_middle_section(window, log_console, serial_controller, tab_manager)

    # ✅ แล้วค่อย pack กล่อง log ด้านล่าง
    log_console.frame.pack(side=BOTTOM, fill="x", padx=10, pady=(5, 10))

    # create_status_bar(window)  # StatusConsole อยู่ล่างสุด

    log_console.log("[READY] UI Initialized.")
    window.mainloop()
