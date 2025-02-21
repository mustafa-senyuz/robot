import os
import asyncio
from telegram import Bot
import requests
from datetime import datetime

# Telegram bot bilgileri
BOT_TOKEN = os.getenv("BOT_TOKEN")  # Çevresel değişkenlerden alınmalı
CHAT_IDS = [-1002281621284, 5637330580]  # Telegram chat ID'leri

# API bilgileri
API_KEY = "1534b0d1-22db-4969-8419-45bc9b7be9be"  # API key
API_URL = "https://api.coingecko.com/api/v3/coins/markets"  # CoinGecko API URL'si

async def countdown_and_send_alerts():
    """
    30 saniyelik geri sayımı başlat ve Telegram'a mesaj gönder.
    Her 10 saniyede bir mesaj gönderilecek.
    0 saniye kalınca API'den veri çekilecek.
    """
    if not BOT_TOKEN:
        print("⚠️ Hata: BOT_TOKEN çevresel değişken olarak tanımlanmamış!")
        return

    bot = Bot(token=BOT_TOKEN)

    while True:
        for remaining in range(30, 0, -10):
            countdown_message = f"API'nin çağrılmasına {remaining} saniye kaldı..."
            for chat_id in CHAT_IDS:
                try:
                    await bot.send_message(chat_id=chat_id, text=countdown_message)
                    print(f"✅ Geri sayım mesajı gönderildi: {chat_id}")
                except Exception as e:
                    print(f"❌ Telegram mesajı gönderilemedi: {e}")
            await asyncio.sleep(10)  # 10 saniyede bir geri sayımı gönder

        # 0 saniye kaldı, API'den veri çekme işlemi yapılacak
        print("API'nin çağrılmasına 0 saniye kaldı, API'den veri çekiliyor...")
        alert_coins = get_coins_with_high_volume_change()
        if alert_coins:
            message = "🚨 High Volume Change Coins (24h):\n" + "\n".join(alert_coins)
            for chat_id in CHAT_IDS:
                try:
                    await bot.send_message(chat_id=chat_id, text=message)
                    print(f"✅ API verisi gönderildi: {chat_id}")
                except Exception as e:
                    print(f"❌ API verisi gönderilemedi: {e}")

        # 30 saniyelik süreyi beklemeden önce tekrar başlat
        print("30 saniye doldu, tekrar başlatılıyor...")
        await asyncio.sleep(30)

def get_coins_with_high_volume_change():
    """
    API'den verileri al ve hacmi %60 veya daha fazla artan coinleri filtrele.
    """
    params = {
        "vs_currency": "usd",
        "order": "volume_desc",
        "per_page": 100,
        "page": 1,
        "sparkline": False
    }
    headers = {
        "Authorization": f"Bearer {API_KEY}"
    }

    try:
        response = requests.get(API_URL, params=params, headers=headers)
        if response.status_code != 200:
            print(f"API Error: {response.status_code} - {response.text}")
            return []

        coins = response.json()
        alert_coins = []

        for coin in coins:
            market_cap = coin.get("market_cap", 0)
            total_volume = coin.get("total_volume", 0)
            if market_cap > 0:
                volume_change = total_volume / market_cap * 100
                if volume_change >= 60:
                    change_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    alert_coins.append(f"{coin['name']} ({coin['symbol']}): {volume_change:.2f}% - Last Change: {change_time}")
        return alert_coins

    except Exception as e:
        print(f"Error occurred: {e}")
        return []

async def main():
    """
    Telegram botunu başlat.
    """
    asyncio.create_task(countdown_and_send_alerts())  # Geri sayım ve API çağrısını başlat
    while True:
        await asyncio.sleep(3600)  # Ana döngü çalışmaya devam etsin

if __name__ == "__main__":
    asyncio.run(main())
