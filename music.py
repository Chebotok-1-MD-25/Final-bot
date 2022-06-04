
def get_text_messages(bot, cur_user, message):
    chat_id = message.chat.id
    ms_text = message.text


    if ms_text == "Ssshhhiiittt!!!":
        shit(bot, message)

    elif ms_text == "Нервы":
        nerv(bot, message)

    elif ms_text == "Кис-Кис":
        kis(bot, message)


# ---------------------------------------------------------------------
def shit(bot, message):
    file1 = open('секонд.mp3', 'rb')
    bot.send_document(message.chat.id, file1)
    file2 = open('танцы.mp3', 'rb')
    bot.send_document(message.chat.id, file2)
    file3 = open('солнце.mp3', 'rb')
    bot.send_document(message.chat.id, file3)

# -----------------------------------------------------------------------
def nerv(bot, message):
    file1 = open('друг.mp3', 'rb')
    file2 = open('счастье.mp3', 'rb')
    file3 = open('на вынос.mp3', 'rb')
    bot.send_document(message.chat.id, file1)
    bot.send_document(message.chat.id, file2)
    bot.send_document(message.chat.id, file3)

# -----------------------------------------------------------------------
def kis(bot, message):
    file1 = open('весна.mp3', 'rb')
    bot.send_document(message.chat.id, file1)
    file2 = open('лбтд.mp3', 'rb')
    bot.send_document(message.chat.id, file2)
    file3 = open('бывший.mp3', 'rb')
    bot.send_document(message.chat.id, file3)
