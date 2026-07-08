import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
from urllib.request import urlopen

API_KEY = "24e2ef95fa492033f6ce212277917fa4"      # <-- Replace with your OpenWeatherMap API Key


class MyServer(BaseHTTPRequestHandler):

    def do_GET(self):

        # Open HTML page
        if self.path == "/" or self.path == "/index.html":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()

            with open("index.html", "rb") as file:
                self.wfile.write(file.read())
            return

        # Weather API
        if self.path.startswith("/weather"):

            query = parse_qs(urlparse(self.path).query)
            city = query.get("city", [""])[0]

            try:

                weather_url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

                weather = json.loads(urlopen(weather_url).read())

                lat = weather["coord"]["lat"]
                lon = weather["coord"]["lon"]

                aqi_url = f"https://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={API_KEY}"

                aqi = json.loads(urlopen(aqi_url).read())

                result = {
                    "city": weather["name"],
                    "temperature": weather["main"]["temp"],
                    "humidity": weather["main"]["humidity"],
                    "pressure": weather["main"]["pressure"],
                    "weather": weather["weather"][0]["description"],
                    "wind": weather["wind"]["speed"],
                    "aqi": aqi["list"][0]["main"]["aqi"]
                }

                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()

                self.wfile.write(json.dumps(result).encode())

            except Exception as e:

                self.send_response(500)
                self.end_headers()

                self.wfile.write(json.dumps({"error": str(e)}).encode())

            return


PORT = 8000

print("Server Running...")
print("Open http://localhost:8000")

HTTPServer(("localhost", PORT), MyServer).serve_forever()