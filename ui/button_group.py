from tkinter import Frame, Button, messagebox, DISABLED, NORMAL
from controller.crc import encode_packet

class ButtonGroup:
    def __init__(self, parent, log_console, serial_config, serial_controller, tab_manager=None):
        self.frame = Frame(parent)
        self.frame.pack(side="left", padx=5, pady=5)

        self.log_console = log_console
        self.serial_config = serial_config
        self.serial_controller = serial_controller
        self.tab_manager = tab_manager

        self.write_hold_active = False
        self.write_repeat_job = None

        self.connect_btn = Button(self.frame, text="Connect", command=self.toggle_connection)
        self.connect_btn.pack(side="left", padx=5)

        # 🔒 ปุ่มควบคุมอื่น ๆ
        self.clear_log_btn = Button(self.frame, text="Clear Log", command=self.on_clear_log, state=DISABLED)
        self.clear_log_btn.pack(side="left", padx=5)

        self.clear_data_btn = Button(self.frame, text="Clear data", command=self.on_clear_data, state=DISABLED)
        self.clear_data_btn.pack(side="left", padx=5)

        self.write_btn = Button(self.frame, text="Write EEPROM", state=DISABLED)
        self.write_btn.pack(side="left", padx=5)
        self.write_btn.bind("<ButtonPress-1>", lambda e: self.start_write_loop())
        self.write_btn.bind("<ButtonRelease-1>", lambda e: self.stop_write_loop())

    def toggle_connection(self):
        port, baud = self.serial_config.get_selected()
        if not self.serial_controller.is_connected():
            if self.serial_controller.connect(port, baud):
                self.connect_btn.config(text="Disconnect")
                self.log_console.log(f"[CONNECT] Connected to {port} @ {baud}")
                self.set_buttons_enabled(True)
                if self.tab_manager:
                    self.tab_manager.set_tabs_enabled(True)
        else:
            self.serial_controller.disconnect()
            self.connect_btn.config(text="Connect")
            self.log_console.log(f"[DISCONNECT] Disconnected from {port}")
            self.set_buttons_enabled(False)
            if self.tab_manager:
                self.tab_manager.set_tabs_enabled(False)

    def set_buttons_enabled(self, enabled):
        state = NORMAL if enabled else DISABLED
        self.clear_log_btn.config(state=state)
        self.clear_data_btn.config(state=state)
        self.write_btn.config(state=state)

    def on_clear_log(self):
        self.log_console.clear()

    def on_clear_data(self):
        confirm = messagebox.askokcancel(
            "Confirm Clear",
            "คุณแน่ใจหรือไม่ว่าต้องการล้างข้อมูลทั้งหมด?",
            icon="warning"
        )
        if confirm:
            packet = encode_packet(0x99, [0.0], 0x00)
            self.serial_controller.send(packet)
            self.log_console.log("[DATA] ⚠️ Cleared data sent.")
        else:
            self.log_console.log("[DATA] ❎ Clear data canceled.")

    def start_write_loop(self):
        self.write_hold_active = True
        self.send_write_packet()

    def send_write_packet(self):
        if not self.write_hold_active:
            return
        packet = encode_packet(cmd=0x10, data=[0.0], flags=0x01)
        self.serial_controller.send(packet)
        self.log_console.log("[WRITE] ✏️ Writing config to EEPROM...")

        # self.write_repeat_job = self.frame.after(500, self.send_write_packet)

    def stop_write_loop(self):
        self.write_hold_active = False
        if self.write_repeat_job:
            self.frame.after_cancel(self.write_repeat_job)
            self.write_repeat_job = None

        packet = encode_packet(cmd=0x10, data=[0.0], flags=0x00)
        self.serial_controller.send(packet)
        self.log_console.log("[WRITE] 🛑 Write command stopped")
