import os
import logging
import asyncio
from datetime import datetime

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Проверка наличия токена
BOT_TOKEN = os.environ.get('BOT_TOKEN')
if not BOT_TOKEN:
    logger.error("❌ ОШИБКА: Не найден BOT_TOKEN в переменных окружения!")
    logger.error("Добавьте BOT_TOKEN в настройках Render: Settings -> Environment")
    exit(1)

print("=" * 60)
print("🚀 ТЕЛЕГРАМ БОТ ДЛЯ БАРБЕРШОПА")
print("=" * 60)

async def main():
    """Основная функция запуска бота"""
    try:
        # Проверяем версию
        import telegram
        print(f"✅ Версия python-telegram-bot: {telegram.__version__}")
        
        # Инициализация базы данных
        print("🔧 Инициализируем базу данных...")
        try:
            from database import init_db
            init_db()
            print("✅ База данных инициализирована")
        except Exception as e:
            print(f"⚠️ Предупреждение при инициализации БД: {e}")
        
        # Импорты для версии 21.x
        from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters
        
        # Создаем Application (версия 21.x)
        print("🤖 Создаем Application...")
        
        # ПРАВИЛЬНЫЙ СПОСОБ для 21.x
        application = Application.builder().token(BOT_TOKEN).build()
        print("✅ Application создан")
        
        # Регистрация обработчиков
        print("📝 Регистрируем обработчики...")
        
        from bot.handlers import start, admin_command, contact_handler, button_handler, text_handler
        
        # Команды
        application.add_handler(CommandHandler("start", start))
        application.add_handler(CommandHandler("admin", admin_command))
        
        # Контакт
        application.add_handler(MessageHandler(
            filters.CONTACT, 
            contact_handler
        ))
        
        # Callback кнопки
        application.add_handler(CallbackQueryHandler(button_handler))
        
        # Текстовые сообщения
        application.add_handler(MessageHandler(
            filters.TEXT & ~filters.COMMAND, 
            text_handler
        ))
        
        # Устанавливаем бота для уведомлений
        try:
            from bot.handlers import set_bot
            set_bot(application.bot)
            print("✅ Бот установлен для уведомлений")
        except:
            print("⚠️ Функция set_bot не найдена")
        
        print("✅ Все обработчики зарегистрированы")
        print("🤖 Запускаем бота...")
        
        # ЗАПУСК для версии 21.x
        await application.initialize()
        await application.start()
        await application.updater.start_polling()
        
        print("=" * 60)
        print("✅ Бот успешно запущен и готов к работе!")
        print("=" * 60)
        
        # Бесконечный цикл
        await asyncio.Event().wait()
        
    except Exception as e:
        print(f"💥 КРИТИЧЕСКАЯ ОШИБКА: {e}")
        import traceback
        traceback.print_exc()
        raise

if __name__ == '__main__':
    asyncio.run(main())
