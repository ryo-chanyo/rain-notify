import os
import requests
from datetime import datetime

# Yahooの天気API URL（地点の現在の天気予報：雨量など含む）
def get_weather_forecast(app_id, lat, lon):
    url = "https://map.yahooapis.jp/weather/V1/place"
    params = {
        "coordinates": f"{lon},{lat}",
        "appid": app_id,
        "output": "json"
    }
    response = requests.get(url, params=params)
    if response.status_code != 200:
        print("Failed to get weather data")
        return None
    return response.json()

# 雨が降りそうか判断
def will_rain_soon(weather_data):
    try:
        rainfall_values = weather_data["Feature"][0]["Property"]["WeatherList"]["Weather"]
        for forecast in rainfall_values[:1]:  # 最初の15分間だけ見る
            if float(forecast["Rainfall"]) > 0:
                return True
    except Exception as e:
        print("Error in will_rain_soon:", e)
    return False

# IFTTT通知
def send_ifttt_notification(webhook_url):
    requests.post(webhook_url, json={ "value1": "15分後に雨が降ります ☔" })

def main():
    now = datetime.now()
    #if not (7 <= now.hour < 21):
        #print("通知時間外です")
        #return

    app_id = os.getenv("YAHOO_APP_ID")
    lat = os.getenv("34.5376861")
    lon = os.getenv("136.6154472")
    #lat = os.getenv("LATITUDE")
    #lon = os.getenv("LONGITUDE")
    webhook_url = os.getenv("IFTTT_WEBHOOK_URL")

    if not all([app_id, lat, lon, webhook_url]):
        print("環境変数が足りません")
        return

    weather = get_weather_forecast(app_id, lat, lon)
    if weather and will_rain_soon(weather):
        send_ifttt_notification(webhook_url)

if __name__ == "__main__":
    main()
