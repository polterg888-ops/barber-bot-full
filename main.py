# main.py - РАБОЧИЙ КОД ДЛЯ ВЕРСИИ 13.15
import os
import sys
import logging

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

def main():
    """Основная функция запуска"""
    try:
        print("=" * 60)
        print("🚀 ТЕЛЕГРАМ БОТ ДЛЯ БАРБЕРШОПА")
        print("=" * 60)
        
        # 1. Проверка конфига
        try:
            from config import BOT_TOKEN, ADMINS
            logger.info(f"✅ Токен: {'установлен' if BOT_TOKEN else 'НЕТ!'}")
            logger.info(f"✅ Админы: {ADMINS}")
            
            if not BOT_TOKEN:
                logger.error("❌ BOT_TOKEN не установлен!")
                return
                
        except ImportError as e:
            logger.error(f"❌ Ошибка загрузки config.py: {e}")
            return
        
        # 2. Инициализация базы данных
        try:
            from database import init_db
            init_db()
            logger.info("✅ База данных инициализирована")
        except Exception as e:
            logger.error(f"❌ Ошибка базы данных: {e}")
            return
        
        # 3. Создание Updater (версия 13.15)
        try:
            from telegram import Updater
            from telegram.ext import CommandHandler, CallbackQueryHandler, MessageHandler, Filters
            
            updater = Updater(token=BOT_TOKEN, use_context=True)
            dp = updater.dispatcher
            
            logger.info("✅ Updater создан")
            
        except Exception as e:
            logger.error(f"❌ Ошибка создания Updater: {e}")
            return
        
        # 4. Импорт обработчиков (важно!)
        try:
            from bot.handlers_13 import start, admin_command, contact_handler, button_handler, text_handler
            
            # Добавление обработчиков (версия 13.15)
            dp.add_handler(CommandHandler("start", start))
            dp.add_handler(CommandHandler("admin", admin_command))
            dp.add_handler(MessageHandler(Filters.contact, contact_handler))
            dp.add_handler(MessageHandler(Filters.text & Filters.private, text_handler))
            dp.add_handler(CallbackQueryHandler(button_handler))
            
            logger.info("✅ Обработчики добавлены")
            
        except ImportError as e:
            logger.error(f"❌ Ошибка импорта обработчиков: {e}")
            logger.error("Создайте файл bot/handlers_13.py")
            return
        
        # 5. Запуск бота
        logger.info("=" * 60)
        logger.info("🤖 БОТ ЗАПУЩЕН И ГОТОВ К РАБОТЕ!")
        logger.info("=" * 60)
        
        updater.start_polling()
        updater.idle()
        
    except Exception as e:
        logger.error(f"💥 КРИТИЧЕСКАЯ ОШИБКА: {e}", exc_info=True)
        sys.exit(1)

if __name__ == '__main__':
    main()
