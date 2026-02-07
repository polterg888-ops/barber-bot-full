# config.py - ИСПРАВЛЕННЫЙ
import os

# НЕ ИСПОЛЬЗУЕМ dotenv на Render.com
# переменные окружения устанавливаются в панели Render

BOT_TOKEN = os.getenv("BOT_TOKEN")

# Разделяем ADMINS по запятым
admins_str = os.getenv("ADMINS", "")
ADMINS = [int(x) for x in admins_str.split(",") if x.strip()]

TIME_SLOT_MINUTES = 60
ENABLE_ADMIN_NOTIFICATIONS = True

# Проверка при запуске
if __name__ == "__main__":
    if not BOT_TOKEN:
        print("❌ ОШИБКА: BOT_TOKEN не установлен!")
    else:
        print(f"✅ BOT_TOKEN: {'***' + BOT_TOKEN[-5:] if BOT_TOKEN else 'Нет'}")
    
    if not ADMINS:
        print("⚠️  ПРЕДУПРЕЖДЕНИЕ: ADMINS не установлены")
    else:
        print(f"✅ ADMINS: {ADMINS}")
