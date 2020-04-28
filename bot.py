"""
    Bot created for searching and getting updates about last-minute tours
    Works with PyTelegramBotApi, sqlite3
    Created by https://github.com/Polar1ty
"""

import config
import telebot
import datetime
import sqlite3 as sql
import dbworker
from telebot import types
import time
import inline_calendar
import random
from selenium import webdriver


# connection = sql.connect('DATABASE.sqlite')
# q = connection.cursor()
# q.execute('''
# 			CREATE TABLE "user" (
# 				'id' TEXT,
# 				'surname' TEXT,
# 				'name' TEXT,
# 				'date_of_birth' TEXT,
# 				'address' TEXT,
# 				'email' TEXT,
# 				'phone' TEXT
# 			)''')
# connection.commit()
# q.close()
# connection.close()

def log(message):
    """ Logging user messages """
    print("<!--------------------------------!>")
    print(datetime.datetime.now())
    print("Сообщение от {0} {1} (id = {2}) \n {3}".format(message.from_user.first_name,
                                                          message.from_user.last_name,
                                                          str(message.from_user.id), message.text))


def ask_from(message):
    button1 = types.KeyboardButton('🇺🇦Київ')
    button2 = types.KeyboardButton('🇺🇦Запоріжжя')
    button3 = types.KeyboardButton('🇺🇦Львів')
    button4 = types.KeyboardButton('🇺🇦Одесса')
    button5 = types.KeyboardButton('🇺🇦Харків')
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=2)
    markup.add(button1, button2, button3, button4, button5)
    bot.send_message(message.chat.id, 'Гарний вибір! Оберіть місто виліту:', reply_markup=markup)


def ask_when(message):
    bot.send_message(message.chat.id,
                     f'Теперь скажіть будь ласка бажану дату виліту📅')
    inline_calendar.init(message.chat.id,
                         datetime.date.today(),
                         datetime.date.today(),
                         datetime.date.today() + datetime.timedelta(days=365))
    bot.send_message(message.chat.id, text='Обрана дата: ',
                     reply_markup=inline_calendar.get_keyboard(message.chat.id))


def count_of_child(message):
    button1 = types.KeyboardButton('👶')
    button2 = types.KeyboardButton('👶👶')
    button3 = types.KeyboardButton('👶👶👶')
    button4 = types.KeyboardButton('Без дітей')
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=2)
    markup.add(button1, button2, button3, button4)
    bot.send_message(message.chat.id, 'Оберіть кількість дітей:', reply_markup=markup)


def count_of_adult(message):
    button1 = types.KeyboardButton('👤')
    button2 = types.KeyboardButton('👤👤')
    button3 = types.KeyboardButton('👤👤👤')
    button4 = types.KeyboardButton('👤👤👤👤')
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=2)
    markup.add(button1, button2, button3, button4)
    bot.send_message(message.chat.id, 'Оберіть кількість дорослих:', reply_markup=markup)


def child_age(message):
    button1 = types.KeyboardButton('2 роки')
    button2 = types.KeyboardButton('3 роки')
    button3 = types.KeyboardButton('4 роки')
    button4 = types.KeyboardButton('5 років')
    button5 = types.KeyboardButton('6 років')
    button6 = types.KeyboardButton('7 років')
    button7 = types.KeyboardButton('8 років')
    button8 = types.KeyboardButton('9 років')
    button9 = types.KeyboardButton('10 років')
    button10 = types.KeyboardButton('11 років')
    button11 = types.KeyboardButton('12 років')
    button12 = types.KeyboardButton('13 років')
    button13 = types.KeyboardButton('14 років')
    button14 = types.KeyboardButton('15 років')
    button15 = types.KeyboardButton('16 років')
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add(button1, button2, button3, button4, button5, button6, button7, button8, button9, button10, button11,
               button12, button13, button14, button15)
    bot.send_message(message.chat.id, 'Оберіть вік дитини:', reply_markup=markup)


def hotel_stars(message):
    button1 = types.KeyboardButton('⭐⭐')
    button2 = types.KeyboardButton('⭐⭐⭐')
    button3 = types.KeyboardButton('⭐⭐⭐⭐')
    button4 = types.KeyboardButton('⭐⭐⭐⭐⭐')
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=2)
    markup.add(button1, button2, button3, button4)
    bot.send_message(message.chat.id, 'Оберіть кількість зірок готелю🏨', reply_markup=markup)


# creating our bot
bot = telebot.TeleBot(config.TOKEN)


@bot.callback_query_handler(func=inline_calendar.is_inline_calendar_callbackquery)
def calendar_callback_handler(q: types.CallbackQuery):
    """ Handle all inline calendars """
    bot.answer_callback_query(q.id)
    try:
        return_data = inline_calendar.handler_callback(q.from_user.id, q.data)
        if return_data is None:
            bot.edit_message_reply_markup(chat_id=q.from_user.id, message_id=q.message.message_id,
                                          reply_markup=inline_calendar.get_keyboard(q.from_user.id))
        else:
            picked_data = return_data
            bot.edit_message_text(text=f'Обрана дата: {picked_data}', chat_id=q.from_user.id,
                                  message_id=q.message.message_id,
                                  reply_markup=inline_calendar.get_keyboard(q.from_user.id))
            button1 = types.KeyboardButton('Від 1🌙')
            button2 = types.KeyboardButton('Від 3🌙')
            button3 = types.KeyboardButton('Від 5🌙')
            button4 = types.KeyboardButton('Від 7🌙')
            button5 = types.KeyboardButton('Від 9🌙')
            button6 = types.KeyboardButton('Від 11🌙')
            button7 = types.KeyboardButton('Від 14🌙')
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            markup.add(button1, button2, button3, button4, button5, button6, button7)
            bot.send_message(q.from_user.id, 'Запам\'ятаю, оберіть будь ласка кількість ночей🌙', reply_markup=markup)
    except inline_calendar.WrongChoiceCallbackException:
        bot.edit_message_text(text=f'Некоректний вибір', chat_id=q.from_user.id, message_id=q.message.message_id,
                              reply_markup=inline_calendar.get_keyboard(q.from_user.id))


@bot.message_handler(commands=['reset'])
def reset(message):
    """ Clear all unnecessary data from utility dict """
    log(message)
    bot.send_message(message.chat.id, 'Бот готовий до повторного використання. Напишіть /start')


@bot.message_handler(commands=['help'])
def help(message):
    """ Directs user into getting help msg func """
    log(message)
    bot.send_message(message.chat.id, 'Напишіть ваше питання, воно буде надіслане до оператора служби підтримки.')


@bot.message_handler(commands=['rules'])
def rules(message):
    """ Here should be rules for using the bot """
    log(message)
    bot.send_message(message.chat.id, 'Правила використання')


@bot.message_handler(commands=['start'])
def start(message):
    log(message)
    bot.send_chat_action(message.chat.id, action='typing')
    time.sleep(1)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2, one_time_keyboard=True)
    button1 = types.KeyboardButton('🇦🇿Азербайджан')
    button2 = types.KeyboardButton('🇦🇱Албания')
    button3 = types.KeyboardButton('🇧🇬Болгария')
    button4 = types.KeyboardButton('🇬🇷Греция')
    button5 = types.KeyboardButton('🇬🇪Грузия')
    button6 = types.KeyboardButton('🇩🇴Доминиканская республика')
    button7 = types.KeyboardButton('🇪🇬Египет')
    button8 = types.KeyboardButton('🇮🇱Израиль')
    button9 = types.KeyboardButton('🇮🇩Индонезия')
    button10 = types.KeyboardButton('🇪🇸Испания')
    button11 = types.KeyboardButton('🇮🇹Италия')
    button12 = types.KeyboardButton('🇨🇾Кипр')
    button13 = types.KeyboardButton('🇨🇳Китай')
    button14 = types.KeyboardButton('🇨🇺Куба')
    button15 = types.KeyboardButton('🇲🇾Малайзия')
    button16 = types.KeyboardButton('🇲🇻Мальдивы')
    button17 = types.KeyboardButton('🇲🇦Марокко')
    button18 = types.KeyboardButton('🇦🇪ОАЭ')
    button19 = types.KeyboardButton('🇴🇲Оман')
    button20 = types.KeyboardButton('🇵🇹Португалия')
    button21 = types.KeyboardButton('🇹🇭Таиланд')
    button22 = types.KeyboardButton('🇹🇳Тунис')
    button23 = types.KeyboardButton('🇹🇷Турция')
    button24 = types.KeyboardButton('🇭🇷Хорватия')
    button25 = types.KeyboardButton('🇱🇰Шри-Ланка')
    markup.add(button1, button2, button3, button4, button5, button6, button7, button8, button9, button10, button11,
               button12, button13, button14, button15, button16, button17, button18, button19, button20, button21,
               button22, button23, button24, button25)
    bot.send_message(message.chat.id,
                     'Добридень {0.first_name}, вас вітає бот для знаходження та порівняння подорожей-{1.first_name}✈🏝\nОберіть країну👇'.format(
                         message.from_user, bot.get_me()), reply_markup=markup)
    # driver = webdriver.Chrome('C:\\Users\Alexeii\PycharmProjects\ChromeDriver\chromedriver.exe')
    # time.sleep(3)
    # driver.get("https://zaraz.travel/")
    # driver.find_element_by_xpath('//*[@id="ssam-theme-default-town-to-box"]/div[1]/span').click()
    # time.sleep(3)
    # driver.quit()


@bot.message_handler(func=lambda message: message.text == '🇦🇿Азербайджан')
def send_calendar(message):
    log(message)
    ask_from(message)


@bot.message_handler(func=lambda message: message.text == '🇦🇱Албания')
def send_calendar(message):
    log(message)
    ask_from(message)


@bot.message_handler(func=lambda message: message.text == '🇧🇬Болгария')
def send_calendar(message):
    log(message)
    ask_from(message)


@bot.message_handler(func=lambda message: message.text == '🇬🇷Греция')
def send_calendar(message):
    log(message)
    ask_from(message)


@bot.message_handler(func=lambda message: message.text == '🇬🇪Грузия')
def send_calendar(message):
    log(message)
    ask_from(message)


@bot.message_handler(func=lambda message: message.text == '🇩🇴Доминиканская республика')
def send_calendar(message):
    log(message)
    ask_from(message)


@bot.message_handler(func=lambda message: message.text == '🇪🇬Египет')
def send_calendar(message):
    log(message)
    ask_from(message)


@bot.message_handler(func=lambda message: message.text == '🇮🇱Израиль')
def send_calendar(message):
    log(message)
    ask_from(message)


@bot.message_handler(func=lambda message: message.text == '🇮🇩Индонезия')
def send_calendar(message):
    log(message)
    ask_from(message)


@bot.message_handler(func=lambda message: message.text == '🇪🇸Испания')
def send_calendar(message):
    log(message)
    ask_from(message)


@bot.message_handler(func=lambda message: message.text == '🇮🇹Италия')
def send_calendar(message):
    log(message)
    ask_from(message)


@bot.message_handler(func=lambda message: message.text == '🇨🇾Кипр')
def send_calendar(message):
    log(message)
    ask_from(message)


@bot.message_handler(func=lambda message: message.text == '🇨🇳Китай')
def send_calendar(message):
    log(message)
    ask_from(message)


@bot.message_handler(func=lambda message: message.text == '🇨🇺Куба')
def send_calendar(message):
    log(message)
    ask_from(message)


@bot.message_handler(func=lambda message: message.text == '🇲🇾Малайзия')
def send_calendar(message):
    log(message)
    ask_from(message)


@bot.message_handler(func=lambda message: message.text == '🇲🇻Мальдивы')
def send_calendar(message):
    log(message)
    ask_from(message)


@bot.message_handler(func=lambda message: message.text == '🇲🇦Марокко')
def send_calendar(message):
    log(message)
    ask_from(message)


@bot.message_handler(func=lambda message: message.text == '🇦🇪ОАЭ')
def send_calendar(message):
    log(message)
    ask_from(message)


@bot.message_handler(func=lambda message: message.text == '🇴🇲Оман')
def send_calendar(message):
    log(message)
    ask_from(message)


@bot.message_handler(func=lambda message: message.text == '🇵🇹Португалия')
def send_calendar(message):
    log(message)
    ask_from(message)


@bot.message_handler(func=lambda message: message.text == '🇹🇭Таиланд')
def send_calendar(message):
    log(message)
    ask_from(message)


@bot.message_handler(func=lambda message: message.text == '🇹🇳Тунис')
def send_calendar(message):
    log(message)
    ask_from(message)


@bot.message_handler(func=lambda message: message.text == '🇹🇷Турция')
def send_calendar(message):
    log(message)
    ask_from(message)


@bot.message_handler(func=lambda message: message.text == '🇭🇷Хорватия')
def send_calendar(message):
    log(message)
    ask_from(message)


@bot.message_handler(func=lambda message: message.text == '🇱🇰Шри-Ланка')
def send_calendar(message):
    log(message)
    ask_from(message)


@bot.message_handler(func=lambda message: message.text == '🇺🇦Київ')
def ask_date_from(message):
    log(message)
    ask_when(message)


@bot.message_handler(func=lambda message: message.text == '🇺🇦Запоріжжя')
def ask_date_from(message):
    log(message)
    ask_when(message)


@bot.message_handler(func=lambda message: message.text == '🇺🇦Львів')
def ask_date_from(message):
    log(message)
    ask_when(message)


@bot.message_handler(func=lambda message: message.text == '🇺🇦Одесса')
def ask_date_from(message):
    log(message)
    ask_when(message)


@bot.message_handler(func=lambda message: message.text == '🇺🇦Харків')
def ask_date_from(message):
    log(message)
    ask_when(message)


@bot.message_handler(func=lambda message: message.text == 'Від 1🌙')
def ask_count_adult(message):
    log(message)
    count_of_adult(message)


@bot.message_handler(func=lambda message: message.text == 'Від 3🌙')
def ask_count_adult(message):
    log(message)
    count_of_adult(message)


@bot.message_handler(func=lambda message: message.text == 'Від 5🌙')
def ask_count_adult(message):
    log(message)
    count_of_adult(message)


@bot.message_handler(func=lambda message: message.text == 'Від 7🌙')
def ask_count_adult(message):
    log(message)
    count_of_adult(message)


@bot.message_handler(func=lambda message: message.text == 'Від 9🌙')
def ask_count_adult(message):
    log(message)
    count_of_adult(message)


@bot.message_handler(func=lambda message: message.text == 'Від 11🌙')
def ask_count_adult(message):
    log(message)
    count_of_adult(message)


@bot.message_handler(func=lambda message: message.text == 'Від 14🌙')
def ask_count_adult(message):
    log(message)
    count_of_adult(message)


@bot.message_handler(func=lambda message: message.text == '👤')
def ask_count_child(message):
    log(message)
    count_of_child(message)


@bot.message_handler(func=lambda message: message.text == '👤👤')
def ask_count_child(message):
    log(message)
    count_of_child(message)


@bot.message_handler(func=lambda message: message.text == '👤👤👤')
def ask_count_child(message):
    log(message)
    count_of_child(message)


@bot.message_handler(func=lambda message: message.text == '👤👤👤👤')
def ask_count_child(message):
    log(message)
    count_of_child(message)


@bot.message_handler(func=lambda message: message.text == '👶')
def ask_child_age(message):
    log(message)
    child_age(message)


@bot.message_handler(func=lambda message: message.text == '👶👶')
def ask_child_age(message):
    log(message)
    child_age(message)
    # TODO: Придумать как записывать несколько возрастов


@bot.message_handler(func=lambda message: message.text == '👶👶👶')
def ask_child_age(message):
    log(message)
    child_age(message)


@bot.message_handler(func=lambda message: message.text == 'Без дітей')
def ask_child_age(message):
    log(message)
    hotel_stars(message)


@bot.message_handler(func=lambda message: message.text == '⭐⭐')
def get_stars(message):
    log(message)


@bot.message_handler(func=lambda message: message.text == '⭐⭐⭐')
def get_stars(message):
    log(message)


@bot.message_handler(func=lambda message: message.text == '⭐⭐⭐⭐')
def get_stars(message):
    log(message)


@bot.message_handler(func=lambda message: message.text == '⭐⭐⭐⭐⭐')
def get_stars(message):
    log(message)


# BOT RUNNING
if __name__ == '__main__':
    bot.polling(none_stop=True)