# ======================================= Развлечения
import requests
import bs4  # BeautifulSoup4
from telebot import types
from io import BytesIO
import random


# -----------------------------------------------------------------------
def get_text_messages(bot, cur_user, message):
    chat_id = message.chat.id
    ms_text = message.text

    if ms_text == "Лиса для хорошего настроения)":
        bot.send_photo(chat_id, photo=get_catURL(), caption="держи лисичку, не грусти...")


    elif ms_text == "Факты о котиках":
        bot.send_message(chat_id, text=facts_cat())

    elif ms_text == "Факты о собаках":
        bot.send_message(chat_id, text=facts_dog())

    elif ms_text == "Факты о лисичках":
        bot.send_message(chat_id, text=facts_fox())


    elif ms_text == "Породы кошек":
        bot.send_message(chat_id, text=poroda())



# -----------------------------------------------------------------------

def poroda():
    array_cats = []
    req_poroda = requests.get('https://kotoholik.com/porody-koshek')
    soup = bs4.BeautifulSoup(req_poroda.text, "html.parser")
    result_find = soup.select('.entry-title')
    for result in result_find:
        array_cats.append(result.getText().strip())
        poroda = random.choice(array_cats)
    return poroda

# -----------------------------------------------------------------------
def facts_cat():
    file = open('коты.txt', 'r', encoding='UTF-8')
    fact = file.read().split('\n')
    file.close()
    return random.choice(fact)
def facts_dog():
    file = open('собаки.txt', 'r', encoding='UTF-8')
    fact = file.read().split('\n')
    file.close()
    return random.choice(fact)
def facts_fox():
    file = open('лисы.txt', 'r', encoding='UTF-8')
    fact = file.read().split('\n')
    file.close()
    return random.choice(fact)


# -----------------------------------------------------------------------
def get_catURL():
    url = ""
    req = requests.get('https://randomfox.ca/floof/')
    if req.status_code == 200:
        r_json = req.json()
        url = r_json['image']
        # url.split("/")[-1]
    return url