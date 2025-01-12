from telegram import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from config import FILIALS

def main_menu_keyboard(is_admin=False):
    buttons = [
        [KeyboardButton("Daromad"), KeyboardButton("Xarajat")]
    ]
    if is_admin:
        buttons.append([KeyboardButton("Admin panel")])
    return ReplyKeyboardMarkup(buttons, resize_keyboard=True)

def back_keyboard():
    return ReplyKeyboardMarkup([[KeyboardButton("Orqaga")]], resize_keyboard=True)

def income_methods_keyboard():
    buttons = [
        [KeyboardButton("Naqt"), KeyboardButton("Humo")],
        [KeyboardButton("Uzcard"), KeyboardButton("Clic")],
        [KeyboardButton("Payme")],
        [KeyboardButton("Keyingi"), KeyboardButton("Orqaga")]
    ]
    return ReplyKeyboardMarkup(buttons, resize_keyboard=True)

def confirm_keyboard():
    buttons = [
        [KeyboardButton("Tasdiqlash"), KeyboardButton("Rad etish")],
        [KeyboardButton("Orqaga")]
    ]
    return ReplyKeyboardMarkup(buttons, resize_keyboard=True)

def expense_menu_keyboard():
    buttons = [
        [KeyboardButton("+"), KeyboardButton("Keyingi")],
        [KeyboardButton("Orqaga")]
    ]
    return ReplyKeyboardMarkup(buttons, resize_keyboard=True)

# keyboards.py

def admin_panel_keyboard():
    buttons = [
        [KeyboardButton("Daromad va xarajatlar"), KeyboardButton("Userlar")],
        [KeyboardButton("Malumotlar")],  # Changed from "Bugungi ma'lumotlar" to "Malumotlar"
        [KeyboardButton("Export")],
        [KeyboardButton("Orqaga")]
    ]
    return ReplyKeyboardMarkup(buttons, resize_keyboard=True)


def filial_inline_keyboard():
    inline_buttons = []
    row = []
    for f_id, f_name in FILIALS.items():
        row.append(InlineKeyboardButton(f_name, callback_data=f"filial_{f_id}"))
    inline_buttons.append(row)
    return InlineKeyboardMarkup(inline_buttons)

def period_select_keyboard():
    buttons = [
        [KeyboardButton("Bugungi"), KeyboardButton("Kechagi")],
        [KeyboardButton("1-Haftalik"), KeyboardButton("1-Oylik")],
        [KeyboardButton("Davrni tanlang (manual)")],
        [KeyboardButton("Orqaga")]
    ]
    return ReplyKeyboardMarkup(buttons, resize_keyboard=True)




def malumotlar_period_keyboard():
    buttons = [
        [KeyboardButton("Bugungi"), KeyboardButton("Kechagi")],
        [KeyboardButton("Orqaga")]
    ]
    return ReplyKeyboardMarkup(buttons, resize_keyboard=True)

# keyboards.py

from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def approval_inline_keyboard(rec_type, rec_id):
    buttons = [
        [
            InlineKeyboardButton("✅ Tasdiqlash", callback_data=f"{rec_type}_approve_{rec_id}"),
            InlineKeyboardButton("❌ Rad etish", callback_data=f"{rec_type}_reject_{rec_id}")
        ]
    ]
    return InlineKeyboardMarkup(buttons)


def export_inline_keyboard():
    inline_buttons = [
        [InlineKeyboardButton("PDF", callback_data="export_pdf")],
        [InlineKeyboardButton("Excel", callback_data="export_excel")]
    ]
    return InlineKeyboardMarkup(inline_buttons)
