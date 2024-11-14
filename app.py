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
    app.run(debug=True)
