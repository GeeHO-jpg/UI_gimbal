from tkinter import Frame, Text, Scrollbar, END, RIGHT, Y

class LogConsole:
    def __init__(self, parent):
        self.frame = Frame(parent)
        self.frame.pack(fill="x", padx=5, pady=2)
        # self.frame = Frame(parent)
        # self.frame.pack(fill="both", expand=True)

        self.text = Text(
            self.frame,
            state='disabled',
            height=10,
            relief="sunken",     # สร้างขอบแบบจม
            bd=2                 # ความหนาของขอบ (border width)
        )
        self.text.pack(side="left", fill="both", expand=True)

        scrollbar = Scrollbar(self.frame, command=self.text.yview)
        scrollbar.pack(side=RIGHT, fill=Y)
        self.text['yscrollcommand'] = scrollbar.set

    def log(self, message):
        self.text.config(state='normal')
        self.text.insert(END, message + '\n')
        self.text.see(END)
        self.text.config(state='disabled')

    def clear(self):
        self.text.config(state='normal')
        self.text.delete(1.0, END)
        self.text.config(state='disabled')
