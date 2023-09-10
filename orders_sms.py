import serial
import threading
import time
import tkinter as tk
from modules.serial_connection import SerialConnection

class Application:
    def __init__(self, master, config):
        self.master = master
        self.config = config
        self.default_font = font = ("Verdana", 10)

        self.init_master()
        self.create_buttons()

        self.scanner_port = self.config['scanner_port']
        self.sms_port = self.config['sms_port']
        self.use_local_file_as_scanner = self.config['use_local_file_as_scanner']
        self.use_console_as_sms = self.config['use_console_as_sms']
        self.connection = SerialConnection()
        self.scanner_thread = threading.Thread(target=self.scan_number, daemon=True)
        self.scanner_thread.start()

    def scan_number(self):
        while True:
            try:
                ser = self.connection.create_serial_connection(self.scanner_port)

                if ser:
                    barcode_data = ser.readline().decode('utf-8').strip()
                    time.sleep(0.2)  # delay for 200 ms
                    if len(barcode_data) > 0:
                        self.update_label(barcode_data)  # update the label with read phone number

            except serial.SerialException as e:
                # handle the error gracefully
                # logging.error(f'Error occurred while connecting to {self.scanner_port}: {str(e)}')
                print(f"Cannot open port {self.scanner_port}. Ensure it's valid and not in use.")
                self.update_label("Scanning...")  # revert to "Scanning..." status in case of exception.
            finally:
                if ser.isOpen():
                    ser.close()


    def update_label(self, phone_number=None):
        if phone_number:
            self.label_actions.config(text=str(phone_number))
        else:
            self.label_actions.config(text="Scanning...")

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

        # added label above the buttons
        self.label_actions = tk.Label(frame_buttons, text="Order Actions", font=self.default_font)
        self.label_actions.pack(pady=5)

        button_przyjmij = tk.Button(frame_buttons, text="Przyjmij", font=self.default_font, width=8, height=1, bg='#00b4c9', fg='#FFFFFF')
        button_przyjmij.pack(side='left', padx=20)

        button_wydaj = tk.Button(frame_buttons, text="Wydaj", font=self.default_font, width=8, height=1, bg='#e07ebf', fg='#FFFFFF')
        button_wydaj.pack(side='left', padx=2)


if __name__ == "__main__":
    root = tk.Tk()

    with open("config_sms.yaml", 'r') as stream:
        try:
            config = yaml.safe_load(stream)
            app = Application(root, config)
        except FileNotFoundError:
            print("The configuration file was not found.")
        except yaml.YAMLError as exc:
            print(f"Error in configuration file: {exc}")

    root.mainloop()

