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

# Проверяем версию Python
import sys
print(f"Python версия: {sys.version}")
print(f"Токен: {'установлен' if BOT_TOKEN else 'НЕТ!'}")

# Импортируем модули
from database import init_db, check_and_fix_db
from bot.handlers import set_bot

async def main():
    """Основная функция запуска бота"""
    try:
        print("=" * 60)
        print("🚀 ТЕЛЕГРАМ БОТ ДЛЯ БАРБЕРШОПА")
        print("=" * 60)
        
        # Инициализация базы данных
        print("🔧 Инициализируем базу данных...")
        init_db()
        check_and_fix_db()
        print("✅ База данных готова")
        
        # Создаем Application
        print("🤖 Создаем Application...")
        
        try:
            # Способ 1: Для версий 20.x+
            from telegram.ext import Application
            application = Application.builder().token(BOT_TOKEN).build()
            print("✅ Application создан через builder()")
            
        except Exception as e:
            print(f"⚠️ Способ 1 не сработал: {e}")
            
            try:
                # Способ 2: Для старых версий 13.x-20.x
                from telegram.ext import Updater
                updater = Updater(token=BOT_TOKEN, use_context=True)
                application = updater.application
                print("✅ Application создан через Updater")
                
            except Exception as e2:
                print(f"❌ Способ 2 не сработал: {e2}")
                raise Exception("Не удалось создать Application!")
        
        # Регистрация обработчиков
        print("📝 Регистрируем обработчики...")
        
        from bot.handlers import (
            start, 
            admin_command, 
            contact_handler, 
            button_handler, 
            text_handler
        )
        
        # Команды
        application.add_handler(telegram.ext.CommandHandler("start", start))
        application.add_handler(telegram.ext.CommandHandler("admin", admin_command))
        
        # Контакт
        application.add_handler(telegram.ext.MessageHandler(
            telegram.ext.filters.CONTACT, 
            contact_handler
        ))
        
        # Callback кнопки
        application.add_handler(telegram.ext.CallbackQueryHandler(button_handler))
        
        # Текстовые сообщения
        application.add_handler(telegram.ext.MessageHandler(
            telegram.ext.filters.TEXT & ~telegram.ext.filters.COMMAND, 
            text_handler
        ))
        
        # Устанавливаем бота для уведомлений
        set_bot(application.bot)
        
        print("✅ Все обработчики зарегистрированы")
        print("🤖 Бот запускается...")
        
        # Запуск бота
        await application.initialize()
        await application.start()
        await application.updater.start_polling()
        
        print("=" * 60)
        print("✅ Бот успешно запущен и готов к работе!")
        print("=" * 60)
        
        # Бесконечный цикл
        while True:
            await asyncio.sleep(3600)
            
    except Exception as e:
        print(f"💥 КРИТИЧЕСКАЯ ОШИБКА: {e}")
        import traceback
        traceback.print_exc()
        raise

if __name__ == '__main__':
    # Проверяем наличие необходимых импортов
    try:
        import telegram
        from telegram.ext import Application, Updater, CommandHandler, MessageHandler, CallbackQueryHandler, filters
        print(f"✅ Версия python-telegram-bot: {telegram.__version__}")
    except ImportError as e:
        print(f"❌ Ошибка импорта: {e}")
        print("Установите библиотеку: pip install python-telegram-bot==20.7")
        exit(1)
    
    # Запуск
    asyncio.run(main())
