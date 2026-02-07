# main.py - ДЛЯ ВЕРСИИ 20.7+
import sys
import os

# ========== ФИКСЫ ДЛЯ МОДУЛЕЙ ==========
class MockImghdr:
    @staticmethod
    def what(file, h=None):
        return None

class FakeDotenv:
    @staticmethod
    def load_dotenv():
        pass

sys.modules['imghdr'] = MockImghdr()
sys.modules['dotenv'] = FakeDotenv()

# ========== ОСНОВНОЙ КОД ==========
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def error_handler(update, context):
    logger.error(f"Ошибка: {context.error}", exc_info=True)

def main():
    try:
        print("=" * 60)
        print("🚀 ТЕЛЕГРАМ БОТ ДЛЯ БАРБЕРШОПА")
        print("Версия: 20.7+")
        print("=" * 60)
        
        # 1. Загружаем config
        from config import BOT_TOKEN, ADMINS
        logger.info(f"✅ Токен: {'установлен' if BOT_TOKEN else 'НЕТ!'}")
        logger.info(f"✅ Админы: {ADMINS}")
        
        if not BOT_TOKEN:
            logger.error("❌ BOT_TOKEN не установлен!")
            return
        
        # 2. Инициализация базы
        from database import init_db
        init_db()
        logger.info("✅ База данных инициализирована")
        
        # 3. СОЗДАЕМ APPLICATION (версия 20.7+)
        logger.info("🤖 Создаем Telegram Application...")
        try:
            # Импорт для версии 20.7+
            from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters
            
            application = Application.builder().token(BOT_TOKEN).build()
            
            # Добавляем обработчик ошибок
            application.add_error_handler(error_handler)
            
            logger.info("✅ Application создан")
            
        except Exception as e:
            logger.error(f"❌ Ошибка создания Application: {e}")
            import traceback
            logger.error(traceback.format_exc())
            return
        
        # 4. ЗАГРУЗКА ОБРАБОТЧИКОВ
        logger.info("🔄 Загружаем обработчики...")
        try:
            # Импортируем обработчики
            from bot.handlers import start, admin_command, contact_handler, button_handler, text_handler
            
            # Регистрируем обработчики (версия 20.7+)
            application.add_handler(CommandHandler("start", start))
            application.add_handler(CommandHandler("admin", admin_command))
            application.add_handler(MessageHandler(filters.CONTACT, contact_handler))
            application.add_handler(MessageHandler(filters.TEXT & filters.ChatType.PRIVATE, text_handler))
            application.add_handler(CallbackQueryHandler(button_handler))
            
            logger.info("✅ Все обработчики добавлены")
            
        except Exception as e:
            logger.error(f"❌ Ошибка импорта обработчиков: {e}")
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
        
        # Запускаем polling (версия 20.7+)
        logger.info("▶️ Запускаем polling...")
        application.run_polling(
            drop_pending_updates=True,
            allowed_updates=None
        )
        
    except Exception as e:
        logger.error(f"💥 КРИТИЧЕСКАЯ ОШИБКА: {e}", exc_info=True)
        import traceback
        logger.error(traceback.format_exc())
        sys.exit(1)

if __name__ == '__main__':
    main()
