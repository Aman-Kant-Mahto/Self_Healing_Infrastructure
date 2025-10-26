from flask import Flask, request
import os

app = Flask(__name__)

@app.route('/', methods=['POST'])
def webhook():
    data = request.json
    if data and "alerts" in data:
        for alert in data["alerts"]:
            if alert["status"] == "firing":
                os.system("ansible-playbook restart-nginx.yml")
    return "OK", 200

app.run(host='0.0.0.0', port=5001)
