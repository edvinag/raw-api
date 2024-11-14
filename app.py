import os
from flask import Flask, request, jsonify

app = Flask(__name__)

# Load the initial IP address from the environment variable, if set
ip_data = {"ip_address": os.environ.get("IP_ADDRESS", None)}

@app.route('/set_ip', methods=['POST'])
def set_ip():
    data = request.get_json()
    if 'ip_address' in data:
        # Update the IP address in the environment variable
        ip_data['ip_address'] = data['ip_address']
        return jsonify({"message": "IP address set successfully!"}), 200
    else:
        return jsonify({"error": "No IP address provided"}), 400

@app.route('/get_ip', methods=['GET'])
def get_ip():
    if ip_data.get('ip_address'):
        return jsonify({"ip_address": ip_data['ip_address']}), 200
    else:
        return jsonify({"error": "No IP address set"}), 404

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
