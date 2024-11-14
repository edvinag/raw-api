import os
from flask import Flask, request, jsonify

app = Flask(__name__)

# Dictionary to store the location data
location_data = {}

@app.route('/set_location', methods=['POST'])
def set_location():
    data = request.get_json()
    if 'location' in data:
        location_data['location'] = data['location']
        return jsonify({"message": "Location set successfully!"}), 200
    else:
        return jsonify({"error": "No location provided"}), 400

@app.route('/get_location', methods=['GET'])
def get_location():
    if 'location' in location_data:
        return jsonify({"location": location_data['location']}), 200
    else:
        return jsonify({"error": "No location set"}), 404

if __name__ == '__main__':
    # Get the port from the environment (Render provides this automatically)
    port = int(os.environ.get("PORT", 5000))
    # Run the app, binding to 0.0.0.0 to be accessible externally
    app.run(host='0.0.0.0', port=port)
