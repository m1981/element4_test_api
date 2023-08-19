import base64
import requests
import time
import tkinter as tk
from tkinter import ttk
from operator import itemgetter
import threading
import winsound

client_key = "ck_5d652d5fca632c5e60cec2e0b4a9d2f8de2ce8ec"
client_secret = "cs_d3c5698ba2c94885c82f906b3c1c440fc9ae1468"

def play_sound():
    winsound.PlaySound('C:/Windows/Media/tada.wav', winsound.SND_ASYNC | winsound.SND_LOOP)

def stop_sound():
    winsound.PlaySound(None, winsound.SND_ASYNC)

def onFocusIn(event):
    stop_sound()

root = tk.Tk()
root.bind('<FocusIn>', onFocusIn)

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


label_order = tk.Label(root, text="")
label_order.pack()

label_nip = tk.Label(root, text="")
label_nip.pack()

label_phone = tk.Label(root, text="")
label_phone.pack()

label_na_miejscu_na_wynos = tk.Label(root, text="")
label_na_miejscu_na_wynos.pack()

label_comments = tk.Label(root, text="")
label_comments.pack()

label_no_orders = tk.Label(root, text="", font = ("Helvetica", 18), fg = "red")
label_no_orders.pack()

treeview = ttk.Treeview(root)
treeview.pack()
treeview["columns"]=("1","2","3")
treeview['show'] = 'headings'
treeview.column("1", width=150 )
treeview.column("2", width=100)
treeview.column("3", width=150)
treeview.heading("1", text="Item")
treeview.heading("2", text="Quantity")
treeview.heading("3", text="Price Including Tax")

button_accept = tk.Button(root, text="Accept Order", command=lambda: accept_order(order_id))
button_accept.pack()

button_reject = tk.Button(root, text="Reject Order", command=lambda: reject_order(order_id))
button_reject.pack()

def update_order():
    global order_id
    order = get_order()
    if order:
        if root.state() == 'iconic':
            threading.Thread(target=play_sound).start()
        root.attributes('-topmost', True)
        label_no_orders.config(text = "")  # Clearing "No orders" text
        order_id = order['id']
        label_order.config(text = f"Zamowienie: {order_id}")
        label_nip.config(text = f"NIP: {order['billing']['nip_do_paragonu']}")
        label_phone.config(text = f"Telefon: {order['billing']['phone']}")
        label_na_miejscu_na_wynos.config(text = f"{order['billing']['na_miejscu_na_wynos']}")
        label_comments.config(text = f"Komentarz: {order['dodatki_do_pizzy']['notatki']}")
        treeview.delete(*treeview.get_children())
        for item in order['line_items']:
            total_price = float(item['total']) + float(item['total_tax'])
            treeview.insert("", 'end', values=(item['name'], item['quantity'], total_price))
    else:
        root.attributes('-topmost', False)
        label_order.config(text = "")
        label_nip.config(text = "")
        label_phone.config(text = "")
        label_na_miejscu_na_wynos.config(text = "")
        label_comments.config(text = "")
        treeview.delete(*treeview.get_children())
        label_no_orders.config(text = "No orders currently")
    root.after(5000, update_order)

if __name__ == "__main__":
    root.after(5000, update_order)
    root.mainloop()
