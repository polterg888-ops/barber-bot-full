# main.py - ИСПРАВЛЕННЫЙ
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
        print("🚀 ТЕЛЕГРАМ БОТ ДЛЯ БАРБЕРШОПА - ПОЛНАЯ ВЕРСИЯ")
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
        
        # 3. Создание приложения бота
        try:
            from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters
            
            app = Application.builder().token(BOT_TOKEN).build()
            logger.info("✅ Приложение бота создано")
            
        except Exception as e:
            logger.error(f"❌ Ошибка создания приложения: {e}")
            return
        
        # 4. Импорт обработчиков (важно: ПОСЛЕ создания приложения)
        try:
            # Импортируем основные функции
            from bot.handlers import start, admin_command, contact_handler, button_handler, text_handler
            
            # Импортируем set_application отдельно
            from bot.handlers import set_application
            set_application(app)
            
            logger.info("✅ Обработчики загружены")
            
        except ImportError as e:
            logger.error(f"❌ Ошибка загрузки обработчиков: {e}")
            logger.error("Проверьте папку bot/:")
            logger.error("1. __init__.py (пустой файл)")
            logger.error("2. handlers.py")
            logger.error("3. admin_keyboards.py")
            logger.error("4. user_keyboards.py")
            return
        
        # 5. Добавление обработчиков
        try:
            app.add_handler(CommandHandler("start", start))
            app.add_handler(CommandHandler("admin", admin_command))
            app.add_handler(MessageHandler(filters.CONTACT, contact_handler))
            app.add_handler(MessageHandler(filters.TEXT & filters.ChatType.PRIVATE, text_handler))
            app.add_handler(CallbackQueryHandler(button_handler))
            
            logger.info("✅ Все обработчики добавлены")
            
        except Exception as e:
            logger.error(f"❌ Ошибка добавления обработчиков: {e}")
            return
        
        # 6. Запуск бота
        logger.info("=" * 60)
        logger.info("🤖 БОТ ЗАПУЩЕН СО ВСЕМИ ФУНКЦИЯМИ:")
        logger.info("✅ Запись на услуги")
        logger.info("✅ Календарь записей")
        logger.info("✅ Управление услугами")
        logger.info("✅ Уведомления админам")
        logger.info("✅ Закрытие/открытие времени")
        logger.info("✅ Работа с пользователями")
        logger.info("=" * 60)
        
        app.run_polling(
            drop_pending_updates=True,
            allowed_updates=["message", "callback_query"]
        )
        
    except Exception as e:
        logger.error(f"💥 КРИТИЧЕСКАЯ ОШИБКА: {e}", exc_info=True)
        sys.exit(1)

if __name__ == '__main__':
    main()
