# user_handlers.py

from datetime import datetime

from telegram import Update
from telegram.ext import ContextTypes

from config import FILIALS
from database import (
    get_user_by_telegram_id, get_income_by_user_and_date, create_income,
    confirm_income, get_expenses_by_user_and_date, create_expense,
    confirm_expense
)
from keyboards import (
    main_menu_keyboard, back_keyboard, income_methods_keyboard,
    confirm_keyboard, expense_menu_keyboard, admin_panel_keyboard
)
from states import State

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user = get_user_by_telegram_id(user_id)
    if not user:
        await update.message.reply_text("Siz ruxsat etilmagan foydalanuvchisiz. Admin bilan bog‘laning.")
        return State.START

    is_admin = (user[5] == 1)
    context.user_data["main_menu_keyboard"] = main_menu_keyboard(is_admin=is_admin)

    filial_id = user[2]
    filial_name = FILIALS.get(filial_id, "Noma’lum filial")

    text = f"Assalomu alaykum, {user[4]}!\n"
    text += f"Sizning filialingiz: {filial_name}\n"
    text += "Quyidagi menyudan foydalaning:"
    await update.message.reply_text(text, reply_markup=context.user_data["main_menu_keyboard"])
    return State.MAIN_MENU

async def main_menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    user_id = update.effective_user.id
    user = get_user_by_telegram_id(user_id)
    if not user:
        await update.message.reply_text("Siz ruxsat etilmagan foydalanuvchisiz. Admin bilan bog‘laning.")
        return State.START

    is_admin = (user[5] == 1)

    if text == "Daromad":
        today_str = datetime.now().strftime("%Y-%m-%d")
        row = get_income_by_user_and_date(user[0], today_str)
        if row:
            # Har qanday mavjud daromadni tekshirish
            await update.message.reply_text("Siz bugungi daromadni allaqachon yuborgansiz!",
                                            reply_markup=context.user_data["main_menu_keyboard"])
            return State.MAIN_MENU

        await update.message.reply_text(
            "Daromad turini tanlang (Naqt, Humo, Uzcard, Clic, Payme).",
            reply_markup=income_methods_keyboard()
        )
        return State.INCOME_SELECT_METHOD

    elif text == "Xarajat":
        today_str = datetime.now().strftime("%Y-%m-%d")
        existing_expenses = get_expenses_by_user_and_date(user[0], today_str)
        if existing_expenses:
            await update.message.reply_text("Siz bugungi xarajatni allaqachon yuborgansiz!",
                                            reply_markup=context.user_data["main_menu_keyboard"])
            return State.MAIN_MENU

        await update.message.reply_text(
            "Bugungi xarajatni kiriting (+ tugmasi bilan). Keyin 'Keyingi' bosiladi.",
            reply_markup=expense_menu_keyboard()
        )
        return State.EXPENSE_ENTER

    elif text == "Admin panel" and is_admin:
        await update.message.reply_text("Admin paneliga xush kelibsiz!",
                                        reply_markup=admin_panel_keyboard())
        return State.ADMIN_MENU

    else:
        await update.message.reply_text("Noma'lum buyruq.",
                                        reply_markup=context.user_data["main_menu_keyboard"])
        return State.MAIN_MENU

"""
DAROMAD
"""
async def income_select_method_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if "income_data" not in context.user_data:
        context.user_data["income_data"] = {
            "naqt": 0,
            "humo": 0,
            "uzkard": 0,
            "clic": 0,
            "payme": 0
        }

    if text == "Orqaga":
        await update.message.reply_text("Orqaga qaytdingiz",
                                        reply_markup=context.user_data["main_menu_keyboard"])
        return State.MAIN_MENU

    if text in ["Naqt", "Humo", "Uzcard", "Clic", "Payme"]:
        # Summani kiritish
        await update.message.reply_text(f"{text} summasini kiriting:", reply_markup=back_keyboard())
        # matndagi tur => dictionary dagi key
        map_key = text.lower() if text.lower() != "uzcard" else "uzkard"
        context.user_data["current_income_type"] = map_key
        return State.INCOME_ENTER_AMOUNT

    if text == "Keyingi":
        inc_data = context.user_data["income_data"]
        total_sum = sum(inc_data.values())
        if total_sum == 0:
            await update.message.reply_text("Hech narsa kiritilmadi. Daromad qo'shilmadi.",
                                            reply_markup=income_methods_keyboard())
            return State.INCOME_SELECT_METHOD
        msg = (
            "Kiritilgan daromad:\n"
            f"Naqt: {inc_data['naqt']}\n"
            f"Humo: {inc_data['humo']}\n"
            f"Uzcard: {inc_data['uzkard']}\n"
            f"Clic: {inc_data['clic']}\n"
            f"Payme: {inc_data['payme']}\n"
            f"Umumiy summa: {total_sum}\n"
            "Hammasi to'g'rimi?"
        )
        await update.message.reply_text(msg, reply_markup=confirm_keyboard())
        return State.INCOME_CHECK_CONFIRM

    await update.message.reply_text("Tugmalardan foydalaning.",
                                    reply_markup=income_methods_keyboard())
    return State.INCOME_SELECT_METHOD

async def income_enter_amount_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text == "Orqaga":
        await update.message.reply_text("Orqaga qaytdingiz",
                                        reply_markup=income_methods_keyboard())
        return State.INCOME_SELECT_METHOD

    try:
        amount = int(text)
        if amount < 0:
            raise ValueError
    except ValueError:
        await update.message.reply_text("Iltimos, musbat raqam kiriting!", reply_markup=back_keyboard())
        return State.INCOME_ENTER_AMOUNT

    inc_type = context.user_data.get("current_income_type", None)
    if inc_type:
        context.user_data["income_data"][inc_type] += amount
        await update.message.reply_text(f"{inc_type.capitalize()} summasi saqlandi.",
                                        reply_markup=income_methods_keyboard())
        # Debugging uchun print statement
        print(f"Income Data Updated: {context.user_data['income_data']}")
        return State.INCOME_SELECT_METHOD
    else:
        await update.message.reply_text("Xatolik yuz berdi. Orqaga qayting.",
                                        reply_markup=income_methods_keyboard())
        return State.INCOME_SELECT_METHOD

async def income_check_confirm_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text == "Orqaga":
        await update.message.reply_text("Orqaga qaytdingiz",
                                        reply_markup=income_methods_keyboard())
        return State.INCOME_SELECT_METHOD

    if text == "Tasdiqlash":
        user = get_user_by_telegram_id(update.effective_user.id)
        if not user:
            await update.message.reply_text("Siz ruxsat etilmagan foydalanuvchisiz.",
                                            reply_markup=main_menu_keyboard(is_admin=False))
            return State.START

        user_db_id = user[0]
        filial_id = user[2]
        today_str = datetime.now().strftime("%Y-%m-%d")

        row = get_income_by_user_and_date(user_db_id, today_str)
        if row:
            # Har qanday mavjud daromadni tekshirish
            await update.message.reply_text("Siz bugungi daromadni allaqachon yuborgansiz!",
                                            reply_markup=context.user_data["main_menu_keyboard"])
            return State.MAIN_MENU

        inc_data = context.user_data["income_data"]
        if sum(inc_data.values()) == 0:
            await update.message.reply_text("Hech qanday daromad kiritilmadi.",
                                            reply_markup=context.user_data["main_menu_keyboard"])
            return State.MAIN_MENU

        create_income(
            user_db_id, filial_id, today_str,
            inc_data["naqt"], inc_data["humo"], inc_data["uzkard"],
            inc_data["clic"], inc_data["payme"]
        )
        # User confirm
        confirm_income(user_db_id, today_str)

        context.user_data.pop("income_data", None)
        context.user_data.pop("current_income_type", None)

        await update.message.reply_text(
            "Bugungi daromadlaringiz muvaffaqiyatli yuborildi! Admin ko‘rib chiqadi.",
            reply_markup=context.user_data["main_menu_keyboard"]
        )
        return State.MAIN_MENU

    elif text == "Rad etish":
        # Optionally handle user rejection here if needed
        context.user_data.pop("income_data", None)
        context.user_data.pop("current_income_type", None)
        await update.message.reply_text(
            "Daromad yuborish bekor qilindi.",
            reply_markup=context.user_data["main_menu_keyboard"]
        )
        return State.MAIN_MENU

    await update.message.reply_text("Tasdiqlash yoki Rad etish.",
                                    reply_markup=confirm_keyboard())
    return State.INCOME_CHECK_CONFIRM

"""
XARAJAT
"""
async def expense_enter_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text == "Orqaga":
        await update.message.reply_text("Asosiy menyuga qaytdingiz",
                                        reply_markup=context.user_data["main_menu_keyboard"])
        return State.MAIN_MENU

    if text == "+":
        await update.message.reply_text("Xarajat summasini kiriting:", reply_markup=back_keyboard())
        return State.EXPENSE_ADDITIONAL

    if text == "Keyingi":
        exp_list = context.user_data.get("expense_list", [])
        if not exp_list:
            await update.message.reply_text("Hech narsa kiritilmadi.",
                                            reply_markup=expense_menu_keyboard())
            return State.EXPENSE_ENTER

        msg = "Kiritilgan xarajatlar:\n"
        total_sum = 0
        for idx, item in enumerate(exp_list, start=1):
            msg += f"{idx}) {item['info']} -- {item['summa']} so'm\n"
            total_sum += item['summa']
        msg += f"Umumiy summa: {total_sum}\n"
        msg += "Tasdiqlash yoki Rad etish?"
        await update.message.reply_text(msg, reply_markup=confirm_keyboard())
        return State.EXPENSE_CHECK_CONFIRM

    await update.message.reply_text("Tugmalardan foydalaning.",
                                    reply_markup=expense_menu_keyboard())
    return State.EXPENSE_ENTER

async def expense_additional_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text == "Orqaga":
        await update.message.reply_text("Orqaga qaytdingiz",
                                        reply_markup=expense_menu_keyboard())
        return State.EXPENSE_ENTER

    try:
        amount = int(text)
        if amount < 0:
            raise ValueError
    except ValueError:
        await update.message.reply_text("Iltimos, musbat raqam kiriting!", reply_markup=back_keyboard())
        return State.EXPENSE_ADDITIONAL

    context.user_data["current_expense_amount"] = amount
    await update.message.reply_text("Bu pul nimaga sarflandi?", reply_markup=back_keyboard())
    return State.EXPENSE_ENTER_INFO

async def expense_enter_info_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text == "Orqaga":
        await update.message.reply_text("Xarajat summasini kiriting:",
                                        reply_markup=back_keyboard())
        return State.EXPENSE_ADDITIONAL

    amount = context.user_data.get("current_expense_amount")
    if amount is None:
        await update.message.reply_text("Xatolik yuz berdi. Iltimos, xarajat summasini qayta kiriting.",
                                        reply_markup=expense_menu_keyboard())
        return State.EXPENSE_ENTER

    if "expense_list" not in context.user_data:
        context.user_data["expense_list"] = []
    context.user_data["expense_list"].append({"summa": amount, "info": text})

    context.user_data.pop("current_expense_amount", None)
    await update.message.reply_text(f"Xarajat qo'shildi: {text} -- {amount} so'm",
                                    reply_markup=expense_menu_keyboard())
    return State.EXPENSE_ENTER

async def expense_check_confirm_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text == "Orqaga":
        await update.message.reply_text("Orqaga qaytdingiz",
                                        reply_markup=expense_menu_keyboard())
        return State.EXPENSE_ENTER

    if text == "Tasdiqlash":
        user = get_user_by_telegram_id(update.effective_user.id)
        if not user:
            await update.message.reply_text("Siz ruxsat etilmagan foydalanuvchisiz.",
                                            reply_markup=main_menu_keyboard(is_admin=False))
            return State.START

        user_db_id = user[0]
        filial_id = user[2]
        date_str = datetime.now().strftime("%Y-%m-%d")

        existing_expenses = get_expenses_by_user_and_date(user_db_id, date_str)
        if existing_expenses:
            await update.message.reply_text("Siz bugungi xarajatni allaqachon yuborgansiz!",
                                            reply_markup=context.user_data["main_menu_keyboard"])
            return State.MAIN_MENU

        exp_list = context.user_data.get("expense_list", [])

        if not exp_list:
            await update.message.reply_text("Hech qanday xarajat kiritilmadi.",
                                            reply_markup=expense_menu_keyboard())
            return State.EXPENSE_ENTER

        for e in exp_list:
            create_expense(user_db_id, filial_id, date_str, e["summa"], e["info"])

        # Optionally, you can mark expenses as confirmed here if needed
        # But based on admin approval, confirmation happens

        context.user_data.pop("expense_list", None)

        await update.message.reply_text("Bugungi xarajatlaringiz yuborildi! Admin ko‘rib chiqadi.",
                                        reply_markup=context.user_data["main_menu_keyboard"])

        return State.MAIN_MENU

    elif text == "Rad etish":
        # Optionally handle user rejection here if needed
        context.user_data.pop("expense_list", None)
        await update.message.reply_text(
            "Xarajat yuborish bekor qilindi.",
            reply_markup=context.user_data["main_menu_keyboard"]
        )
        return State.MAIN_MENU

    await update.message.reply_text("Tasdiqlash yoki Rad etish.",
                                    reply_markup=confirm_keyboard())
    return State.EXPENSE_CHECK_CONFIRM
