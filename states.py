# states.py

from enum import Enum, auto

class State(Enum):
    MAIN_MENU = auto()

    # Daromad
    INCOME_SELECT_METHOD = auto()
    INCOME_ENTER_AMOUNT = auto()
    INCOME_CHECK_CONFIRM = auto()

    # Xarajat
    EXPENSE_ENTER = auto()
    EXPENSE_ADDITIONAL = auto()
    EXPENSE_ENTER_INFO = auto()
    EXPENSE_CHECK_CONFIRM = auto()

    # Admin
    ADMIN_MENU = auto()
    ADMIN_SELECT_FILIAL = auto()
    ADMIN_SELECT_PERIOD = auto()
    ADMIN_ENTER_PERIOD_MANUAL = auto()
    ADMIN_VIEW_REPORT = auto()

    USER_MANAGEMENT = auto()
    USER_MANAGEMENT_EDIT = auto()
    USER_MANAGEMENT_ADD = auto()
    USER_MANAGEMENT_DELETE = auto()

    ADMIN_TODAY_VIEW = auto()

    # Export States
    ADMIN_EXPORT_FILIAL = auto()
    ADMIN_EXPORT_PERIOD = auto()
    ADMIN_EXPORT_FORMAT = auto()

    # New States for "Malumotlar" Navigation
    ADMIN_SELECT_TODAY_FILIAL = auto()
    ADMIN_SELECT_TODAY_PERIOD = auto()
    ADMIN_NAVIGATE_DATA = auto()
    ADMIN_SELECT_CUSTOM_PERIOD = auto()
