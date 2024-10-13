from flask import Flask, render_template
import requests
import json


app = Flask(__name__, template_folder='templates', static_folder='static')

# Fetch data from NOAA
def fetch_kp_data():
    try:
        kp_index_url = 'https://services.swpc.noaa.gov/json/planetary_k_index_1m.json'
        response = requests.get(kp_index_url)
        data = json.loads(response.text)
        return data  # This will be a list of dicts
    except requests.RequestException as e:
        print(f"Error fetching data: {e}")
        return []

def northern_hemisphere_image_func():
  try:
    image_url = 'https://services.swpc.noaa.gov/images/aurora-forecast-northern-hemisphere.jpg'
    response = requests.head(image_url)  # Use HEAD request for efficiency
    response.raise_for_status()  # Raise an exception for bad status codes
    return image_url
  except requests.RequestException as e:
    print(f"Error fetching image URL: {e}")
    return 'static/noaa.png'  # Return 'noaa.png' on error



@app.route("/")
def index():
    
    data = fetch_kp_data()
    if data:
        # Pass the full data list to the template
            return render_template('index.html', data=data, image=northern_hemisphere_image_func())

    else:
        return "Failed to fetch data", 500

if __name__ == "__main__":
    app.run(debug=True)
