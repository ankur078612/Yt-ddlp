import requests
import urllib.parse

API_KEY = "fadc77a3f9msh90809e83902c99ap11df3ajsn5549b00443c6"
API_HOST = "youtube-info-download-api.p.rapidapi.com"

youtube_url = "https://www.youtube.com/watch?v=z19HM7ANZlo"

encoded_url = urllib.parse.quote(youtube_url, safe="")

url = (
    "https://youtube-info-download-api.p.rapidapi.com/ajax/download.php"
    f"?format=mp3&add_info=0&url={encoded_url}"
    "&audio_quality=128&allow_extended_duration=false"
)

headers = {
    "x-rapidapi-key": API_KEY,
    "x-rapidapi-host": API_HOST
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    data = response.json()
    print("✅ API Response:\n")
    print(data)

    # Agar download link ho
    if "download_url" in data:
        print("\n🎵 Download URL:")
        print(data["download_url"])
    else:
        print("\n⚠️ Download link response me nahi aayi")
else:
    print("❌ API Error:", response.status_code, response.text)
