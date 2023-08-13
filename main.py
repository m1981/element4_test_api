from flask import Flask, render_template
import requests
import base64
import itertools

app = Flask(__name__)

client_key = "ck_5d652d5fca632c5e60cec2e0b4a9d2f8de2ce8ec"
client_secret = "cs_d3c5698ba2c94885c82f906b3c1c440fc9ae1468"


@app.route('/accept_order/<int:order_id>', methods=['POST'])
def accept_order(order_id):
    change_order_status(order_id, 'completed')
    return "Order status updated successfully to 'completed'", 200

@app.route('/reject_order/<int:order_id>', methods=['POST'])
def reject_order(order_id):
    change_order_status(order_id, 'cancelled')
    return "Order status updated successfully to 'cancelled'", 200

def change_order_status(order_id, status):
    base64_encoded_data = base64.b64encode(f"{client_key}:{client_secret}".encode("utf-8")).decode("utf-8")
    order_update_url = f"https://fabrykasmakow.com.pl/wp-json/wc/v3/orders/{order_id}"
    headers = {"Authorization": f"Basic {base64_encoded_data}"}
    data = {"status": status}
    response = requests.put(order_update_url, headers=headers, json=data)
    response.raise_for_status()


@app.route('/')
def table():
    base64_encoded_data = base64.b64encode(f"{client_key}:{client_secret}".encode("utf-8")).decode("utf-8")
    response = requests.get(
        "https://fabrykasmakow.com.pl/wp-json/wc/v3/orders",
        headers={"Authorization": f"Basic {base64_encoded_data}"}
    )
    data = response.json()

    sorted_data = sorted(data, key=lambda x: x['order_key'])
    grouped_data = [{'order_key': k, 'orders': list(v)} for k, v in itertools.groupby(sorted_data, key=lambda x: x['order_key'])]
    
    return render_template('table.html', data=grouped_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=81)
