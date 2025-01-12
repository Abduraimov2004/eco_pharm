# database.py

import sqlite3
from config import DATABASE_NAME, ADMIN_IDS, USERS

def create_tables():
    """
    Initialize database tables.
    """
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    # Users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            telegram_id INTEGER UNIQUE,
            filial_id INTEGER,
            username TEXT,
            full_name TEXT,
            is_admin INTEGER DEFAULT 0
        )
    """)

    # Incomes table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS incomes(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            filial_id INTEGER,
            date_kiritilgan TEXT,
            naqt INTEGER DEFAULT 0,
            humo INTEGER DEFAULT 0,
            uzkard INTEGER DEFAULT 0,
            clic INTEGER DEFAULT 0,
            payme INTEGER DEFAULT 0,
            confirm_status INTEGER DEFAULT 0, -- User confirmed
            admin_approval INTEGER DEFAULT 0  -- Admin approval status
        )
    """)

    # Expenses table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            filial_id INTEGER,
            date_kiritilgan TEXT,
            summa INTEGER,
            info TEXT,
            confirm_status INTEGER DEFAULT 0, -- User confirmed
            admin_approval INTEGER DEFAULT 0  -- Admin approval status
        )
    """)

    conn.commit()
    conn.close()

def get_connection():
    return sqlite3.connect(DATABASE_NAME)

# --- User Operations ---

def create_user(telegram_id, filial_id, username, full_name, is_admin=0):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO users(telegram_id, filial_id, username, full_name, is_admin)
            VALUES (?, ?, ?, ?, ?)
        """, (telegram_id, filial_id, username, full_name, is_admin))
        conn.commit()
    except sqlite3.IntegrityError:
        pass  # User already exists
    finally:
        conn.close()

def get_user_by_telegram_id(tg_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE telegram_id=?", (tg_id,))
    row = cursor.fetchone()
    conn.close()
    return row

def get_user_by_id(user_id):
    """
    Foydalanuvchini ichki ID orqali olish.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id=?", (user_id,))
    row = cursor.fetchone()
    conn.close()
    return row

def get_all_users():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()
    conn.close()
    return rows

# --- Income Operations ---

def get_income_by_user_and_date(user_id, date_str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM incomes
        WHERE user_id=? AND date_kiritilgan=?
    """, (user_id, date_str))
    rows = cursor.fetchall()
    conn.close()
    return rows  # Endi bitta row emas, barcha row larni qaytaradi

def create_income(user_id, filial_id, date_str, naqt, humo, uzkard, clic, payme):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO incomes(user_id, filial_id, date_kiritilgan,
                            naqt, humo, uzkard, clic, payme,
                            confirm_status, admin_approval)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, 0, 0)
    """, (user_id, filial_id, date_str, naqt, humo, uzkard, clic, payme))
    conn.commit()
    conn.close()

def confirm_income(user_id, date_str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE incomes
        SET confirm_status=1
        WHERE user_id=? AND date_kiritilgan=?
    """, (user_id, date_str))
    conn.commit()
    conn.close()

def admin_approve_income(income_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE incomes
        SET admin_approval=1
        WHERE id=?
    """, (income_id,))
    conn.commit()
    conn.close()

def admin_reject_income(income_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE incomes
        SET admin_approval=2
        WHERE id=?
    """, (income_id,))
    conn.commit()
    conn.close()

def delete_income(income_id):
    """
    Daromadni ID orqali o'chirish.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM incomes WHERE id=?", (income_id,))
    conn.commit()
    conn.close()

def get_incomes_by_filial_and_period(filial_id, start_date, end_date):
    conn = get_connection()
    cursor = conn.cursor()
    if filial_id:
        cursor.execute("""
            SELECT * FROM incomes
            WHERE filial_id=?
              AND date_kiritilgan BETWEEN ? AND ?
        """, (filial_id, start_date, end_date))
    else:
        # Agar filial_id=None bo'lsa, barcha filials uchun
        cursor.execute("""
            SELECT * FROM incomes
            WHERE date_kiritilgan BETWEEN ? AND ?
        """, (start_date, end_date))
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_income_by_id(income_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM incomes WHERE id=?", (income_id,))
    row = cursor.fetchone()
    conn.close()
    return row

# --- Expense Operations ---

def get_expenses_by_user_and_date(user_id, date_str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM expenses
        WHERE user_id=? AND date_kiritilgan=?
    """, (user_id, date_str))
    rows = cursor.fetchall()
    conn.close()
    return rows

def create_expense(user_id, filial_id, date_str, summa, info):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO expenses(user_id, filial_id, date_kiritilgan,
                             summa, info, confirm_status, admin_approval)
        VALUES (?, ?, ?, ?, ?, 1, 0)
    """, (user_id, filial_id, date_str, summa, info))  # confirm_status=1
    conn.commit()
    conn.close()

def confirm_expense(expense_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE expenses
        SET confirm_status=1
        WHERE id=?
    """, (expense_id,))
    conn.commit()
    conn.close()

def admin_approve_expense(exp_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE expenses
        SET admin_approval=1
        WHERE id=?
    """, (exp_id,))
    conn.commit()
    conn.close()

def admin_reject_expense(exp_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE expenses
        SET admin_approval=2
        WHERE id=?
    """, (exp_id,))
    conn.commit()
    conn.close()

def delete_expense(exp_id):
    """
    Xarajatni ID orqali o'chirish.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM expenses WHERE id=?", (exp_id,))
    conn.commit()
    conn.close()

def get_expenses_by_filial_and_period(filial_id, start_date, end_date):
    conn = get_connection()
    cursor = conn.cursor()
    if filial_id:
        cursor.execute("""
            SELECT * FROM expenses
            WHERE filial_id=?
              AND date_kiritilgan BETWEEN ? AND ?
        """, (filial_id, start_date, end_date))
    else:
        # Agar filial_id=None bo'lsa, barcha filials uchun
        cursor.execute("""
            SELECT * FROM expenses
            WHERE date_kiritilgan BETWEEN ? AND ?
        """, (start_date, end_date))
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_expense_by_id(exp_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM expenses WHERE id=?", (exp_id,))
    row = cursor.fetchone()
    conn.close()
    return row

# --- Initialization ---

def init_users():
    """
    Insert initial users (Admin + 5 users).
    """
    conn = get_connection()
    cursor = conn.cursor()

    # Admin users
    for admin_id in ADMIN_IDS:
        cursor.execute("SELECT * FROM users WHERE telegram_id=?", (admin_id,))
        admin_row = cursor.fetchone()
        if not admin_row:
            create_user(admin_id, 1, "admin_user", "Admin FullName", is_admin=1)

    # Regular users
    for tg_id, fil_id in USERS.items():
        cursor.execute("SELECT * FROM users WHERE telegram_id=?", (tg_id,))
        row = cursor.fetchone()
        if not row:
            create_user(tg_id, fil_id, f"user_{tg_id}", f"User {tg_id}", is_admin=0)

    conn.close()
