# main.py

import logging
from telegram.ext import (
    ApplicationBuilder,
    ConversationHandler,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters
)

from config import BOT_TOKEN, ADMIN_IDS
from database import create_tables, init_users
from states import State
from user_handlers import (
    start_command, main_menu_handler,
    income_select_method_handler, income_enter_amount_handler, income_check_confirm_handler,
    expense_enter_handler, expense_additional_handler, expense_enter_info_handler,
    expense_check_confirm_handler
)
from admin_handlers import (
    admin_menu_handler, admin_select_filial_callback,
    admin_select_period_handler, admin_enter_period_manual_handler,
    admin_callback_approval,
    admin_select_today_filial_callback, admin_today_view_handler,
    admin_export_filial_callback, admin_export_period_handler,
    admin_export_enter_period_manual_handler, export_format_callback,
    navigate_forward_handler, navigate_back_handler,
)

def main():
    # Initialize database va foydalanuvchilar
    create_tables()
    init_users()

    # Logging konfiguratsiyasi
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.WARNING  # Log darajasini WARNING ga o'rnating
    )
    logger = logging.getLogger(__name__)

    # httpx va telegram.ext loglarini suspen qilish
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("telegram").setLevel(logging.WARNING)
    logging.getLogger("telegram.ext").setLevel(logging.WARNING)

    # Bot ilovasini yaratish
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    # ConversationHandler ni aniqlash
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start_command)],
        states={

            # Asosiy menyu
            State.MAIN_MENU: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, main_menu_handler),
            ],
            # Daromadlarni boshqarish
            State.INCOME_SELECT_METHOD: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, income_select_method_handler),
            ],
            State.INCOME_ENTER_AMOUNT: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, income_enter_amount_handler),
            ],
            State.INCOME_CHECK_CONFIRM: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, income_check_confirm_handler),
            ],
            # Xarajatlarni boshqarish
            State.EXPENSE_ENTER: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, expense_enter_handler),
            ],
            State.EXPENSE_ADDITIONAL: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, expense_additional_handler),
            ],
            State.EXPENSE_ENTER_INFO: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, expense_enter_info_handler),
            ],
            State.EXPENSE_CHECK_CONFIRM: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, expense_check_confirm_handler),
            ],
            # Admin menyusi
            State.ADMIN_MENU: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, admin_menu_handler),
            ],
            # Admin filial tanlash
            State.ADMIN_SELECT_FILIAL: [
                CallbackQueryHandler(admin_select_filial_callback, pattern=r"filial_\d+"),
            ],
            # Admin davr tanlash
            State.ADMIN_SELECT_PERIOD: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, admin_select_period_handler),
            ],
            State.ADMIN_SELECT_CUSTOM_PERIOD: [  # Yangi qo'shilgan
                MessageHandler(filters.TEXT & ~filters.COMMAND, admin_select_period_handler),
            ],
            State.ADMIN_ENTER_PERIOD_MANUAL: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, admin_enter_period_manual_handler),
            ],
            # Admin hisobot ko'rish
            State.ADMIN_VIEW_REPORT: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, admin_menu_handler),
            ],
            # Foydalanuvchilarni boshqarish
            State.USER_MANAGEMENT: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, admin_menu_handler),
            ],
            # Admin bugungi ma'lumotlarni ko'rish
            State.ADMIN_TODAY_VIEW: [
                MessageHandler(filters.ALL, admin_today_view_handler),
            ],
            # Export qilish holatlari
            State.ADMIN_EXPORT_FILIAL: [
                CallbackQueryHandler(admin_export_filial_callback, pattern=r"filial_\d+"),
            ],
            State.ADMIN_EXPORT_PERIOD: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, admin_export_period_handler),
                MessageHandler(filters.TEXT & ~filters.COMMAND, admin_export_enter_period_manual_handler),
            ],
            State.ADMIN_EXPORT_FORMAT: [
                CallbackQueryHandler(export_format_callback, pattern=r"export_(pdf|excel)")
            ],
            # "Malumotlar" filial tanlash
            State.ADMIN_SELECT_TODAY_FILIAL: [
                CallbackQueryHandler(admin_select_today_filial_callback, pattern=r"filial_\d+"),
            ],
            # "Malumotlar" ma'lumotlarni navigatsiya qilish
            State.ADMIN_NAVIGATE_DATA: [
                CallbackQueryHandler(navigate_forward_handler, pattern=r"navigate_forward_\d+"),
                CallbackQueryHandler(navigate_back_handler, pattern=r"navigate_back_\d+"),
            ],
            # Yangi holat "Malumotlar" davr tanlash
            State.ADMIN_SELECT_TODAY_PERIOD: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, admin_select_period_handler),
            ],
        },
        fallbacks=[
            CommandHandler("start", start_command),
        ],
    )

    # ConversationHandler ni botga qo'shish
    application.add_handler(conv_handler)

    # Admin tasdiqlash callback handler
    application.add_handler(
        CallbackQueryHandler(
            admin_callback_approval,
            pattern=r"(income|expense)_(approve|reject)_\d+"
        )
    )

    # Botni ishga tushurish
    print("Bot ishga tushmoqda...")
    application.run_polling()

if __name__ == "__main__":
    main()
