from flask import Flask, jsonify, request
import json
import requests

app = Flask(__name__)

DATA_FILE = "data.json"
API_URL = "https://www.travel-advisory.info/api"

def fetch_data():
    try:
        response = requests.get(API_URL)
        response.raise_for_status()
        data = response.json()

        with open(DATA_FILE, 'w') as file:
            json.dump(data, file, indent=2)

        return data
    except requests.RequestException as e:
        print(f"Error fetching data from the API: {e}")
        return None

def load_data():
    try:
        with open(DATA_FILE, 'r') as file:
            data = json.load(file)
        return data
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error loading data from {DATA_FILE}: {e}")
        return None

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok"})

@app.route('/diag', methods=['GET'])
def diag():
    try:
        response = requests.get(API_URL)
        response.raise_for_status()
        api_status = {"api_status": {"code": response.status_code, "status": "ok"}}
        return jsonify(api_status)
    except requests.RequestException as e:
        print(f"Error checking API status: {e}")
        return jsonify({"error": "Error checking API status"}), 500

@app.route('/convert', methods=['GET'])
def convert():
    country_name = request.args.get('countryName')
 
    if not country_name:
        return jsonify({"error": "Country name not provided"}), 400
 
    data = load_data()
 
    if not data:
        return jsonify({"error": "Error loading data"}), 500
    try:
        for country_code, country_data in data['data'].items():
            if country_data.get('name') == country_name:
                country_code = country_data.get('iso_alpha2', None)
                if country_code:
                  return jsonify({"countryCode": country_code})
                else:
                  return jsonify({"error": "ISO alpha-2 code not found for the country"}), 404
 
        return jsonify({"error": "Country not found"}), 404
    except Exception as e:
        print(f"Error converting country name to code: {e}")
        return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    data = load_data()

    if not data:
        print("Fetching data from the API...")
        fetch_data()

    app.run(debug=True , host="0.0.0.0")
