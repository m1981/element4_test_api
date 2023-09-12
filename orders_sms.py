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
from version import __version__

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
        logger.info("")
        logger.info("----------------------------------------")
        logger.info("----------------------------------------")
        logger.info("----------------------------------------")
        logger.info("App Version: {}".format(__version__))
        logger.info("----------------------------------------")
        logger.info("----------------------------------------")
        logger.info("----------------------------------------")

        self.master = master
        self.config = config
        self.default_font = font = ("Verdana", 10)
        self.buttons_enabled = tk.BooleanVar()
        self.buttons_enabled.set(True)

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
        self._async_disable_buttons()
        ser = None
        while True:
            try:
                logger.debug("scan_number")
                ser = self.connection.create_serial_connection(self.scanner_port)
                if ser:
                    phone_num = ser.readline().decode('utf-8').strip()
                    time.sleep(0.2)  # delay for 200 ms
                    if len(phone_num) > 0:
                        print(len(phone_num))
                        self._async_enable_buttons()
                        self._async_update_label(phone_number=phone_num)
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
        message = "Zamowienie przyjete do realizacji :)"
        self._async_disable_buttons()
        self.send_sms(message)

    def wydaj(self):
        message = "Zamowienie gotowe do odbioru :)"
        self._async_disable_buttons()
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
            value = self.label_actions.cget("text")
            print("send_sms label value: {}".format(value))
            dispatcher.send_sms(value, message)
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
        self.app_height = 40
        self.app_width = 600
        position_right = screen_width - self.app_width - offset_right
        self.master.geometry("{}x{}+{}+{}".format(self.app_width, self.app_height, position_right, position_top))

    def create_buttons(self):

        # added label above the buttons
        self.label_actions = tk.Label(self.master, text="Starting...", font=self.default_font)
        self.label_actions.place(x=200, y=20, anchor='e')

        button_close = tk.Button(self.master, text="x", command=self.close_app, font=self.default_font, width=1, height=1, bg='#ff0000', fg='#FFFFFF')
        button_close.place(anchor='ne', relx=1, rely=0)

        label_version = tk.Label(self.master, text='ver: ' + str(__version__), font=("Verdana", 8))
        label_version.place(x=self.app_width-30, y=20, anchor='e')

        self.button_wydaj = tk.Button(self.master, text="Wydaj", command=self.wydaj, width=8, height=1, bg='#e07ebf', fg='#FFFFFF')
        self.button_wydaj.place(x=self.app_width-240, y=20, anchor='e')

        self.button_przyjmij = tk.Button(self.master, text="Przyjmij", command=self.przyjmij, width=8, height=1, bg='#00b4c9', fg='#FFFFFF')
        self.button_przyjmij.place(x=self.app_width-320, y=20, anchor='e')

    def _async_update_label(self, phone_number=None):
        self.master.after(0, lambda: self.update_label(phone_number))

    def _async_disable_buttons(self):
        if self.buttons_enabled.get():
            self.buttons_enabled.set(False)
            self.master.after(0, self.disable_buttons)

    def _async_enable_buttons(self):
        if not self.buttons_enabled.get():
            self.buttons_enabled.set(True)
            self.master.after(0, self.enable_buttons)

    def enable_buttons(self):
        self.update_buttons(tk.NORMAL)
        self.label_actions.config(text="Enabled")

    def disable_buttons(self):
        self.update_buttons(tk.DISABLED)
        self.label_actions.config(text="Scanning...")

    def update_buttons(self, state):
        self.button_przyjmij.config(state=state)
        self.button_wydaj.config(state=state)

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

