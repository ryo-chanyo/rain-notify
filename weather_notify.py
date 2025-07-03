import os
import requests
from datetime import datetime

# Yahooの天気APIからデータ取得
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

# 雨が降るか、どの程度かをチェックしてメッセージを返す
def analyze_rainfall(weather_data):
    try:
        forecasts = weather_data["Feature"][0]["Property"]["WeatherList"]["Weather"]
        for forecast in forecasts[:1]:  # 最初の15分だけ確認
            rainfall = float(forecast["Rainfall"])
            time_str = datetime.strptime(forecast["Date"], "%Y%m%d%H%M").strftime("%H:%M")
            if rainfall > 0:
                if rainfall < 1.0:
                    return f"{time_str}頃、ポツポツ来そうです ☔"
                else:
                    return f"{time_str}頃、傘を忘れずに！強めの雨です ☔"
    except Exception as e:
        print("Error analyzing rainfall:", e)
    return None

# IFTTT通知を送信
def send_ifttt_notification(webhook_url, message):
    requests.post(webhook_url, json={"value1": message})

def main():
    app_id = os.getenv("YAHOO_APP_ID")
    lat = os.getenv("LATITUDE")
    lon = os.getenv("LONGITUDE")
    webhook_url = os.getenv("IFTTT_WEBHOOK_URL")

    if not all([app_id, lat, lon, webhook_url]):
        print("環境変数が足りません")
        return

    weather = get_weather_forecast(app_id, lat, lon)
    message = analyze_rainfall(weather)

    if message:
        print("通知内容:", message)
        send_ifttt_notification(webhook_url, message)
    else:
        print("雨の予報はありません")

if __name__ == "__main__":
    main()
