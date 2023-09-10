import tkinter as tk

class Application:
    def __init__(self, master):
        self.master = master
        self.master.geometry("300x50")
        self.master.title("SMS order")
        self.master.overrideredirect(True)
        self.master.attributes('-topmost', True) # This line ensures the application window is always on top.
        self.default_font = font = ("Verdana", 12)

        # Position the application at the top-right corner with offset.
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        position_top = 25
        position_right = screen_width - 300 - 20  # window-width minus-app-width minus desired-offset
        self.master.geometry("+{}+{}".format(position_right, position_top))

        # Create a frame for the buttons.
        frame_buttons = tk.Frame(master)
        frame_buttons.pack(pady=10)

        button_przyjmij = tk.Button(frame_buttons, text="Przyjmij", font=self.default_font, width=10, height=2, bg='#36b37e', fg='#FFFFFF')
        button_przyjmij.pack(side='left', padx=2)

        button_wydaj = tk.Button(frame_buttons, text="Wydaj", font=self.default_font, width=10, height=2, bg='#cc3931', fg='#FFFFFF')
        button_wydaj.pack(side='left', padx=2)

root = tk.Tk()
app = Application(root)
root.mainloop()
