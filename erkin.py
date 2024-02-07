import telebot
from telebot.types import *
import sqlite3
import openai



bot = telebot.TeleBot("YOUR-TOKEN")

def get_db_connection():
    return sqlite3.connect("users.db")





def create_users_table():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            telegram_id INTEGER NOT NULL,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

create_users_table()





@bot.message_handler(commands=['start'])
def start_command(message): 
    markup = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    markup.add(telebot.types.KeyboardButton("Регистрация"), telebot.types.KeyboardButton("Логин"))
    markup.add(telebot.types.KeyboardButton("Контакты"), telebot.types.KeyboardButton("Ближащие аптеки", request_location=True))
    bot.send_message(message.chat.id, "Здравствуйте! Я health support бот.", reply_markup=markup)



@bot.message_handler(func=lambda message: message.text == "Регистрация")
def registration_button(message):
    bot.send_message(message.chat.id, "Пожалуйста, отправьте имя пользователя и пароль в формате: Логин пароль")
    bot.register_next_step_handler(message, handle_registration)

def handle_registration(message):
    text = message.text.strip().split(' ')
    if len(text) != 2:
        bot.send_message(message.chat.id, "Неверный формат. Пожалуйста, используйте формат: Логин пароль")
        return

    username = text[0]
    password = text[1]

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE username=?", (username,))
    if cursor.fetchone():
        bot.send_message(message.chat.id, "Пользователь с таким именем уже существует.")
    else:
        cursor.execute("INSERT INTO users (telegram_id, username, password) VALUES (?, ?, ?)",
                       (message.from_user.id, username, password))
        conn.commit()
        bot.send_message(message.chat.id, "Регистрация успешно завершена.")

    conn.close()


@bot.message_handler(func=lambda message: message.text == "Логин")
def login_button(message):
    bot.send_message(message.chat.id, "Пожалуйста, отправьте ваше имя пользователя и пароль в формате: Логин пароль")
    bot.register_next_step_handler(message, handle_login)

def handle_login(message):
    text = message.text.strip().split(' ')
    if len(text) != 2:
        bot.send_message(message.chat.id, "Неверный формат. Пожалуйста, используйте формат: Логин пароль")
        return

    username = text[0]
    password = text[1]

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    if cursor.fetchone():
        bot.send_message(message.chat.id, "Вход выполнен успешно.")
    else:
        bot.send_message(message.chat.id, "Неверное имя пользователя или пароль.")

    conn.close()





inmark= InlineKeyboardMarkup()
location_button1 = InlineKeyboardButton(text="ЦЕНТРАЛЬНАЯ АПТЕКА НГМК", callback_data="apteka1")
location_button2= InlineKeyboardButton(text="FAROVON-ZIYO-BARAKA", callback_data="apteka2")
location_button3 = InlineKeyboardButton(text="FRANGULA АПТЕКА", callback_data="apteka3")
location_button4 = InlineKeyboardButton(text="XUDDI KARIM", callback_data="apteka4")
location_button5 = InlineKeyboardButton(text="FITO FARM LEK", callback_data="apteka5")
inmark.add(location_button1).add(location_button2).add(location_button3).add(location_button4).add(location_button5)


@bot.message_handler(content_types=['location'])
def handle_location(message):
    bot.send_message(message.chat.id, "<b>Вот список ближащих аптек, выберите одну из них:</b>", parse_mode="HTML", reply_markup=inmark)




@bot.callback_query_handler(func=lambda call: call.data == "apteka1")
def send_location(call):
    bot.send_location(call.message.chat.id, 40.098647174837375, 65.37638762568365)  
    bot.send_message(call.message.chat.id, "<b>Название: ЦЕНТРАЛЬНАЯ АПТЕКА НГМК\nАдрес: Узбекистан, Навоийская область, Навои, ул. УЗБЕКИСТАНСКАЯ, 16\nТелефон: +998(36)223-29-42</b>",parse_mode="HTML")


@bot.callback_query_handler(func=lambda call: call.data == "apteka2")
def send_location(call):
    bot.send_location(call.message.chat.id, 40.10536832263608, 65.3815157842264)  
    bot.send_message(call.message.chat.id, "<b>Название: FAROVON-ZIYO-BARAKA\nАдрес: Узбекистан, Навоийская область, Навои, ул. ТОЛСТОГО, 1/30\nТелефон: +998(36)431-32-33</b>",parse_mode="HTML")


@bot.callback_query_handler(func=lambda call: call.data == "apteka3")
def send_location(call):
    bot.send_location(call.message.chat.id, 40.09047290714578, 65.37472127316738)
    bot.send_message(call.message.chat.id, "<b>Название: FRANGULA АПТЕКА\nАдрес: Узбекистан, Навоийская область, Навои, ул. НАВОИ, 52/111\nТелефон: +998(36)224-89-15</b>",parse_mode="HTML")


@bot.callback_query_handler(func=lambda call: call.data == "apteka4")
def send_location(call):
    bot.send_location(call.message.chat.id, 40.08759797799526, 65.37798567508442)
    bot.send_message(call.message.chat.id, "<b>Название: XUDDI KARIM\nАдрес: Узбекистан, Навоийская область, 210100, Навои, ул. АМИРА ТЕМУРА\nТелефон: +998(91)337-56-06</b>",parse_mode="HTML")


@bot.callback_query_handler(func=lambda call: call.data == "apteka5")
def send_location(call):
    bot.send_location(call.message.chat.id, 40.09338718733384, 65.38014578586724)  
    bot.send_message(call.message.chat.id, "<b>Название: FITO FARM LEK\nАдрес: Узбекистан, Навоийская область, 210100, Навои, ул. ХАЛКЛАР ДУСТЛИГИ, 7\nТелефон: +998(36)223-60-65</b>",parse_mode="HTML")


    



@bot.message_handler(func=lambda message: message.text == "Контакты")
def login_button(message):
    bot.send_contact(message.chat.id, phone_number="+998975544455", first_name="Стомотолог")
    bot.send_contact(message.chat.id, phone_number="+998959115522", first_name="Травматолог")
    bot.send_contact(message.chat.id, phone_number="+998787770303", first_name="Хирург")
    bot.send_contact(message.chat.id, phone_number="+998909713770", first_name="Кардиолог")
    bot.send_contact(message.chat.id, phone_number="+998712911866", first_name="Невропатолог")
    bot.send_contact(message.chat.id, phone_number="+998977714407", first_name="Аллерголог")
    bot.send_contact(message.chat.id, phone_number="+998712284885", first_name="Инфекционист")








openai.api_key="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"


@bot.message_handler()
def gpt(message):
    response = openai.Completion.create(
        engine="gpt-3.5-turbo-instruct",
        prompt=f"User: {message.text}\nBot: ",
        max_tokens=150,
        temperature=0.7,
        n=1,
        stop=None
    ).choices[0].text

    if len(response)>4096:
        bot.send_message(message.chat.id, response[:4096]+"...")
        bot.send_message(message.chat.id, response[4096:])
    else:
        bot.send_message(message.chat.id, response)



bot.polling(none_stop=True)