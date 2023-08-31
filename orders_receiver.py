# -*- coding: utf-8 -*-

import winsound
import collections.abc
import requests
import os
import sys
import json
import base64
import bleach
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import traceback
import threading
import argparse
import logging
import yaml
from datetime import datetime, timedelta
from logging.handlers import TimedRotatingFileHandler
from receipt import Order, ReceiptItem, Printer, elzabdr


# Set up logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

log_dir, log_file = 'logs', 'orders.log'  # Place your log files in a logs directory
os.makedirs(log_dir, exist_ok=True)  # Ensure logs directory exists

handler_file = TimedRotatingFileHandler(os.path.join(log_dir, log_file),
                                   when="midnight",
                                   interval=1,
                                   encoding='utf-8')
handler_file.suffix = "%Y%m%d"  # Save logs with date in file name

# Handler for writing logs to the console
handler_console = logging.StreamHandler()
handler_console.setLevel(logging.ERROR)

# Formatter specifies the layout of logs
handler_file.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
handler_console.setFormatter(logging.Formatter('%(asctime)s - %(message)s'))

# Add both handlers to the logger
logger.addHandler(handler_file)
logger.addHandler(handler_console)

class OrderManager:
    def __init__(self):
        with open('config.yaml', 'r') as stream:
            config = yaml.safe_load(stream)

        self.local_files_path = config['local_files_path']
        self.use_local_files = config['use_local_files']
        self.use_local_printer = config['use_local_printer']
        self.printer = Printer(elzabdr, config['printer']['port'], config['printer']['speed'], config['printer'][
        'timeout'], self.use_local_printer)
        self.proxies = None
        if config['use_proxy']:
            self.proxies = config['proxy']

        self.order_exists = False
        self.order_id = None
        self.client_key = "ck_5d652d5fca632c5e60cec2e0b4a9d2f8de2ce8ec"
        self.client_secret = "cs_d3c5698ba2c94885c82f906b3c1c440fc9ae1468"
        self.rest_api_url = "https://fabrykasmakow.com.pl/wp-json/wc/v3"
        self.treeview = None
        self.label_order = None
        self.label_no_orders = None
        self.label_phone = None
        self.label_nip = None
        self.label_comments = None
        self.label_na_miejscu_na_wynos = None
        self.process_status = None
        self.has_orders = False
        self._update_id = None
        self.root = tk.Tk()

        self.wait_for_orders_msg = "Czekam na zamówienia..."
        # Set the initial size of the window
        width = 800  # Desired width
        height = 700  # Desired height

        # Get screen width and height
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Calculate the correct position to center the window
        position_top = int(screen_height / 2 - height / 2)
        position_right = int(screen_width / 2 - width / 2)

        self.root.geometry(f'{width}x{height}+{position_right}+{position_top}')

        self.root.bind('<FocusIn>', self.onFocusIn)
        self.root.bind('<FocusOut>', self.onFocusOut)
        self.sound_playing = threading.Event()  # Indicator for whether sound is playing
        self.window_in_focus = tk.BooleanVar()  # Indicator for whether window is in focus

        self.label_font = font = ("Verdana", 12)
        self.default_font = font = ("Verdana", 14)
        # Create a frame for the labels.
        frame_labels = tk.Frame(self.root)
        frame_labels.pack(fill='x')

        order_label = tk.Label(frame_labels, text="Zamowienie:", font = self.label_font, anchor='e')
        order_label.grid(row=0, column=0, sticky='e')
        self.label_order = tk.Label(frame_labels, text="", font = self.default_font, anchor='w')
        self.label_order.grid(row=0, column=1, sticky='w')

        date_label = tk.Label(frame_labels, text="Data:", font = self.label_font, anchor='e')
        date_label.grid(row=0, column=2, sticky='e')
        self.label_date = tk.Label(frame_labels, text="", font = self.default_font, anchor='w')
        self.label_date.grid(row=0, column=3, sticky='w')

        self.local_orders_label = tk.Label(frame_labels, text="", fg='red', font=self.label_font, anchor='e')
        self.local_orders_label.grid(row=1, column=3, sticky='e')

        self.console_printer_label = tk.Label(frame_labels, text="", fg='red', font=self.label_font, anchor='e')
        self.console_printer_label.grid(row=2, column=3, sticky='e')


        nip_label = tk.Label(frame_labels, text="NIP:", font = self.label_font, anchor='e')
        nip_label.grid(row=1, column=0, sticky='e')
        self.label_nip = tk.Label(frame_labels, text="", font = self.default_font, anchor='w')
        self.label_nip.grid(row=1, column=1, sticky='w')

        phone_label = tk.Label(frame_labels, text="Tel:", font = self.label_font, anchor='e')
        phone_label.grid(row=2, column=0, sticky='e')
        self.label_phone = tk.Label(frame_labels, text="", font = self.default_font, anchor='w')
        self.label_phone.grid(row=2, column=1, sticky='w')

        nmnw_label = tk.Label(frame_labels, text="Gdzie:", font = self.label_font, anchor='e')
        nmnw_label.grid(row=3, column=0, sticky='e', pady=(50, 0))
        self.label_na_miejscu_na_wynos = tk.Label(frame_labels, text="", font = self.default_font, anchor='w')
        self.label_na_miejscu_na_wynos.grid(row=3, column=1, sticky='w', pady=(50, 0))

        comments_label = tk.Label(frame_labels, text="Komentarz:", font = self.label_font, anchor='e')
        comments_label.grid(row=4, column=0, sticky='e')
        self.label_comments = tk.Text(frame_labels, height=4, width=20, wrap='word', font=self.default_font)
        self.label_comments.grid(row=4, column=1, sticky='w')
        self.label_comments.insert(1.0, "")  # add some text
        self.label_comments.configure(state="disable")  # make it read-only


        self.label_no_orders = tk.Label(self.root, text=self.wait_for_orders_msg, font = ("Verdana", 18), fg = "green")
        self.label_no_orders.pack()

        # Create a frame for the buttons.
        frame_buttons = tk.Frame(self.root)
        frame_buttons.pack(pady=10)

        self.button_accept = tk.Button(frame_buttons, text="Akceptuj", font = self.default_font, width = 10, height = 2,
                                       command=lambda: self.accept_order(self.order_id),  fg='#FFFFFF', bg='#36b37e')
        self.button_accept.pack(side='left', padx=5)

        self.button_reject = tk.Button(frame_buttons, text="Odrzuć", font = self.default_font, width = 10, height = 2,
                                       command=lambda: self.reject_order(self.order_id),  fg='#FFFFFF', bg='#cc3931')
        self.button_reject.pack(side='left', padx=5)

        # Create a frame for the Treeview.
        frame_treeview = tk.Frame(self.root)
        frame_treeview.pack(fill='both', expand=True)

        style = ttk.Style()
        style.configure("mystyle.Treeview", highlightthickness=0, bd=0, font=('Verdana', 14)) # Modify the font of the body
        style.configure("mystyle.Treeview.Heading", font=('Verdana', 14,'bold')) # Modify the font of the headings
        style.layout("mystyle.Treeview", [('mystyle.Treeview.treearea', {'sticky': 'nswe'})]) # Remove the borders

        self.treeview = ttk.Treeview(frame_treeview, style="mystyle.Treeview")


        self.treeview.pack(fill='both', expand=True)
        self.treeview["columns"]=("1","2","3")
        self.treeview['show'] = 'headings'
        self.treeview.column("1", width=350)
        self.treeview.column("2", width=50)
        self.treeview.column("3", width=100)
        self.treeview.heading("1", text="Danie", anchor="w")
        self.treeview.heading("2", text="Ilość", anchor="w")
        self.treeview.heading("3", text="Cena", anchor="w")

        self.update_buttons(state=tk.DISABLED)
        self.root.after(5000, self.update_order)



    def parse_args(self):
        self.parser = argparse.ArgumentParser(description="Process some integers.")
        self.parser.add_argument("--status", type=str, required=True, help="Order status")
        self.args = self.parser.parse_args()
        self.process_status = self.args.status

    def run(self):
        self.root.mainloop()


    def convert_date(self, order_date):
        today = datetime.now()
        if order_date.date() == today.date():
            relative_date = "(dzisiaj)"
        elif order_date.date() == today.date() - timedelta(days=1):
            relative_date = "(wczoraj)"
        else:
            diff = today.date() - order_date.date()
            relative_date = f"({diff.days} dni temu)"

        formatted_date = order_date.strftime("%d.%m  godzina: %H:%M")
        return f"{relative_date} {formatted_date}"


    def play_sound(self):
        if self.root.state() == 'iconic':  # Check if window is minimized
            winsound.PlaySound('C:/Windows/Media/tada.wav', winsound.SND_ASYNC | winsound.SND_LOOP)
            self.sound_playing.set()  # Indicate that sound is playing

    def stop_sound(self):
        if self.sound_playing.is_set():  # Check if sound is playing
            winsound.PlaySound(None, winsound.SND_ASYNC)
            self.sound_playing.clear()  # Indicate that sound is not playing anymore

    def onFocusIn(self, event):
        self.window_in_focus.set(True)  # Indicate that window is now in focus
        self.stop_sound()  # Stop sound if it's playing

    def onFocusOut(self, event):
        self.window_in_focus.set(False)  # Indicate that window lost focus
        if self.has_orders:
            self.play_sound()

    def get_orders(self):
        orders = []
        try:
            if self.use_local_files:
                orders = self.get_local_orders(self.local_files_path)
            else:
                base64_encoded_data = base64.b64encode(f"{self.client_key}:{self.client_secret}".encode("windows-1250")).decode("windows-1250")
                response = requests.get(
                    f"{self.rest_api_url}/orders",
                    headers={"Authorization": f"Basic {base64_encoded_data}"},
                    proxies=self.proxies,
                )
                response.encoding = 'utf-8'
                response.raise_for_status() # Raise exception if status code indicates an HTTP error
                orders = [self.clean_recursive(order) for order in response.json()]

        except Exception as e:
            self.handle_exception(e)

        orders.reverse()
        for order in orders:
            logger.info(f"Fetched: id: {order['id']}, status: {order['status']}")
        return orders

    def change_order_status(self, order_id, new_status):
        old_status = self.get_order_by_id(order_id)['status']
        if self.use_local_files:
            os.remove(os.path.join(self.local_files_path, f'order_{order_id}.json'))
        else:
            base64_encoded_data =  base64.b64encode(f"{self.client_key}:{self.client_secret}".encode("windows-1250")).decode("windows-1250")
            data = {"status": new_status}
            r = requests.put(
                f"{self.rest_api_url}/orders/{order_id}",
                headers={"Authorization": f"Basic {base64_encoded_data}"},
                json=data,
                proxies=self.proxies,
            )
            r.raise_for_status()
            logger.info(f"Order status changed. Order ID: {order_id}, Old Status: {old_status}, New Status: {new_status}")

    def get_order_by_id(self, order_id):
        if self.use_local_files:
            with open(os.path.join(self.local_files_path, f'order_{order_id}.json'), encoding='utf-8') as f:
                return json.load(f)
        else:
            base64_encoded_data =  base64.b64encode(f"{self.client_key}:{self.client_secret}".encode("windows-1250")).decode("windows-1250")
            response = requests.get(
                f"{self.rest_api_url}/orders/{order_id}",
                headers={"Authorization": f"Basic {base64_encoded_data}"},
                proxies=self.proxies,
            )
            return response.json()

    def get_local_orders(self, path):
        orders = []
        files = os.listdir(path)
        files.sort(reverse=True)  # This will sort the files in descending order
        for filename in files:
            if filename.endswith(".json"):
                with open(os.path.join(path, filename), encoding='utf-8') as f:
                    orders.append(json.load(f))
        return orders

    def is_processing(self, order):
      return order["status"] == self.process_status

    def order_processing_effects(self, order):
        self.show_order(order)
        if self.root.state() == 'iconic':
            self.root.deiconify()
        self.stop_sound()
        self.update_buttons(state=tk.NORMAL)

    def order_not_processing_effects(self):
        self.show_no_order()
        self.stop_sound()
        self.update_buttons(state=tk.DISABLED)
        self.root.attributes('-topmost', 0) # removes topmost state

    def force_deiconify_and_bring_to_front(self):
        if self.root.state() == 'iconic':  # Check if the window is minimized
            self.root.deiconify()  # If so, restore it
        self.root.attributes('-topmost', True)  # brings the window to top

    def update_order(self):
        logger.info("update_order")
        try:
            logger.info("before get_orders")
            orders = self.get_orders()
            logger.info("before process_orders")
            self.process_orders(orders)
            logger.info("before self.root.after")
            self.root.after(5000, self.update_order)  # Sleep for 5 seconds before checking new orders
        except Exception as e:
            self.handle_exception(e)
        logger.info("end of update_order")


    def process_orders(self, orders):
        logger.info(f"Number of orders to process: {len(orders)}")
        has_orders_now = False
        for order in orders:
            logger.info(f"Processing order with ID {order['id']} and status {order['status']}")
            if self.is_processing(order):  # An order is in processing state
                self.order_id = order["id"]
                logger.info(f"Processing: id: {order['id']}, status: {order['status']}")
                has_orders_now = True
                break

        logger.info("after for loop")
        if not self.has_orders:
            self.cleanup_ui()

        if not self.has_orders and has_orders_now:
            self.order_processing_effects(order)
        elif self.has_orders and not has_orders_now and orders:
            self.order_id = orders[0]['id']
            self.order_processing_effects(order)
        elif self.has_orders and not has_orders_now:
            self.order_not_processing_effects()
        else:
            logger.info("else in process_orders")

        self.has_orders = has_orders_now


    def show_order(self, order):
        logger.info(f"show_order {order['id']}")
        self.force_deiconify_and_bring_to_front()
        self.populate_ui(order)

    def show_no_order(self):
        logger.info("show_no_order")
        self.cleanup_ui()


    def update_buttons(self, state):
        self.button_accept.config(state=state)
        self.button_reject.config(state=state)

    def accept_order(self, order_id):
        try:
            logger.info(f"Accepting order: {order_id}")
            self.update_buttons(state=tk.DISABLED)
            self.print_receipt(self.get_order_by_id(order_id))
            self.change_order_status(order_id, 'completed')
            self.stop_sound()
            self.has_orders = False # Set the flag to False before updating the order
            self.update_order() # Manually update orders immediately after accepting an order
            if self._update_id is not None:
                self.root.after_cancel(self._update_id)
            self._update_id = self.root.after(5000, self.update_order)
            logger.info(f"Accepted order {order_id}.")
        except Exception as e:
            self.handle_exception(e)

    def reject_order(self, order_id):
        try:
            logger.info(f"Rejecting order: {order_id}")
            self.update_buttons(state=tk.DISABLED)
            self.change_order_status(order_id, 'cancelled')
            self.stop_sound()
            self.has_orders = False # Set the flag to False before updating the order
            self.update_order()  # Manually update orders immediately after rejecting an order
            if self._update_id is not None:
                self.root.after_cancel(self._update_id)
            self._update_id = self.root.after(5000, self.update_order)
            logger.info(f"Rejected order {order_id}.")
        except Exception as e:
            self.handle_exception(e)



    def print_receipt(self, order):
        receipt_order = Order()
        vat_id = 2
        receipt_order.NIP = order['billing']['nip_do_paragonu']
        receipt_order.order_id = order['id']
        receipt_order.date_created = datetime.strptime(order['date_created'], "%Y-%m-%dT%H:%M:%S")
        receipt_order.phone_number = order['billing']['phone']
        receipt_order.na_miejscu_na_wynos = order['billing']['na_miejscu_na_wynos']
        receipt_order.comments = order['dodatki_do_pizzy']['notatki']
        for item in order['line_items']:
            total_price = float(item['total']) + float(item['total_tax'])
            receipt_order.add_item(ReceiptItem(item['name'], item['quantity']*100, vat_id, int((float(item['total']) + float(item['total_tax']))*100), 'szt.'))
        self.printer.print_receipt(receipt_order)
        self.printer.print_internal_order(receipt_order)

    def populate_ui(self, order):
        logger.info("populate_ui")
        try:
            self.order_id = order['id']
            self.label_order.config(text = f"{self.order_id}")
            self.label_date.config(text = self.convert_date(datetime.strptime(order['date_created'][:-1], "%Y-%m-%dT%H:%M:%S")))
            self.label_nip.config(text = f"{order['billing']['nip_do_paragonu']}")
            self.label_phone.config(text = f"{order['billing']['phone']}")
            self.label_na_miejscu_na_wynos.config(text = f"{order['billing']['na_miejscu_na_wynos']}")
            comments = order['dodatki_do_pizzy']['notatki']

            comments = order['dodatki_do_pizzy']['notatki']
            self.label_comments.configure(state="normal")  # make it editable
            self.label_comments.delete("1.0", "end")  # delete the existing text
            self.label_comments.insert("1.0", comments)  # insert the new text
            self.label_comments.configure(state="disable")  # make it read-only again
            self.label_no_orders.config(text="")
            # Clear Treeview
            self.treeview.delete(*self.treeview.get_children())
            if self.local_files_path:
                self.local_orders_label.config(text="Testing: Local orders")
            else:
                self.local_orders_label.config(text="")

            if self.use_local_printer:
                self.console_printer_label.config(text="Testing: Console printer")
            else:
                self.console_printer_label.config(text="")

            for item in order['line_items']:
                price = float(item['total']) + float(item['total_tax'])
                formatted_price = '{:.2f} PLN'.format(price)
                self.treeview.insert("", 'end', values=(item['name'], item['quantity'], formatted_price))
        except Exception as e:
            self.handle_exception(e)


    def cleanup_ui(self):
        logger.info("cleanup_ui")
        self.label_no_orders.config(text="")
        self.label_order.config(text="")
        self.label_date.config(text = "")
        self.label_nip.config(text="")
        self.label_phone.config(text="")
        self.label_na_miejscu_na_wynos.config(text="")
        self.label_comments.configure(state="normal")
        self.label_comments.delete("1.0", "end")
        self.label_no_orders.config(text=self.wait_for_orders_msg)
        # Clear Treeview
        self.treeview.delete(*self.treeview.get_children())


    def handle_exception(self, e, error_message="An unexpected error occurred"):
        logger.exception(f"{error_message}: {str(e)}")
        exception_message = str(e) + "\n\nTraceback:\n" + traceback.format_exc()
        messagebox.showerror("Error", exception_message)
        sys.exit(1)


    def clean_recursive(self, d):
        result = {}
        for key, value in d.items():
            if isinstance(value, collections.abc.Mapping):
                result[bleach.clean(key)] = self.clean_recursive(value)
            elif isinstance(value, str):
                result[bleach.clean(key)] = bleach.clean(value)
            else:
                result[bleach.clean(key)] = value
        return result

if __name__=="__main__":
  manager = OrderManager()
  manager.parse_args()
  manager.run()
