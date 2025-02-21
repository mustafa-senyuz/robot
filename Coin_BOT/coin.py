import os
import asyncio
from telegram import Bot
from datetime import datetime

# 📌 API Anahtarlarını Güvenli Şekilde Kullan
BOT_TOKEN = os.getenv("BOT_TOKEN")  # Çevresel değişkenlerden al
CHAT_IDS = [-1002281621284, 5637330580]  # Telegram chat ID'leri

async def countdown_and_send_alerts():
    """
    30 saniyelik geri sayımı başlat ve Telegram'a mesaj gönder.
    """
    if not BOT_TOKEN:
        print("⚠️ Hata: BOT_TOKEN çevresel değişken olarak tanımlanmamış!")
        return

    bot = Bot(token=BOT_TOKEN)

    while True:
        # 30 saniyelik geri sayım yap
        for remaining in range(30, 0, -1):
            countdown_message = f"Geri sayım: {remaining} saniye kaldı."
            for chat_id in CHAT_IDS:
                try:
                    await bot.send_message(chat_id=chat_id, text=countdown_message)
                    print(f"✅ Geri sayım mesajı gönderildi: {chat_id}")
                except Exception as e:
                    print(f"❌ Telegram mesajı gönderilemedi: {e}")
            await asyncio.sleep(1)  # Her saniyede bir geri sayımı gönderecek

        # 30 saniye dolduktan sonra tekrar başlayacak
        print("30 saniye doldu, tekrar başlatılıyor...")

        # Burada API'den veri çekebilirsiniz ya da sadece geri sayım gösterebilirsiniz.
        # Eğer API verisi çekmek isterseniz, yukarıdaki `get_coins_with_high_volume_change` fonksiyonunu kullanabilirsiniz.
        # Örnek:
        # alert_coins = get_coins_with_high_volume_change()
        # if alert_coins:
        #     message = "🚨 **High Volume Change Coins (24h):**\n" + "\n".join(alert_coins)
        #     for chat_id in CHAT_IDS:
        #         await bot.send_message(chat_id=chat_id, text=message, parse_mode="Markdown")
        
        # 30 saniye beklemeden önce
        await asyncio.sleep(30)

async def main():
    """
    Telegram botunu başlat.
    """
    asyncio.create_task(countdown_and_send_alerts())  # Geri sayım ve uyarıları başlat
    while True:
        await asyncio.sleep(3600)  # Ana döngü çalışmaya devam etsin

if __name__ == "__main__":
    asyncio.run(main())
