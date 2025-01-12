
import os
from dotenv import load_dotenv
load_dotenv()
BOT_TOKEN =os.getenv("BOT_TOKEN") # BotFatherdan olingan tokenni shu yerga yozasiz


ADMIN_IDS = [1753386725]  # Admin telegram_id (o'zingizning real ID'niz)

FILIALS = {
    1: "Filial-1",
    2: "Filial-2",
    3: "Filial-3",
    4: "Filial-4",
    5: "Filial-5",
}

USERS = {
    6279470162: 1,  # 1- user -> Filial-1
    111111002: 2,  # 2- user -> Filial-2
    111111003: 3,  # 3- user -> Filial-3
    111111004: 4,  # 4- user -> Filial-4
    111111005: 5,  # 5- user -> Filial-5
}

DATABASE_NAME = "ohhiri2.db"

