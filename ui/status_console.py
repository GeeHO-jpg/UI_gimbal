from tkinter import Frame, Label

class StatusConsole:
    # def __init__(self, parent):
    #     self.frame = Frame(parent)
    #     self.frame.pack(fill='x')
    #     Label(self.frame, text="Status: OK").pack()
    def __init__(self, parent):
        self.label = Label(
            parent,
            text="Status: OK",
            anchor="w",
            height=1,         # ✅ ลดความสูงลงเหลือ 1 line
            pady=0,           # ✅ ไม่เว้น padding ภายใน
            font=("Arial", 5)  # (ถ้าอยากให้เล็กลงอีก)
        )
        self.label.pack(fill="x")
