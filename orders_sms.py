import tkinter as tk

class Application:
    def __init__(self, master):
        self.master = master
        self.default_font = font = ("Verdana", 10)
        
        self.init_master()
        self.create_buttons()

    def init_master(self):
        self.master.geometry("300x50")
        self.master.title("SMS order")
        self.master.overrideredirect(True)
        self.master.attributes('-topmost', True)

        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        position_top = 25
        offset_right = 20
        app_height = 80
        app_width = 400
        position_right = screen_width - app_width - offset_right 
        self.master.geometry("{}x{}+{}+{}".format(app_width, app_height, position_right, position_top))

    def create_buttons(self):
        frame_buttons = tk.Frame(self.master)
        frame_buttons.pack(pady=2)

        button_przyjmij = tk.Button(frame_buttons, text="Przyjmij", font=self.default_font, width=8, height=1, bg='#00b4c9', fg='#FFFFFF')
        button_przyjmij.pack(side='left', padx=20)

        button_wydaj = tk.Button(frame_buttons, text="Wydaj", font=self.default_font, width=8, height=1, bg='#e07ebf', fg='#FFFFFF')
        button_wydaj.pack(side='left', padx=2)


root = tk.Tk()
app = Application(root)
root.mainloop()
