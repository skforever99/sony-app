import requests
import json

def fetch_data(api_url):
    response = requests.get(api_url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch data from the API. Status code: {response.status_code}")
        return None

def save_to_file(data, filename):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=2)
    print(f"Data saved to {filename}")

def main():
    api_url = "https://www.travel-advisory.info/api"
    data = fetch_data(api_url)

    if data:
        save_to_file(data, "data.json")

if __name__ == "__main__":
    main()
