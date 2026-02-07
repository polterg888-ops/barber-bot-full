# main.py - ПОЛНЫЙ ИСПРАВЛЕННЫЙ КОД
import sys
import os

# ========== ФИКСЫ ДЛЯ МОДУЛЕЙ ==========
# 1. Фикс для imghdr (удален в Python 3.11+)
try:
    import imghdr
except ImportError:
    class MockImghdr:
        @staticmethod
        def what(file, h=None):
            return None
    sys.modules['imghdr'] = MockImghdr()

# 2. Фикс для dotenv (если где-то пытается импортироваться)
try:
    import dotenv
except ImportError:
    class FakeDotenv:
        @staticmethod
        def load_dotenv():
            pass  # На Render.com переменные уже в окружении
    sys.modules['dotenv'] = FakeDotenv()

# ========== ОСНОВНОЙ КОД ==========
import logging

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

# Обработчик ошибок для бота
def error_handler(update, context):
    """Логируем ошибки"""
    logger.error(f'Ошибка: {context.error}', exc_info=True)

def main():
    """Основная функция запуска"""
    try:
        print("=" * 60)
        print("🚀 ТЕЛЕГРАМ БОТ ДЛЯ БАРБЕРШОПА")
        print("=" * 60)
        
        # 1. ЗАГРУЗКА КОНФИГУРАЦИИ
        logger.info("📋 Загружаем конфигурацию...")
        try:
            # Импортируем config (после фиксов)
            from config import BOT_TOKEN, ADMINS, TIME_SLOT_MINUTES, ENABLE_ADMIN_NOTIFICATIONS
            
            logger.info(f"✅ Токен: {'установлен' if BOT_TOKEN else 'НЕТ!'}")
            logger.info(f"✅ Админы: {ADMINS}")
            
            if not BOT_TOKEN:
                logger.error("❌ ОШИБКА: BOT_TOKEN не установлен!")
                logger.error("Добавьте BOT_TOKEN в переменные окружения Render.com")
                return
                
        except ImportError as e:
            logger.error(f"❌ Ошибка загрузки config.py: {e}")
            logger.error("Проверьте содержимое config.py")
            return
        
        # 2. ИНИЦИАЛИЗАЦИЯ БАЗЫ ДАННЫХ
        logger.info("🗄️ Инициализируем базу данных...")
        try:
            from database import init_db
            init_db()
            logger.info("✅ База данных инициализирована")
        except Exception as e:
            logger.error(f"❌ Ошибка базы данных: {e}")
            return
        
        # 3. СОЗДАНИЕ UPDATER
        logger.info("🤖 Создаем Telegram бота...")
        try:
            from telegram import Updater
            from telegram.ext import CommandHandler, CallbackQueryHandler, MessageHandler, Filters
            
            updater = Updater(token=BOT_TOKEN, use_context=True)
            dp = updater.dispatcher
            
            # Добавляем обработчик ошибок
            dp.add_error_handler(error_handler)
            
            logger.info("✅ Updater создан")
            
        except Exception as e:
            logger.error(f"❌ Ошибка создания Updater: {e}")
            return
        
        # 4. ЗАГРУЗКА ОБРАБОТЧИКОВ
        logger.info("🔄 Загружаем обработчики...")
        try:
            from bot.handlers import (
                start, admin_command, contact_handler, 
                button_handler, text_handler, set_application
            )
            
            # Передаем application для уведомлений
            set_application(updater)
            
            # Добавляем обработчики
            dp.add_handler(CommandHandler("start", start))
            dp.add_handler(CommandHandler("admin", admin_command))
            dp.add_handler(MessageHandler(Filters.contact, contact_handler))
            dp.add_handler(MessageHandler(Filters.text & Filters.private, text_handler))
            dp.add_handler(CallbackQueryHandler(button_handler))
            
            logger.info("✅ Все обработчики добавлены")
            
        except ImportError as e:
            logger.error(f"❌ Ошибка импорта обработчиков: {e}")
            logger.error("Проверьте файлы в папке bot/")
            import traceback
            logger.error(traceback.format_exc())
            return
        
        # 5. ЗАПУСК БОТА
        logger.info("=" * 60)
        logger.info("🤖 БОТ ЗАПУЩЕН СО ВСЕМИ ФУНКЦИЯМИ:")
        logger.info("✅ Запись на услуги")
        logger.info("✅ Календарь записей")
        logger.info("✅ Управление услугами")
        logger.info("✅ Уведомления админам")
        logger.info("✅ Закрытие/открытие времени")
        logger.info("=" * 60)
        
        # Запускаем polling
        updater.start_polling(
            drop_pending_updates=True,
            timeout=30
        )
        
        logger.info("✅ Бот запущен и работает!")
        logger.info("⏳ Ожидаем сообщений...")
        
        # Блокируем выполнение
        updater.idle()
        
    except Exception as e:
        logger.error(f"💥 КРИТИЧЕСКАЯ ОШИБКА: {e}", exc_info=True)
        import traceback
        logger.error(traceback.format_exc())
        sys.exit(1)

if __name__ == '__main__':
    main()
