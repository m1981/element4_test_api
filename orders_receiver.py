import os
import json
import base64
import requests
import time
import tkinter as tk
from tkinter import ttk
from operator import itemgetter
import threading
import winsound
from receipt import Order, ReceiptItem, Printer, elzabdr
import argparse
import logging

import glob
import os
import logging
from logging.handlers import TimedRotatingFileHandler

from receipt import Order, ReceiptItem, Printer, elzabdr
# setup printer
printer = Printer(elzabdr, port=1, speed=9600, timeout=5)

# Set up logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

log_dir, log_file = 'logs', 'orders.log'  # Place your log files in a logs directory
os.makedirs(log_dir, exist_ok=True)  # Ensure logs directory exists

handler = TimedRotatingFileHandler(os.path.join(log_dir, log_file),
                                   when="midnight",
                                   interval=1,
                                   encoding='utf-8')
handler.suffix = "%Y%m%d"  # Save logs with date in file name

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

logger.addHandler(handler)


class OrderManager:
    def __init__(self, use_local_files=False, local_files_path='./'):
        self.use_local_files = use_local_files
        self.local_files_path = local_files_path
        self.printer = Printer(elzabdr, port=1, speed=9600, timeout=5)
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

        self.root = tk.Tk()
        self.root.bind('<FocusIn>', self.onFocusIn)
        self.root.bind('<FocusOut>', self.onFocusOut)
        self.sound_playing = threading.Event()  # Indicator for whether sound is playing
        self.window_in_focus = tk.BooleanVar()  # Indicator for whether window is in focus

        self.button_accept = tk.Button(self.root, text="Accept Order", command=lambda: self.accept_order(self.order_id))
        self.button_accept.pack()

        self.button_reject = tk.Button(self.root, text="Reject Order", command=lambda: self.reject_order(self.order_id))
        self.button_reject.pack()

        self.label_order = tk.Label(self.root, text="")
        self.label_order.pack()

        self.label_nip = tk.Label(self.root, text="")
        self.label_nip.pack()

        self.label_phone = tk.Label(self.root, text="")
        self.label_phone.pack()

        self.label_na_miejscu_na_wynos = tk.Label(self.root, text="")
        self.label_na_miejscu_na_wynos.pack()

        self.label_comments = tk.Label(self.root, text="")
        self.label_comments.pack()

        self.label_no_orders = tk.Label(self.root, text="", font = ("Helvetica", 18), fg = "red")
        self.label_no_orders.pack()

        self.treeview = ttk.Treeview(self.root)
        self.treeview.pack()
        self.treeview["columns"]=("1","2","3")
        self.treeview['show'] = 'headings'
        self.treeview.column("1", width=150 )
        self.treeview.column("2", width=100)
        self.treeview.column("3", width=150)
        self.treeview.heading("1", text="Item")
        self.treeview.heading("2", text="Quantity")
        self.treeview.heading("3", text="Price Including Tax")

        self.root.after(5000, self.update_order)


    def parse_args(self):
        self.parser = argparse.ArgumentParser(description="Process some integers.")
        self.parser.add_argument("--status", type=str, required=True, help="Order status")
        self.args = self.parser.parse_args()
        self.process_status = self.args.status

    def run(self):
        self.root.mainloop()

    def play_sound(self):
        if not self.window_in_focus.get():  # Check if window is not in focus
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

    def get_orders(self):
        orders = []
        try:
            if self.use_local_files:
                orders = self.get_local_orders(self.local_files_path)
            else:
                base64_encoded_data = base64.b64encode(f"{self.client_key}:{self.client_secret}".encode("windows-1250")).decode("windows-1250")
                response = requests.get(
                    f"{self.rest_api_url}/orders",
                    headers={"Authorization": f"Basic {base64_encoded_data}"}
                )
                response.raise_for_status() # Raise exception if status code indicates an HTTP error
                orders = response.json()

        except requests.RequestException as re:
            logger.error(f"Error connecting with API: {str(re)}")

        except json.decoder.JSONDecodeError as json_err:
            logger.error(f"JSON decoding error while fetching orders: {str(json_err)}")

        except IOError as ioerr:
            logger.error(f"File operation error while fetching orders: {str(ioerr)}")

        except Exception as ex:
            logger.error(f"An unexpected error occurred while fetching orders: {str(ex)}")

        finally:
            logger.info(f"Fetched orders data: {orders}")
            return orders

    def change_order_status(self, order_id, new_status):
        try:
            if self.use_local_files:
                data = self.get_order_by_id(order_id)
                logger.info(f"Order data: {data}")  # Log the order data
                data['status'] = new_status
                with open(os.path.join(self.local_files_path, f'order_{order_id}.json'), 'w') as f:
                    f.write(json.dumps(data))

            else:
                base64_encoded_data =  base64.b64encode(f"{self.client_key}:{self.client_secret}".encode("windows-1250")).decode("windows-1250")
                data = {"status": new_status}
                r = requests.put(
                    f"{self.rest_api_url}/orders/{order_id}",
                    headers={"Authorization": f"Basic {base64_encoded_data}"},
                    json=data
                )
                r.raise_for_status()
                logger.info(f"Response: {r.json()}")  # Log the response from the server

        except requests.RequestException as re:
            logger.error(f"Error connecting with API: {re}")
            return None

        except PermissionError:
            logger.error(f"Permission denied: Unable to write to {os.path.join(self.local_files_path, f'order_{order_id}.json')}")
            return None

        except IOError as e:
            logger.error(f"File error occurred: {e}")
            return None

        except KeyError as e:
            logger.error(f"Order data is missing key: {e}")
            return None

        except Exception as e:
            logger.error(f"An unexpected error occurred: {str(e)}")
            return None



    def get_order_by_id(self, order_id):
        if self.use_local_files:
            with open(os.path.join(self.local_files_path, f'order_{order_id}.json')) as f:
                return json.load(f)
        else:
            base64_encoded_data =  base64.b64encode(f"{self.client_key}:{self.client_secret}".encode("windows-1250")).decode("windows-1250")
            response = requests.get(
                f"{self.rest_api_url}/orders/{order_id}",
                headers={"Authorization": f"Basic {base64_encoded_data}"}
            )
            return response.json()

    def reset_orders(self):
        '''Reset the status field of all orders to 'processing' in local JSON files.'''
        if self.use_local_files:
            for filename in os.listdir(self.local_files_path):
                if filename.endswith(".json"):
                    with open(os.path.join(self.local_files_path, filename)) as f:
                        data = json.load(f)
                        data['status'] = 'processing'
                    with open(os.path.join(self.local_files_path, filename), 'w') as f:
                        f.write(json.dumps(data))


    def get_local_orders(self, path):
        orders = []
        for filename in os.listdir(path):
            if filename.endswith(".json"):
                with open(os.path.join(path, filename)) as f:
                    orders.append(json.load(f))
        return orders

    def is_processing(self, order):
        assert self.process_status
        return order["status"] == self.process_status

    def order_processing_effects(self, order):
        self.show_order(order)
        self.play_sound()
        self.update_buttons(state=tk.NORMAL)

    def order_not_processing_effects(self):
        self.show_no_order()
        self.update_buttons(state=tk.DISABLED)

    def update_order(self):
        try:
            orders = self.get_orders()
            for order in orders:
                logger.info(f"Single Order data: {order}")
                if self.is_processing(order):
                    self.order_id = order["id"]
                    self.order_processing_effects(order)
                    break
            else:
                self.order_not_processing_effects()
        except Exception as e:
            logger.error(f"An error occurred in the order update process: {str(e)}")
        finally:
            self.root.after(5000, self.update_order)  # Sleep for 5 seconds before checking new orders

    def show_order(self, order):
        self.populate_ui(order)

    def show_no_order(self):
        # Cleanup UI
        self.cleanup_ui()

        # Display message
        self.label_no_orders.config(text="No orders currently.")
        self.update_buttons(tk.DISABLED)

    def update_buttons(self, state):
        self.button_accept.config(state=state)
        self.button_reject.config(state=state)

    def update_ui_after_order_process(self, text):
        self.cleanup_ui()
        self.label_no_orders.config(text = text)

    def accept_order(self, order_id):
        self.print_receipt(self.get_order_by_id(order_id))
        self.change_order_status(order_id, 'completed')
        self.update_buttons(tk.DISABLED)
        print(f"Accepted order {order_id}.")
        self.update_ui_after_order_process("No orders currently")

    def reject_order(self, order_id):  # TODO: Adjust the order status depending on your requirements.
        self.change_order_status(order_id, 'cancelled')
        self.update_buttons(tk.DISABLED)
        print(f"Rejected order {order_id}.")
        self.update_ui_after_order_process("No orders currently")


    def print_receipt(self, order):
        receipt_order = Order()
        vat_id = 2
        receipt_order.NIP = order['billing']['nip_do_paragonu']
        receipt_order.order_id = order['id']
        receipt_order.phone_number = order['billing']['phone']
        receipt_order.na_miejscu_na_wynos = order['billing']['na_miejscu_na_wynos']
        receipt_order.comments = order['dodatki_do_pizzy']['notatki']
        for item in order['line_items']:
            total_price = float(item['total']) + float(item['total_tax'])
            receipt_order.add_item(ReceiptItem(item['name'], item['quantity']*100, vat_id, int((float(item['total']) + float(item['total_tax']))*100), 'szt.'))
        printer.print_receipt(receipt_order)
        printer.print_internal_order(receipt_order)

    def populate_ui(self, order):
        self.root.attributes('-topmost', True)
        self.label_no_orders.config(text="")
        self.order_id = order['id']
        self.label_order.config(text = f"Zamowienie: {self.order_id}")
        self.label_nip.config(text = f"NIP: {order['billing']['nip_do_paragonu']}")
        self.label_phone.config(text = f"Telefon: {order['billing']['phone']}")
        self.label_na_miejscu_na_wynos.config(text = f"{order['billing']['na_miejscu_na_wynos']}")
        self.label_comments.config(text = f"Komentarz: {order['dodatki_do_pizzy']['notatki']}")
        self.treeview.delete(*self.treeview.get_children())
        for item in order['line_items']:
            self.treeview.insert("", 'end', values=(item['name'], item['quantity'], item['total']))


    def cleanup_ui(self):
        # Clear all Labels
        self.label_no_orders.config(text="")
        self.label_order.config(text="")
        self.label_nip.config(text="")
        self.label_phone.config(text="")
        self.label_na_miejscu_na_wynos.config(text="")
        self.label_comments.config(text="")
        # Clear Treeview
        self.treeview.delete(*self.treeview.get_children())


if __name__=="__main__":
  manager = OrderManager()
  manager.parse_args()
  manager.run()
