import logging
from logging.handlers import TimedRotatingFileHandler
import os
import serial
import threading
import traceback
import time
import sys
import tkinter as tk
from tkinter import messagebox
import yaml

from modules.serial_connection import SerialConnection
from modules.sms_factory import RealSmsFactory, SimulatedSmsFactory

# Set up logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

log_dir, log_file = 'logs', 'sms.log'  # Place your log files in a logs directory
os.makedirs(log_dir, exist_ok=True)  # Ensure logs directory exists

handler_file = TimedRotatingFileHandler(os.path.join(log_dir, log_file),
                                   when="midnight",
                                   interval=1,
                                   encoding='utf-8')
handler_file.suffix = "%Y%m%d"  # Save logs with date in file name

# Handler for writing logs to the console
handler_console = logging.StreamHandler()
handler_console.setLevel(logging.DEBUG)

# Formatter specifies the layout of logs
handler_file.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
handler_console.setFormatter(logging.Formatter('%(asctime)s - %(message)s'))

# Add both handlers to the logger
logger.addHandler(handler_file)
logger.addHandler(handler_console)


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

        if self.use_console_as_sms:
            self.sms_factory = SimulatedSmsFactory
        else:
            self.sms_factory = RealSmsFactory

        self.scanner_thread = threading.Thread(target=self.scan_number, daemon=True)
        self.scanner_thread.start()

    def scan_number(self):
        ser = None
        while True:
            try:
                logger.debug("scan_number")
                if self.use_local_file_as_scanner:
                    time.sleep(0.5)
                    with open('sms.txt', 'r') as file:
                        phone_number = file.read()
                        self.update_label(phone_number)
                else:
                    ser = self.connection.create_serial_connection(self.scanner_port)
                    if ser:
                        barcode_data = ser.readline().decode('utf-8').strip()
                        time.sleep(0.2)  # delay for 200 ms
                        if len(barcode_data) > 0:
                            self.update_label(barcode_data)  # update the label with read phone number
            except serial.SerialException as e:
                error_message = f"Cannot open port {self.scanner_port}. Ensure it's valid and not in use."
                self.handle_exception(e, error_message)
            except FileNotFoundError as e:
                error_message = f"Cannot find the file 'sms.txt'. Ensure it's in the correct path."
                self.handle_exception(e, error_message)
            except PermissionError as e:
                error_message = "No permission to read the file 'sms.txt'."
                self.handle_exception(e, error_message)
            except Exception as e:
                error_message = "Unknown error"
                self.handle_exception(e)
            finally:
                if ser and ser.isOpen():
                    ser.close()

    def przyjmij(self):
        # Here you can add more logic specific to the "przyjmij" action
        message = "Zamówienie przyjęte do realizacji!"
        self.send_sms(message)

    def wydaj(self):
        # Here you can add more logic specific to the "wydaj" action
        message = "Zamówienie gotowe do odbioru!"
        self.send_sms(message)


    def update_label(self, phone_number=None):
        if phone_number:
            self.label_actions.config(text=str(phone_number))
        else:
            self.label_actions.config(text="Scanning...")

    def send_sms(self, message):
        try:
            connection = self.sms_factory.get_connection(self.sms_port)
            composer = self.sms_factory.get_composer(connection)
            dispatcher = self.sms_factory.get_dispatcher(composer)
            dispatcher.send_sms(self.label_actions.cget("text"), message)
        except Exception as e:
            self.handle_exception(e, "Error occurred while sending SMS.")

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
        self.label_actions = tk.Label(frame_buttons, text="Starting...", font=self.default_font)
        self.label_actions.pack(pady=5)

        button_close = tk.Button(self.master, text="x", command=self.close_app, font=self.default_font, width=1, height=1, bg='#ff0000', fg='#FFFFFF')
        button_close.place(anchor='ne', relx=1, rely=0)

        button_przyjmij = tk.Button(frame_buttons, text="Przyjmij", command=self.przyjmij, font=self.default_font, width=8, height=1, bg='#00b4c9', fg='#FFFFFF')
        button_przyjmij.pack(side='left', padx=20)

        button_wydaj = tk.Button(frame_buttons, text="Wydaj", command=self.wydaj, font=self.default_font, width=8, height=1, bg='#e07ebf', fg='#FFFFFF')
        button_wydaj.pack(side='left', padx=2)

    def handle_exception(self, e, error_message="An unexpected error occurred"):
        logger.exception(f"{error_message}: {str(e)}")
        exception_message = str(e) + "\n\nTraceback:\n" + traceback.format_exc()
        messagebox.showerror("Error", exception_message)
        self.master.quit()

    def close_app(self):
         self.master.quit()

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

