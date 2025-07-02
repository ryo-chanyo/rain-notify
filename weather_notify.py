import os
import requests

# 環境変数から値を取得
APP_ID = os.getenv("YAHOO_APP_ID")
LAT = os.getenv("LATITUDE")
LON = os.getenv("LONGITUDE")
IFTTT_URL = os.getenv("IFTTT_WEBHOOK_URL")

# Yahoo!気象APIのエンドポイント（GeoJSON形式）
url = f"https://map.yahooapis.jp/weather/V1/place?coordinates={LON},{LAT}&output=json&appid={APP_ID}"

def get_weather_info():
    try:
        response = requests.get(url)
        data = response.json()

        # 時間帯ごとの降水確率を取得（例として3時間ごと）
        features = data["Feature"][0]["Property"]["WeatherList"]["Weather"]

        message_lines = ["【今日の降水確率】"]
        rain_expected = False

        for f in features:
            time = f["Date"]
            rain = f["Rainfall"]
            message_lines.append(f"{time}: {rain}%")
            if float(rain) >= 30:  # 雨の可能性が高いと判断
                rain_expected = True

        message = "\n".join(message_lines)

        if rain_expected:
            message += "\n☔ 雨の可能性あり！傘を忘れずに。"

        return message

    except Exception as e:
        return f"天気情報の取得に失敗しました: {str(e)}"

def notify_ifttt(message):
    if not IFTTT_URL:
        print("IFTTT WebhookのURLが未設定です")
        return

    payload = {"value1": message}
    try:
        response = requests.post(IFTTT_URL, json=payload)
        print("IFTTT通知を送信しました:", response.status_code)
    except Exception as e:
        print("IFTTT通知に失敗しました:", str(e))

if __name__ == "__main__":
    weather_message = get_weather_info()
    print(weather_message)
    notify_ifttt(weather_message)
