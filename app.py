from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

API_KEY = "389b209e960e4c0a271e91867f3edb69"  # Ganti dengan API key dari OpenWeather
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

def get_weather(city):
    params = {
        'q': city,
        'appid': API_KEY,
        'units': 'metric'
    }
    response = requests.get(BASE_URL, params=params)
    if response.status_code == 200:
        data = response.json()
        weather_info = {
            "city": data["name"],
            "temperature": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "weather": data["weather"][0]["description"]
        }
        return weather_info
    else:
        return None

@app.route('/')
def index():
    return render_template('index.html')  # Merender index.html dari folder templates

@app.route('/weather', methods=['GET'])
def weather():
    city = request.args.get('city')
    if not city:
        return jsonify({"error": "City parameter is required"}), 400

    weather_data = get_weather(city)
    if weather_data:
        return jsonify(weather_data)
    else:
        return jsonify({"error": "City not found or API error"}), 404

if __name__ == '__main__':
    app.run(debug=True)
