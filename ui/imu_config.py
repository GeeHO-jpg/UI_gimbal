from tkinter import Frame, Label

class IMUConfig:
    def __init__(self, parent):
        self.frame = Frame(parent)
        self.frame.pack()
        Label(self.frame, text="IMU Configuration").pack()
