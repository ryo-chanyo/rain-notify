import os
import requests
import datetime

def get_weather(lat, lon, app_id):
    url = f"https://map.yahooapis.jp/weather/V1/place?coordinates={lon},{lat}&appid={app_id}&output=json"
    res = requests.get(url)
    res.raise_for_status()
    return res.json()

def is_rainy(weather_json):
    features = weather_json["Feature"]
    if not features:
        return False
    weather_elements = features[0]["Property"]["WeatherList"]["Weather"]
    if not weather_elements:
        return False
    # 直近（15分後）の降水強度（mm/h）
    rain_value = float(weather_elements[0]["Rainfall"])
    return rain_value >= 0.1

def send_ifttt_notification(url, message):
    requests.post(url, json={"value1": message})

def main():
    lat = os.getenv("LATITUDE")
    lon = os.getenv("LONGITUDE")
    app_id = os.getenv("YAHOO_APP_ID")
    ifttt_url = os.getenv("IFTTT_WEBHOOK_URL")

    weather = get_weather(lat, lon, app_id)
    if is_rainy(weather):
        send_ifttt_notification(ifttt_url, "15分後に雨が降ります ☔")

if __name__ == "__main__":
    main()
