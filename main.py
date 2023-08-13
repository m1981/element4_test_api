from flask import Flask, render_template
import requests
import base64

app = Flask(__name__)

client_key = "ck_5d652d5fca632c5e60cec2e0b4a9d2f8de2ce8ec"
client_secret = "cs_d3c5698ba2c94885c82f906b3c1c440fc9ae1468"

@app.route('/')
def table():
    base64_encoded_data = base64.b64encode(f"{client_key}:{client_secret}".encode("utf-8")).decode("utf-8")
    response = requests.get(
        "https://fabrykasmakow.com.pl/wp-json/wc/v3/orders",
        headers={"Authorization": f"Basic {base64_encoded_data}"}
    )
    data = response.json()
    return render_template('table.html', data=data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=81)
