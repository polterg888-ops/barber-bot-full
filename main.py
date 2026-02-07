# main.py - ДЛЯ ВЕРСИИ 20.7
import sys
import os
import logging

# Фиксы для модулей
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
        print("Версия: 20.7")
        print("=" * 60)
        
        # Импортируем config
        from config import BOT_TOKEN, ADMINS
        logger.info(f"✅ Токен: {'установлен' if BOT_TOKEN else 'НЕТ!'}")
        
        if not BOT_TOKEN:
            logger.error("❌ BOT_TOKEN не установлен!")
            return
        
        # Инициализация базы
        from database import init_db
        init_db()
        logger.info("✅ База данных инициализирована")
        
        # Создаем Application (версия 20.7)
        from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters
        
        application = Application.builder().token(BOT_TOKEN).build()
        
        # Обработчик ошибок
        application.add_error_handler(error_handler)
        
        # Импортируем обработчики
        from bot.handlers import start, admin_command, contact_handler, button_handler, text_handler
        
        # Регистрируем обработчики (версия 20.7)
        application.add_handler(CommandHandler("start", start))
        application.add_handler(CommandHandler("admin", admin_command))
        application.add_handler(MessageHandler(filters.CONTACT, contact_handler))
        application.add_handler(MessageHandler(filters.TEXT & filters.ChatType.PRIVATE, text_handler))
        application.add_handler(CallbackQueryHandler(button_handler))
        
        logger.info("✅ Все обработчики добавлены")
        
        # Запускаем бота
        logger.info("🤖 Запускаем бота...")
        application.run_polling(
            allowed_updates=None,
            drop_pending_updates=True
        )
        
    except Exception as e:
        logger.error(f"💥 Критическая ошибка: {e}", exc_info=True)
        sys.exit(1)

if __name__ == '__main__':
    main()
