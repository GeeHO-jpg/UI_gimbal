import serial

class SerialController:
    def __init__(self, log_callback=None):
        self.ser = None
        self.log_callback = log_callback or print

    def connect(self, port, baud):
        try:
            self.ser = serial.Serial(port, int(baud), timeout=1)
            self.log_callback(f"[CONNECTED] {port} @ {baud}bps")
            return True
        except Exception as e:
            self.log_callback(f"[ERROR] Failed to connect: {e}")
            return False

    def disconnect(self):
        if self.ser and self.ser.is_open:
            self.ser.close()
            self.log_callback("[DISCONNECTED] Port closed.")

    def is_connected(self):
        return self.ser and self.ser.is_open
    
    def send(self, data):
        if self.is_connected():
            if isinstance(data, str):
                self.ser.write(data.encode())
            elif isinstance(data, bytes):
                self.ser.write(data)
            else:
                raise ValueError("Data must be str or bytes")

            # if self.log_callback:
                # self.log_callback(f"[TX] {data}")
