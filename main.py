# main.py - УНИВЕРСАЛЬНЫЙ ДЛЯ ЛЮБОЙ ВЕРСИИ
import sys
import os

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

import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    try:
        print("=" * 60)
        print("🚀 ТЕЛЕГРАМ БОТ ДЛЯ БАРБЕРШОПА")
        print("=" * 60)
        
        # 1. Определяем версию
        logger.info("🔍 Определяем версию python-telegram-bot...")
        try:
            import pkg_resources
            ptb_version = pkg_resources.get_distribution("python-telegram-bot").version
            logger.info(f"📦 Версия: {ptb_version}")
            
            if ptb_version.startswith("13."):
                VERSION_13 = True
                logger.info("⚙️ Определено: версия 13.x")
            elif ptb_version.startswith("20."):
                VERSION_13 = False
                logger.info("⚙️ Определено: версия 20.x")
            else:
                logger.warning(f"⚠️ Неизвестная версия: {ptb_version}")
                # Предполагаем версию 20.x как современную
                VERSION_13 = False
        except:
            logger.warning("⚠️ Не удалось определить версию, предполагаем 20.x")
            VERSION_13 = False
        
        # 2. Загружаем config
        from config import BOT_TOKEN, ADMINS
        logger.info(f"✅ Токен: {'установлен' if BOT_TOKEN else 'НЕТ!'}")
        
        if not BOT_TOKEN:
            logger.error("❌ BOT_TOKEN не установлен!")
            return
        
        # 3. Инициализация базы
        from database import init_db
        init_db()
        logger.info("✅ База данных инициализирована")
        
        # 4. Импортируем обработчики
        from bot.handlers import start, admin_command, contact_handler, button_handler, text_handler
        
        if VERSION_13:
            # ========== ВЕРСИЯ 13.15 ==========
            logger.info("🤖 Создаем Updater (версия 13.x)...")
            from telegram import Updater
            from telegram.ext import CommandHandler, CallbackQueryHandler, MessageHandler, Filters
            
            updater = Updater(token=BOT_TOKEN, use_context=True)
            dp = updater.dispatcher
            
            # Передаем updater для уведомлений
            set_application(updater)
            
            # Добавляем обработчики
            dp.add_handler(CommandHandler("start", start))
            dp.add_handler(CommandHandler("admin", admin_command))
            dp.add_handler(MessageHandler(Filters.contact, contact_handler))
            dp.add_handler(MessageHandler(Filters.text & Filters.private, text_handler))
            dp.add_handler(CallbackQueryHandler(button_handler))
            
            logger.info("✅ Все обработчики добавлены")
            logger.info("▶️ Запускаем бота (версия 13.x)...")
            
            updater.start_polling()
            updater.idle()
            
        else:
            # ========== ВЕРСИЯ 20.7+ ==========
            logger.info("🤖 Создаем Application (версия 20.x)...")
            from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters
            
            application = Application.builder().token(BOT_TOKEN).build()
            
            # Передаем application для уведомлений
            set_application(application)
            
            # Добавляем обработчики
            application.add_handler(CommandHandler("start", start))
            application.add_handler(CommandHandler("admin", admin_command))
            application.add_handler(MessageHandler(filters.CONTACT, contact_handler))
            application.add_handler(MessageHandler(filters.TEXT & filters.ChatType.PRIVATE, text_handler))
            application.add_handler(CallbackQueryHandler(button_handler))
            
            logger.info("✅ Все обработчики добавлены")
            logger.info("▶️ Запускаем бота (версия 20.x)...")
            
            application.run_polling(drop_pending_updates=True)
        
    except Exception as e:
        logger.error(f"💥 КРИТИЧЕСКАЯ ОШИБКА: {e}", exc_info=True)
        import traceback
        logger.error(traceback.format_exc())
        sys.exit(1)

if __name__ == '__main__':
    main()
