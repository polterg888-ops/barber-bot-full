import os
import logging
import asyncio
import sys

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

print(f"Python версия: {sys.version}")
print(f"Токен: {'установлен' if BOT_TOKEN else 'НЕТ!'}")

async def main():
    """Основная функция запуска бота"""
    try:
        print("=" * 60)
        print("🚀 ТЕЛЕГРАМ БОТ ДЛЯ БАРБЕРШОПА")
        print("=" * 60)
        
        # Инициализация базы данных (ПРОСТОЙ ВАРИАНТ)
        print("🔧 Инициализируем базу данных...")
        try:
            from database import init_db
            init_db()
            print("✅ База данных инициализирована")
        except Exception as e:
            print(f"⚠️ Предупреждение при инициализации БД: {e}")
        
        # Импортируем telegram
        try:
            import telegram
            from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters
            print(f"✅ Версия python-telegram-bot: {telegram.__version__}")
        except ImportError as e:
            print(f"❌ Ошибка импорта: {e}")
            print("Установите библиотеку: pip install python-telegram-bot==20.7")
            exit(1)
        
        # Создаем Application
        print("🤖 Создаем Application...")
        
        try:
            # Способ для версий 20.x
            application = Application.builder().token(BOT_TOKEN).build()
            print("✅ Application создан")
        except Exception as e:
            print(f"❌ Ошибка создания Application: {e}")
            
            # Пробуем альтернативный способ
            try:
                from telegram.ext import Updater
                updater = Updater(token=BOT_TOKEN, use_context=True)
                application = updater.application
                print("✅ Application создан через Updater")
            except Exception as e2:
                print(f"❌ Все способы не сработали: {e2}")
                raise
        
        # Регистрация обработчиков
        print("📝 Регистрируем обработчики...")
        
        try:
            from bot.handlers import start, admin_command, contact_handler, button_handler, text_handler
        except ImportError as e:
            print(f"❌ Ошибка импорта обработчиков: {e}")
            print("Проверьте файлы в папке bot/")
            exit(1)
        
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
        
        # Запуск бота
        await application.initialize()
        await application.start()
        
        try:
            await application.updater.start_polling()
        except AttributeError:
            # Для некоторых версий
            print("⚠️ start_polling не доступен, используем run_polling")
            await application.run_polling()
        
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
    asyncio.run(main())
