import config
import telebot
import time
from telebot import types
from database import Database

from typing import final

db = Database('db.db')
bot = telebot.TeleBot(config.TOKEN)

#Рассылка
@bot.message_handler(commands=["spam"])
def spam(message):
    if (message.from_user.id == 345765593):
        user_mgs = message.text
        separating = user_mgs.split(maxsplit=1)
        users_spam= db.get_user()
        for i in users_spam:
            try:
                bot.send_message(i[1],separating[1])
            except:
                continue


@bot.message_handler(commands = ['check_all'])
def bot_message(message):
    if (message.from_user.id == 345765593):
       users = db.get_all_users()
    bot.send_message(message.chat.id, "Количество людей которые используют твоего бота = " + str(len(users)))

#Ссыки
@bot.message_handler(commands=['website'])
def open_website(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Вот это прикол ^*^", url="https://www.youtube.com/watch?v=WACsPXKOOTU"))
    bot.send_message(message.chat.id, "Отличный выбор, просто нажмите на кнопку ниже", parse_mode='html', reply_markup=markup)

@bot.message_handler(commands=['insta'])
def instagram(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Перейти в Инстаграм разработчика", url="https://instagram.com/x_denk?utm_medium=copy_link"))
    bot.send_message(message.chat.id, "Нажмите на кнопку ниже и подписывайтесь ^_^", parse_mode='html', reply_markup=markup)
#------------------------------------------


def main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
    item1 = types.KeyboardButton('👥 Поиск собеседника')
    item2 = types.KeyboardButton('Сменить пол👩‍👨')
    markup.add(item1, item2)
    return markup

def stop_dialog():
    markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
    item1 = types.KeyboardButton('🗣 Сказать свой профиль')
    item2 = types.KeyboardButton('/stop')
    markup.add(item1, item2)
    return markup

def stop_search():
    markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
    item1 = types.KeyboardButton('❌ Остановить поиск')
    markup.add(item1)
    return markup

@bot.message_handler(commands = ['start'])
def start(message):
    bot.send_message(message.chat.id, 'Привет, {0.first_name}! Добро пожаловать в анонимный чат! Укажите ваш пол! '.format(message.from_user), reply_markup = choose_gender(message))
#--------------------------------------------------
def choose_gender(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
    item1 = types.KeyboardButton('Я Парень 👨')
    item2 = types.KeyboardButton('Я Девушка 👩‍🦱')
    markup.add(item1, item2)
    return markup
#--------------------------------------------------

@bot.message_handler(commands = ['menu'])
def menu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
    item1 = types.KeyboardButton('👥 Поиск собеседника')
    item2 = types.KeyboardButton('Сменить пол👩‍👨')
    markup.add(item1, item2)

    bot.send_message(message.chat.id, '📝 Меню'.format(message.from_user), reply_markup = markup)

@bot.message_handler(commands = ['stop'])
def stop(message):
    chat_info = db.get_active_chat(message.chat.id)
    if chat_info != False:
        db.delete_chat(chat_info[0])
        markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
        item1 = types.KeyboardButton('✏️ Следующий диалог')
        item2 = types.KeyboardButton('/menu')
        markup.add(item1, item2)

        bot.send_message(chat_info[1], '❌ Собеседник покинул чат', reply_markup = markup)
        bot.send_message(message.chat.id, '❌ Вы вышли из чата', reply_markup = markup)
    else:
        bot.send_message(message.chat.id, '❌ Вы не начали чат!', reply_markup = markup)


@bot.message_handler(content_types = ['text'])
def bot_message(message):
    if message.chat.type == 'private':
        if message.text == '👥 Поиск собеседника' or message.text == '✏️ Следующий диалог':
            markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
            item1 = types.KeyboardButton('🔎 Парень')
            item2 = types.KeyboardButton('🔎 Девушка')
            item3 = types.KeyboardButton('👩‍👨 Рандом')
            markup.add(item1, item2, item3)

            bot.send_message(message.chat.id, 'Кого искать?', reply_markup = markup)
#-------------------------------------------------------------------------------
        elif message.text == 'Сменить пол👩‍👨':
            bot.send_message(message.chat.id, '👍 Теперь вы можете изменить свой пол', reply_markup = choose_gender(message))
#--------------------------------------------------------------------------------            
        elif message.text == '❌ Остановить поиск':
            db.delete_queue(message.chat.id)
            bot.send_message(message.chat.id, '❌ Поиск остановлен, напишите /menu', reply_markup = main_menu())

        
        elif message.text == '🔎 Парень':
            user_info = db.get_gender_chat('male')
            chat_two = user_info[0]
            if db.create_chat(message.chat.id, chat_two) == False:
                db.add_queue(message.chat.id, db.get_gender(message.chat.id))
                bot.send_message(message.chat.id, '👻 Поиск собеседника', reply_markup = stop_search())
            else:
                mess = 'Собеседник найден! Чтобы остановить диалог, напишите /stop'

                bot.send_message(message.chat.id, mess, reply_markup = stop_dialog())
                bot.send_message(chat_two, mess, reply_markup = stop_dialog())
        
        
        elif message.text == '🔎 Девушка':
            user_info = db.get_gender_chat('female')
            chat_two = user_info[0]
            if db.create_chat(message.chat.id, chat_two) == False:
                db.add_queue(message.chat.id, db.get_gender(message.chat.id))
                bot.send_message(message.chat.id, '👻 Поиск собеседника', reply_markup = stop_search())
            else:
                mess = 'Собеседник найден! Чтобы остановить диалог, напишите /stop'

                bot.send_message(message.chat.id, mess, reply_markup = stop_dialog())
                bot.send_message(chat_two, mess, reply_markup = stop_dialog())
        

        elif message.text == '👩‍👨 Рандом':
            user_info = db.get_chat()
            chat_two = user_info[0]

            if db.create_chat(message.chat.id, chat_two) == False:
                db.add_queue(message.chat.id, db.get_gender(message.chat.id))
                bot.send_message(message.chat.id, '👻 Поиск собеседника', reply_markup = stop_search())
            else:
                mess = 'Собеседник найден! Чтобы остановить диалог, напишите /stop'

                bot.send_message(message.chat.id, mess, reply_markup = stop_dialog())
                bot.send_message(chat_two, mess, reply_markup = stop_dialog())
        
        elif message.text == '🗣 Сказать свой профиль':
            chat_info = db.get_active_chat(message.chat.id)
            if chat_info != False:
                if message.from_user.username:
                    bot.send_message(chat_info[1], '@' + message.from_user.username)
                    bot.send_message(message.chat.id, '🗣 Вы сказали свой профиль')
                else:
                    bot.send_message(message.chat.id, '❌ В вашем аккаунте не указан username')
            else:
                bot.send_message(message.chat.id, '❌ Вы не начали диалог!')

        

        elif message.text == 'Я Парень 👨':
            if db.set_gender(message.chat.id, 'male'):
                bot.send_message(message.chat.id, '✅ Ваш пол успешно добавлен!', reply_markup = main_menu())
            else:
                bot.send_message(message.chat.id,'Ваш пол успешно выбран 😋', reply_markup = main_menu())
        
        elif message.text == 'Я Девушка 👩‍🦱':
            if db.set_gender(message.chat.id, 'female'):
                bot.send_message(message.chat.id, '✅ Ваш пол успешно добавлен!', reply_markup = main_menu())
            else:
                bot.send_message(message.chat.id,'Ваш пол успешно выбран 😋', reply_markup = main_menu())
        
        else:
            if db.get_active_chat(message.chat.id) != False:
                chat_info = db.get_active_chat(message.chat.id)
                bot.send_message(chat_info[1], message.text)
            else:
                bot.send_message(message.chat.id, '❌ Вы не начали диалог!')


@bot.message_handler(content_types='stickers')
def bot_stickers(message):
    if message.chat.type == 'private':
        chat_info = db.get_active_chat(message.chat.id)
        if chat_info != False:
            bot.send_sticker(chat_info[1], message.sticker.file_id)
        else:
            bot.send_message(message.chat.id, '❌ Вы не начали диалог!')

@bot.message_handler(content_types='voice')
def bot_voice(message):
    if message.chat.type == 'private':
        chat_info = db.get_active_chat(message.chat.id)
        if chat_info != False:
            bot.send_voice(chat_info[1], message.voice.file_id)
        else:
            bot.send_message(message.chat.id, '❌ Вы не начали диалог!')

@bot.message_handler(content_types='video')
def bot_video(message):
    if message.chat.type == 'private':
        chat_info = db.get_active_chat(message.chat.id)
        if chat_info != False:
            bot.send_video(chat_info[1], message.video.file_id)
        else:
            bot.send_message(message.chat.id, '❌ Вы не начали диалог!')

@bot.message_handler(content_types='video_note')
def bot_video_note(message):
    if message.chat.type == 'private':
        chat_info = db.get_active_chat(message.chat.id)
        if chat_info != False:
            bot.send_video_note(chat_info[1], message.video_note.file_id)
        else:
            bot.send_message(message.chat.id, '❌ Вы не начали диалог!')

@bot.message_handler(content_types='photo')
def bot_photo(message):
    if message.chat.type == 'private':
        chat_info = db.get_active_chat(message.chat.id)
        if chat_info != False:
            bot.send_photo(chat_info[1], message.photo[2].file_id)
        else:
            bot.send_message(message.chat.id, '❌ Вы не начали диалог!')



bot.polling(none_stop = True)