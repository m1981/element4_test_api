import base64
import requests
import time
import tkinter as tk
from operator import itemgetter
from tkinter import messagebox
client_key = "ck_5d652d5fca632c5e60cec2e0b4a9d2f8de2ce8ec"
client_secret = "cs_d3c5698ba2c94885c82f906b3c1c440fc9ae1468"

def get_order():
    base64_encoded_data = base64.b64encode(f"{client_key}:{client_secret}".encode("utf-8")).decode("utf-8")
    response = requests.get(
        "https://fabrykasmakow.com.pl/wp-json/wc/v3/orders",
        headers={"Authorization": f"Basic {base64_encoded_data}"}
    )
    data = response.json()
    on_hold_orders = [order for order in data if order['status'] == "on-hold"]
    sorted_orders = sorted(on_hold_orders, key=itemgetter('date_created'))
    return sorted_orders[0] if sorted_orders else None

def accept_order(order_id):
    change_order_status(order_id, 'completed')

def reject_order(order_id):
    change_order_status(order_id, 'cancelled')

def change_order_status(order_id, status):
    base64_encoded_data = base64.b64encode(f"{client_key}:{client_secret}".encode("utf-8")).decode("utf-8")
    order_update_url = f"https://fabrykasmakow.com.pl/wp-json/wc/v3/orders/{order_id}"
    headers = {"Authorization": f"Basic {base64_encoded_data}"}
    data = {"status": status}
    response = requests.put(order_update_url, headers=headers, json=data)
    response.raise_for_status()

def main_loop():
    root = tk.Tk()

    while True:
        order = get_order()
        if order:
            action = tk.messagebox.askquestion('New Order', f'New order ({order["order_key"]}) available, accept or reject?')
            if action == 'yes':
                accept_order(order['id'])
            else:
                reject_order(order['id'])
        #give server some time before hitting it with requests again
        time.sleep(5)
    #start gui event loop 
    root.mainloop()

if __name__ == "__main__":
    main_loop()
