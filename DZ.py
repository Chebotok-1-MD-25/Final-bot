
# -----------------------------------------------------------------------
def get_text_messages(bot, cur_user, message):
    chat_id = message.chat.id
    ms_text = message.text

    if ms_text == "Задание-1":
        dz1(bot, chat_id)

    elif ms_text == "Задание-2":
        dz2(bot, chat_id)

    elif ms_text == "Задание-3":
        dz3(bot, chat_id)

    elif ms_text == "Задание-4":
        dz4(bot, chat_id)

    elif ms_text == "Задание-5":
        dz5(bot, chat_id, message)

    elif ms_text == "Задание-6":
        dz6(bot, chat_id, message)

    elif ms_text == "Задание-7":
        dz7(bot, chat_id, message)

    elif ms_text == "Задание-8":
        dz8(bot, chat_id, message)

# -----------------------------------------------------------------------
def dz1(bot, chat_id):
    bot.send_message(chat_id, text="Привет, я Маша")
# -----------------------------------------------------------------------
def dz2(bot, chat_id):
    bot.send_message(chat_id, text="Мне 5")
# -----------------------------------------------------------------------
def dz3(bot, chat_id):
    bot.send_message(chat_id, text="Маша "*5)
# -----------------------------------------------------------------------
def dz4(bot, chat_id):
    dz4_ResponseHandler = lambda message: bot.send_message(chat_id, f"Привет, {message.text}! Мне моё имя нравится больше, но твоё тоже ничего)")
    my_input(bot, chat_id, "А как тебя зовут?", dz4_ResponseHandler)
# -----------------------------------------------------------------------
def dz5(bot, chat_id,message):
    bot.send_message(chat_id, 'Сколько тебе лет?')
    bot.register_next_step_handler(message, reg_age, bot)
# -----------------------------------------------------------------------
def dz6(bot, chat_id,message):
    bot.send_message(chat_id, 'Повтори своё имя')
    bot.register_next_step_handler(message, reg_name, bot)
# -----------------------------------------------------------------------
def dz7 (bot,chat_id,message):
    bot.send_message(chat_id, 'Я уже совсем забыла... Повтори-ка ещё разок своё имя')
    bot.register_next_step_handler(message, reg_name4, bot)
# -----------------------------------------------------------------------
def dz8 (bot,chat_id,message):
    bot.send_message(chat_id, "Помоги мне решить пример: 9 + (9 / 9) + (9 * 9) – 9")
    bot.register_next_step_handler(message, reg_ans, bot)
# -----------------------------------------------------------------------
# -----------------------------------------------------------------------
def reg_age(message,bot):
    global userage
    myage = 5
    userage = 0
    while userage == 0:
        try:
            userage = int(message.text)
        except Exception:
            bot.send_message(message.chat.id,"Возраст - это числа, а не буквы -__-")
            break
    if userage != 0:
        if (userage <= myage):
            bot.send_message(message.chat.id,"О, да ты совсем недавно родился...")
        elif userage > 150:
            bot.send_message(message.chat.id,"Треш...")
        else:
            bot.send_message(message.chat.id,"Вы мне в родители годитесь...\n")
# -----------------------------------------------------------------------
def reg_name(message,bot):
    global username
    username = message.text
    username = username[10::-1]
    bot.send_message(message.chat.id, "Твоё имя наоборот будет: "+' '+ username)
# -----------------------------------------------------------------------
def reg_name4(message,bot):
    global username1
    username1 = message.text

    bot.send_message(message.chat.id, 'Вот твоё имя-малыш: ' + username1.lower())
    bot.send_message(message.chat.id, 'А так будет, если кто-то на тебя очень сильно злится: ' + username1.upper())

# -----------------------------------------------------------------------
def reg_ans(message,bot):
    global ans
    ans = int(message.text)
    ans=0
    while ans == 0:
        try:
            ans = int(message.text)
        except Exception:
            bot.send_message(message.chat.id,"Здесь нужно вводить только числа")
            break
    if ans == 82:
        bot.send_message(message.chat.id,"Вау! Да ты гений! \n Спасибо!!!")
    else:
        bot.send_message(message.chat.id, "Мда.. плохой из тебя математик")
# -----------------------------------------------------------------------
# -----------------------------------------------------------------------
# -----------------------------------------------------------------------
def my_input(bot, chat_id, txt, ResponseHandler):
    message = bot.send_message(chat_id, text=txt)
    bot.register_next_step_handler(message, ResponseHandler)
# -----------------------------------------------------------------------
def my_inputInt(bot, chat_id, txt, ResponseHandler):

    # bot.send_message(chat_id, text=botGames.GameRPS_Multiplayer.name, reply_markup=types.ReplyKeyboardRemove())

    message = bot.send_message(chat_id, text=txt)
    bot.register_next_step_handler(message, my_inputInt_SecondPart, botQuestion=bot, txtQuestion=txt, ResponseHandler=ResponseHandler)
    # bot.register_next_step_handler(message, my_inputInt_return, bot, txt, ResponseHandler)  # то-же самое, но короче

def my_inputInt_SecondPart(message, botQuestion, txtQuestion, ResponseHandler):
    chat_id = message.chat.id
    try:
        if message.content_type != "text":
            raise ValueError
        var_int = int(message.text)
        # данные корректно преобразовались в int, можно вызвать обработчик ответа, и передать туда наше число
        ResponseHandler(botQuestion, chat_id, var_int)
    except ValueError:
        botQuestion.send_message(chat_id,
                         text="Можно вводить ТОЛЬКО целое число в десятичной системе исчисления (символами от 0 до 9)!\nПопробуйте еще раз...")
        my_inputInt(botQuestion, chat_id, txtQuestion, ResponseHandler)  # это не рекурсия, но очень похоже
        # у нас пара процедур, которые вызывают друг-друга, пока пользователь не введёт корректные данные,
        # и тогда этот цикл прервётся, и управление перейдёт "наружу", в ResponseHandler

# -----------------------------------------------------------------------
