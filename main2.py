# Телеграм-бот v.004
import telebot  # pyTelegramBotAPI 4.3.1
from telebot import types
import botGames
import menuBot
from menuBot import Menu
import requests
import bs4
from mg import get_map_cell
import DZ
import cats

import music




bot = telebot.TeleBot('5207343139:AAH41gyhjwZMb97KtPFQ2hMk8Fo_5EFfgvY')

# -----------------------------------------------------------------------
# Функция, обрабатывающая команды
@bot.message_handler(commands="start")
def command(message):
    chat_id = message.chat.id
    bot.send_sticker(chat_id, "CAACAgIAAxkBAAI6OmKCdeW-deMX2A9_sm3va2byLCVlAAJ9GAACHB05SpAfprNoMQNzJAQ")
    txt_message = f"Привет, {message.from_user.first_name}! Я тестовый бот для курса программирования на языке Python"
    bot.send_message(chat_id, text=txt_message, reply_markup=Menu.getMenu(chat_id, "Главное меню").markup)


#@bot.message_handler(commands="play")
#def start_menu_2(message):
    #main_.start_menu(message)



# -----------------------------------------------------------------------

cols, rows = 8, 8
maps = {}

keyboard = telebot.types.InlineKeyboardMarkup()
keyboard.row(telebot.types.InlineKeyboardButton('⇦', callback_data='left'),
             telebot.types.InlineKeyboardButton('⇧', callback_data='up'),
             telebot.types.InlineKeyboardButton('⇩', callback_data='down'),
             telebot.types.InlineKeyboardButton('⇨', callback_data='right'))

def get_map_str(map_cell, player):
    map_str = ""
    for y in range(rows * 2 - 1):
        for x in range(cols * 2 - 1):
            if map_cell[x + y * (cols * 2 - 1)]:
                map_str += "⬛"
            elif (x, y) == player:
                map_str += "🍓"
            else:
                map_str += "⬜"
        map_str += "\n"
    return map_str

@bot.message_handler(commands=['labirint'])
def play_message(message):
    map_cell = get_map_cell(cols, rows)

    user_data = {
        'map': map_cell,
        'x': 0,
        'y': 0
    }

    maps[message.chat.id] = user_data

    bot.send_message(message.from_user.id, get_map_str(map_cell, (0, 0)), reply_markup=keyboard)


#@bot.callback_query_handler(func=lambda call: True)
#def call_back(call):
#    button_list[call.data](call)

@bot.callback_query_handler(func=lambda call: True)
def callback_func(query):
     user_data = maps[query.message.chat.id]
     new_x, new_y = user_data['x'], user_data['y']

     if query.data == 'left':
         new_x -= 1
     if query.data == 'right':
         new_x += 1
     if query.data == 'up':
         new_y -= 1
     if query.data == 'down':
         new_y += 1

     if new_x < 0 or new_x > 2 * cols - 2 or new_y < 0 or new_y > rows * 2 - 2:
         return None
     if user_data['map'][new_x + new_y * (cols * 2 - 1)]:
         return None

     user_data['x'], user_data['y'] = new_x, new_y

     if new_x == cols * 2 - 2 and new_y == rows * 2 - 2:
         bot.edit_message_text(chat_id=query.message.chat.id,
                               message_id=query.message.id,
                               text="Ура ура, победа!")
         return None

     bot.edit_message_text(chat_id=query.message.chat.id,
                           message_id=query.message.id,
                           text=get_map_str(user_data['map'], (new_x, new_y)),
                           reply_markup=keyboard)


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    chat_id = message.chat.id
    ms_text = message.text

    cur_user = menuBot.Users.getUser(chat_id)
    if cur_user is None:
        cur_user = menuBot.Users(chat_id, message.json["from"])


    # проверка = мы нажали кнопку подменю, или кнопку действия
    subMenu = menuBot.goto_menu(bot, chat_id, ms_text)  # попытаемся использовать текст как команду меню, и войти в него
    if subMenu is not None:
        # Проверим, нет ли обработчика для самого меню. Если есть - выполним нужные команды
        if subMenu.name == "Игра в 21":
            game21 = botGames.newGame(chat_id, botGames.Game21(jokers_enabled=True))  # создаём новый экземпляр игры
            text_game = game21.get_cards(2)  # просим 2 карты в начале игры
            bot.send_media_group(chat_id, media=game21.mediaCards)  # получим и отправим изображения карт
            bot.send_message(chat_id, text=text_game)

        elif subMenu.name == "Игра КНБ":
            gameRPS = botGames.newGame(chat_id, botGames.GameRPS())  # создаём новый экземпляр игры и регистрируем его
            bot.send_photo(chat_id, photo=gameRPS.url_picRules, caption=gameRPS.text_rules, parse_mode='HTML')

        return  # мы вошли в подменю, и дальнейшая обработка не требуется

    cur_menu = Menu.getCurMenu(chat_id)
    if cur_menu is not None and ms_text in cur_menu.buttons:  # проверим, что команда относится к текущему меню
        module = cur_menu.module

        if module != "":  # проверим, есть ли обработчик для этого пункта меню в другом модуле, если да - вызовем его (принцип инкапсуляции)
            exec(module + ".get_text_messages(bot, cur_user, message)")

        if ms_text == "Помощь🙏":
            send_help(bot, chat_id)

        elif ms_text == "Погода🌧":
            bot.send_message(chat_id, text=pogoda(chat_id))

        elif ms_text == "Лабиринт":
            bot.send_message(chat_id, text="Для начала игры нажмите: /labirint")


    else:  # ======================================= случайный текст
        bot.send_message(chat_id, text="Мне жаль, я не понимаю вашу команду: " + ms_text)
        menuBot.goto_menu(bot, chat_id, "Главное меню")


# -----------------------------------------------------------------------

# -----------------------------------------------------------------------
def send_help(bot, chat_id):
    bot.send_message(chat_id, "Автор: Маша Чеботок")
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text = "Кто напишет, тот Сергей", url = "https://t.me/Chhebott")
    markup.add(btn1)
    img = open('кот.jpg', 'rb')

    bot.send_photo(chat_id, img, reply_markup=markup)

    bot.send_message(chat_id, "Активные пользователи чат-бота:")
    for el in menuBot.Users.activeUsers:
        bot.send_message(chat_id, menuBot.Users.activeUsers[el].getUserHTML(), parse_mode='HTML')

def pogoda(chat_id):
    req = requests.get('https://pogoda.mail.ru/prognoz/sankt_peterburg/')
    html = bs4.BeautifulSoup(req.content, "html.parser")
    answer = str(html.select('.information__content__temperature'))
    temp = answer.split("/span>")
    temp2 = temp[1].strip()
    temp2 = temp2[0:3]
    st_temp = "Сегодня погода в Санкт-Петербурге: " + temp2
    return st_temp





bot.polling(none_stop=True, interval=0)  # Запускаем бота
