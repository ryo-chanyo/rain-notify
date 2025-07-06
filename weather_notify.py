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
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print("❗天気データ取得エラー:", e)
        return None

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
        print("❗雨量解析エラー:", e)
    return None

# IFTTT通知を送信
def send_ifttt_notification(webhook_url, message):
    try:
        response = requests.post(webhook_url, json={"value1": message})
        if response.status_code == 200:
            print("✅ 通知を送信しました")
        else:
            print(f"❌ 通知送信失敗: {response.status_code} {response.text}")
    except Exception as e:
        print("❗通知送信エラー:", e)

# メイン処理
def main():
    print("🔍 天気チェック開始:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    app_id = os.getenv("YAHOO_APP_ID")
    lat = os.getenv("LATITUDE")
    lon = os.getenv("LONGITUDE")
    webhook_url = os.getenv("IFTTT_WEBHOOK_URL")

    if not all([app_id, lat, lon, webhook_url]):
        print("❗環境変数が足りません")
        return

    weather = get_weather_forecast(app_id, lat, lon)
    if not weather:
        print("❌ 天気データ取得に失敗しました")
        return

    message = analyze_rainfall(weather)
    if message:
        print("📨 通知内容:", message)
        send_ifttt_notification(webhook_url, message)
    else:
        print("🌤 雨の予報はありません")

if __name__ == "__main__":
    main()
