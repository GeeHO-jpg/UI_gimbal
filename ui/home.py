from tkinter import Frame, Label, Canvas, CENTER

class HomeTab:
    def __init__(self, parent):
        self.frame = Frame(parent, bg="white")
        self.frame.pack(fill="both", expand=True)

        # ✅ Canvas พื้นหลัง
        canvas = Canvas(self.frame, bg="white", highlightthickness=0)
        canvas.pack(fill="both", expand=True)

        # ✅ เมื่อขนาดเปลี่ยน ให้ update RCSA และ center frame
        def draw_rcsa(event=None):
            canvas.delete("all")

            width = canvas.winfo_width()
            height = canvas.winfo_height()

            # ✅ วาดตัวอักษร RCSA กลางจอ
            canvas.create_text(
                width / 2,
                height / 2,
                text="RCSA",
                font=("Arial", int(height * 0.3), "bold"),
                fill="#eeeeee",
                angle=30
            )

            # ✅ สร้างกล่องข้อความแล้ววางด้วย x/y ไม่ใช้ relx/rely
            center_frame = Frame(canvas, bg="white")
            canvas.create_window(width / 2, height * 0.4, window=center_frame, anchor=CENTER)

            Label(
                center_frame,
                text="🔌 กรุณาเชื่อมต่อพอร์ตก่อนใช้งาน",
                font=("Arial", 16, "bold"),
                fg="#222",
                bg="white"
            ).pack(pady=(10, 5))

            Label(
                center_frame,
                text="ระบบจะปลดล็อกเมนูเมื่อมีการเชื่อมต่อกับพอร์ตสำเร็จ",
                font=("Arial", 12),
                fg="#666",
                bg="white"
            ).pack()

        canvas.bind("<Configure>", draw_rcsa)
