import requests
import os
import asyncio
from telegram import Bot
from datetime import datetime

# 📌 API Anahtarlarını Güvenli Şekilde Kullan
BOT_TOKEN = os.getenv("BOT_TOKEN")  # Çevresel değişkenlerden al
API_KEY = os.getenv("API_KEY")  # Çevresel değişkenlerden al
CHAT_IDS = [-1002281621284, 5637330580]  # Telegram chat ID'leri

# API URL
API_URL = "https://api.coingecko.com/api/v3/coins/markets"

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

    try:
        response = requests.get(API_URL, params=params)
        if response.status_code != 200:
            print(f"❌ API Hatası: {response.status_code} - {response.text}")
            return []

        coins = response.json()
        alert_coins = []

        for coin in coins:
            market_cap = coin.get("market_cap", 0)
            total_volume = coin.get("total_volume", 0)
            
            if market_cap > 0 and total_volume > 0:
                volume_change = (total_volume / market_cap) * 100
                if volume_change >= 60:
                    change_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    alert_coins.append(f"🚀 {coin['name']} ({coin['symbol'].upper()}): {volume_change:.2f}% - {change_time}")

        return alert_coins

    except Exception as e:
        print(f"⚠️ Hata oluştu: {e}")
        return []

async def send_alerts():
    """
    Hacim değişimi yüksek coinleri bul ve Telegram'a gönder.
    """
    if not BOT_TOKEN:
        print("⚠️ Hata: BOT_TOKEN çevresel değişken olarak tanımlanmamış!")
        return

    bot = Bot(token=BOT_TOKEN)

    while True:
        alert_coins = get_coins_with_high_volume_change()
        if alert_coins:
            message = "🚨 **High Volume Change Coins (24h):**\n" + "\n".join(alert_coins)
            for chat_id in CHAT_IDS:
                try:
                    await bot.send_message(chat_id=chat_id, text=message, parse_mode="Markdown")
                    print(f"✅ Uyarı gönderildi: {chat_id}")
                except Exception as e:
                    print(f"❌ Telegram mesajı gönderilemedi: {e}")
        else:
            print("📉 Yüksek hacim değişimi olan coin yok.")

        await asyncio.sleep(600)  # ⏳ 10 dakika bekle

async def main():
    """
    Telegram botunu başlat.
    """
    asyncio.create_task(send_alerts())
    while True:
        await asyncio.sleep(3600)  # Ana döngü çalışmaya devam etsin

if __name__ == "__main__":
    asyncio.run(main())
