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
import selenium


# connection = sql.connect('DATABASE.sqlite')
# q = connection.cursor()
# q.execute('''
# 			CREATE TABLE "user" (
# 				'id' TEXT,
# 				'country' TEXT,
# 				'city' TEXT,
# 				'date_from' TEXT,
# 				'nights' TEXT,
# 				'adults' TEXT,
# 				'childs' TEXT,
# 				'stars' TEXT,
# 				'cost' TEXT
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


def request_zaraz_travel(message):
    connection = sql.connect('DATABASE.sqlite')
    q = connection.cursor()
    q.execute("SELECT * from user WHERE id='%s'" % message.from_user.id)
    results = q.fetchall()
    print(results)
    print(results[0][1].split(',')[1])
    print(results[0][2].split(',')[1])
    connection.commit()
    q.close()
    connection.close()
    driver = webdriver.Chrome('C:\\Users\Alexeii\PycharmProjects\ChromeDriver\chromedriver.exe')
    driver.get("https://zaraz.travel/")
    country_set = driver.find_element_by_xpath('//*[@id="ssam-theme-default-town-to-box"]')
    driver.execute_script(f"arguments[0].setAttribute('data-values','{results[0][1].split(',')[1]}')", country_set)  # set county code
    city = driver.find_element_by_xpath('//*[@id="ssam-theme-default-town-from-box"]')
    driver.execute_script(f"arguments[0].setAttribute('data-values','{results[0][2].split(',')[1]}')", city)  # set city code
    fromfrom = driver.find_element_by_xpath('//*[@id="ssam-theme-default-search-box"]/div[1]/input[1]')
    driver.execute_script(f"arguments[0].setAttribute('value','{results[0][3]}')", fromfrom)  # set fromfrom date
    fromto = driver.find_element_by_xpath('//*[@id="ssam-theme-default-search-box"]/div[1]/input[2]')
    driver.execute_script(f"arguments[0].setAttribute('value','{results[0][3]}')", fromto)  # set fromto date
    # --------------- #
    # Here should be set count of nights
    # --------------- #
    adults = driver.find_element_by_xpath('//*[@id="ssam-theme-default-search-box"]/div[1]/input[3]')
    driver.execute_script(f"arguments[0].setAttribute('value','{results[0][5]}')", adults)  # set count_of adults
    children = driver.find_element_by_xpath('//*[@id="ssam-theme-default-search-box"]/div[1]/input[4]')
    driver.execute_script(f"arguments[0].setAttribute('value','{results[0][6]}')", children)  # set count of children
    stars = driver.find_element_by_xpath('//*[@id="ssam-theme-default-category-box"]')
    driver.execute_script(f"arguments[0].setAttribute('data-values','{results[0][7]}')", stars)  # set count of stars
    driver.find_element_by_xpath('//*[@id="ssam-theme-default-search-box"]/div[5]/button').click()  # Press Шукати
    time.sleep(6.5)
    # all_tours = driver.find_element_by_xpath('/html/body/main/section[2]/div/div/div[2]/div/div[2]/div[2]/div[2]/div/div/div[2]') # work!
    print(driver.find_elements_by_xpath(
        '/html/body/main/section[2]/div/div/div[2]/div/div[2]/div[2]/div[2]/div/div/div[2]/div[1]/div/div/div[2]/div[3]/div[2]/a'))
    if driver.find_elements_by_xpath('/html/body/main/section[2]/div/div/div[2]/div/div[2]/div[2]/div[2]/div/div/div[2]/div[1]/div/div/div[2]/div[3]/div[2]/a') == []:
        print('Ничего не найдено')
        all_tours = []
    else:
        all_tours = []
        for i in range(1, 27):
            try:
                url = driver.find_element_by_xpath(
                    f'/html/body/main/section[2]/div/div/div[2]/div/div[2]/div[2]/div[2]/div/div/div[2]/div[{i}]/div/div/div[2]/div[3]/div[2]/a').get_attribute(
                    "href")
                price = driver.find_element_by_xpath(
                    f'/html/body/main/section[2]/div/div/div[2]/div/div[2]/div[2]/div[2]/div/div/div[2]/div[{i}]/div/div/div[2]/div[3]/div[2]/a').text
                hotel = driver.find_element_by_xpath(
                    f'/html/body/main/section[2]/div/div/div[2]/div/div[2]/div[2]/div[2]/div/div/div[2]/div[{i}]/div/div/div[2]/div[1]/a/p').text
                date = driver.find_element_by_xpath(
                    f'/html/body/main/section[2]/div/div/div[2]/div/div[2]/div[2]/div[2]/div/div/div[2]/div[{i}]/div/div/div[2]/div[2]/div[2]/p[2]').text
                country = driver.find_element_by_xpath(
                    f'/html/body/main/section[2]/div/div/div[2]/div/div[2]/div[2]/div[2]/div/div/div[2]/div[{i}]/div/div/div[2]/div[3]/div[1]/p/span').text
                print(url)
                print(price)
                print(hotel)
                print(date)
                print(country)
                dict = {
                    'url': url,
                    'price': price,
                    'hotel': hotel,
                    'date': date,
                    'country': country
                }
                all_tours.append(dict)
            except selenium.common.exceptions.NoSuchElementException:
                pass
    print(all_tours)
    try:
        for i in range(1, 6):
            bot.send_message(message.chat.id, f'✈{all_tours[i]["country"]}\n🏝{all_tours[i]["hotel"]}\n📅{all_tours[i]["date"]}\n💵<a href="{all_tours[i]["url"]}">{all_tours[i]["price"]}</a>', parse_mode='HTML')
    except IndexError:
        bot.send_message(message.chat.id, 'По вашому запиту не знайдено жодних тарифів🤷‍\nСпробуйте ще🔁\nНапишіть /reset для перезапуску')

        #  driver.quit()

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


def expected_cost(message):
    button1 = types.KeyboardButton('💵0-300$')
    button2 = types.KeyboardButton('💵300-600$')
    button3 = types.KeyboardButton('💵600-900$')
    button4 = types.KeyboardButton('💵900-1200$')
    button5 = types.KeyboardButton('💵1200-1500$')
    button6 = types.KeyboardButton('💵Від 1500$')
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=2)
    markup.add(button1, button2, button3, button4, button5, button6)
    bot.send_message(message.chat.id, 'Оберіть початкову вартість туру💸', reply_markup=markup)


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
            connection = sql.connect('DATABASE.sqlite')
            q1 = connection.cursor()
            db_picked_data = str(str(picked_data).split('-')[2]) + '.' + str(str(picked_data).split('-')[1]) + '.' + str(str(picked_data).split('-')[0])
            print(db_picked_data)
            q1.execute("UPDATE user SET date_from='%s' WHERE id='%s'" % (db_picked_data, q.from_user.id))
            connection.commit()
            q1.close()
            connection.close()
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
    connection = sql.connect('DATABASE.sqlite')
    q = connection.cursor()
    q.execute("SELECT EXISTS(SELECT 1 FROM user WHERE id='%s')" % message.from_user.id)
    results1 = q.fetchone()
    if results1[0] != 1:
        q.execute("INSERT INTO 'user' (id) VALUES ('%s')" % message.from_user.id)
    connection.commit()
    q.close()
    connection.close()
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


@bot.message_handler(func=lambda message: message.text == '🇦🇿Азербайджан')
def send_calendar(message):
    log(message)
    country = message.text
    connection = sql.connect('DATABASE.sqlite')
    q = connection.cursor()
    q.execute("UPDATE user SET country='%s' WHERE id='%s'" % (f'{country[2:]},2000000087', message.from_user.id))
    connection.commit()
    q.close()
    connection.close()
    ask_from(message)


@bot.message_handler(func=lambda message: message.text == '🇦🇱Албания')
def send_calendar(message):
    log(message)
    country = message.text
    connection = sql.connect('DATABASE.sqlite')
    q = connection.cursor()
    q.execute("UPDATE user SET country='%s' WHERE id='%s'" % (f'{country[2:]},2000000115', message.from_user.id))
    connection.commit()
    q.close()
    connection.close()
    ask_from(message)


@bot.message_handler(func=lambda message: message.text == '🇧🇬Болгария')
def send_calendar(message):
    log(message)
    country = message.text
    connection = sql.connect('DATABASE.sqlite')
    q = connection.cursor()
    q.execute("UPDATE user SET country='%s' WHERE id='%s'" % (f'{country[2:]},35', message.from_user.id))
    connection.commit()
    q.close()
    connection.close()
    ask_from(message)


@bot.message_handler(func=lambda message: message.text == '🇬🇷Греция')
def send_calendar(message):
    log(message)
    country = message.text
    connection = sql.connect('DATABASE.sqlite')
    q = connection.cursor()
    q.execute("UPDATE user SET country='%s' WHERE id='%s'" % (f'{country[2:]},10', message.from_user.id))
    connection.commit()
    q.close()
    connection.close()
    ask_from(message)


@bot.message_handler(func=lambda message: message.text == '🇬🇪Грузия')
def send_calendar(message):
    log(message)
    country = message.text
    connection = sql.connect('DATABASE.sqlite')
    q = connection.cursor()
    q.execute("UPDATE user SET country='%s' WHERE id='%s'" % (f'{country[2:]},151', message.from_user.id))
    connection.commit()
    q.close()
    connection.close()
    ask_from(message)


@bot.message_handler(func=lambda message: message.text == '🇩🇴Доминиканская республика')
def send_calendar(message):
    log(message)
    country = message.text
    connection = sql.connect('DATABASE.sqlite')
    q = connection.cursor()
    q.execute("UPDATE user SET country='%s' WHERE id='%s'" % (f'{country[2:]},42', message.from_user.id))
    connection.commit()
    q.close()
    connection.close()
    ask_from(message)


@bot.message_handler(func=lambda message: message.text == '🇪🇬Египет')
def send_calendar(message):
    log(message)
    country = message.text
    connection = sql.connect('DATABASE.sqlite')
    q = connection.cursor()
    q.execute("UPDATE user SET country='%s' WHERE id='%s'" % (f'{country[2:]},3', message.from_user.id))
    connection.commit()
    q.close()
    connection.close()
    ask_from(message)


@bot.message_handler(func=lambda message: message.text == '🇮🇱Израиль')
def send_calendar(message):
    log(message)
    country = message.text
    connection = sql.connect('DATABASE.sqlite')
    q = connection.cursor()
    q.execute("UPDATE user SET country='%s' WHERE id='%s'" % (f'{country[2:]},80', message.from_user.id))
    connection.commit()
    q.close()
    connection.close()
    ask_from(message)


@bot.message_handler(func=lambda message: message.text == '🇮🇩Индонезия')
def send_calendar(message):
    log(message)
    country = message.text
    connection = sql.connect('DATABASE.sqlite')
    q = connection.cursor()
    q.execute("UPDATE user SET country='%s' WHERE id='%s'" % (f'{country[2:]},59', message.from_user.id))
    connection.commit()
    q.close()
    connection.close()
    ask_from(message)


@bot.message_handler(func=lambda message: message.text == '🇪🇸Испания')
def send_calendar(message):
    log(message)
    country = message.text
    connection = sql.connect('DATABASE.sqlite')
    q = connection.cursor()
    q.execute("UPDATE user SET country='%s' WHERE id='%s'" % (f'{country[2:]},18', message.from_user.id))
    connection.commit()
    q.close()
    connection.close()
    ask_from(message)


@bot.message_handler(func=lambda message: message.text == '🇮🇹Италия')
def send_calendar(message):
    log(message)
    country = message.text
    connection = sql.connect('DATABASE.sqlite')
    q = connection.cursor()
    q.execute("UPDATE user SET country='%s' WHERE id='%s'" % (f'{country[2:]},6', message.from_user.id))
    connection.commit()
    q.close()
    connection.close()
    ask_from(message)


@bot.message_handler(func=lambda message: message.text == '🇨🇾Кипр')
def send_calendar(message):
    log(message)
    country = message.text
    connection = sql.connect('DATABASE.sqlite')
    q = connection.cursor()
    q.execute("UPDATE user SET country='%s' WHERE id='%s'" % (f'{country[2:]},16', message.from_user.id))
    connection.commit()
    q.close()
    connection.close()
    ask_from(message)


@bot.message_handler(func=lambda message: message.text == '🇨🇳Китай')
def send_calendar(message):
    log(message)
    country = message.text
    connection = sql.connect('DATABASE.sqlite')
    q = connection.cursor()
    q.execute("UPDATE user SET country='%s' WHERE id='%s'" % (f'{country[2:]},99', message.from_user.id))
    connection.commit()
    q.close()
    connection.close()
    ask_from(message)


@bot.message_handler(func=lambda message: message.text == '🇨🇺Куба')
def send_calendar(message):
    log(message)
    country = message.text
    connection = sql.connect('DATABASE.sqlite')
    q = connection.cursor()
    q.execute("UPDATE user SET country='%s' WHERE id='%s'" % (f'{country[2:]},76', message.from_user.id))
    connection.commit()
    q.close()
    connection.close()
    ask_from(message)


@bot.message_handler(func=lambda message: message.text == '🇲🇾Малайзия')
def send_calendar(message):
    log(message)
    country = message.text
    connection = sql.connect('DATABASE.sqlite')
    q = connection.cursor()
    q.execute("UPDATE user SET country='%s' WHERE id='%s'" % (f'{country[2:]},69', message.from_user.id))
    connection.commit()
    q.close()
    connection.close()
    ask_from(message)


@bot.message_handler(func=lambda message: message.text == '🇲🇻Мальдивы')
def send_calendar(message):
    log(message)
    country = message.text
    connection = sql.connect('DATABASE.sqlite')
    q = connection.cursor()
    q.execute("UPDATE user SET country='%s' WHERE id='%s'" % (f'{country[2:]},73', message.from_user.id))
    connection.commit()
    q.close()
    connection.close()
    ask_from(message)


@bot.message_handler(func=lambda message: message.text == '🇲🇦Марокко')
def send_calendar(message):
    log(message)
    country = message.text
    connection = sql.connect('DATABASE.sqlite')
    q = connection.cursor()
    q.execute("UPDATE user SET country='%s' WHERE id='%s'" % (f'{country[2:]},86', message.from_user.id))
    connection.commit()
    q.close()
    connection.close()
    ask_from(message)


@bot.message_handler(func=lambda message: message.text == '🇦🇪ОАЭ')
def send_calendar(message):
    log(message)
    country = message.text
    connection = sql.connect('DATABASE.sqlite')
    q = connection.cursor()
    q.execute("UPDATE user SET country='%s' WHERE id='%s'" % (f'{country[2:]},20', message.from_user.id))
    connection.commit()
    q.close()
    connection.close()
    ask_from(message)


@bot.message_handler(func=lambda message: message.text == '🇴🇲Оман')
def send_calendar(message):
    log(message)
    country = message.text
    connection = sql.connect('DATABASE.sqlite')
    q = connection.cursor()
    q.execute("UPDATE user SET country='%s' WHERE id='%s'" % (f'{country[2:]},94', message.from_user.id))
    connection.commit()
    q.close()
    connection.close()
    ask_from(message)


@bot.message_handler(func=lambda message: message.text == '🇵🇹Португалия')
def send_calendar(message):
    log(message)
    country = message.text
    connection = sql.connect('DATABASE.sqlite')
    q = connection.cursor()
    q.execute("UPDATE user SET country='%s' WHERE id='%s'" % (f'{country[2:]},81', message.from_user.id))
    connection.commit()
    q.close()
    connection.close()
    ask_from(message)


@bot.message_handler(func=lambda message: message.text == '🇹🇭Таиланд')
def send_calendar(message):
    log(message)
    country = message.text
    connection = sql.connect('DATABASE.sqlite')
    q = connection.cursor()
    q.execute("UPDATE user SET country='%s' WHERE id='%s'" % (f'{country[2:]},12', message.from_user.id))
    connection.commit()
    q.close()
    connection.close()
    ask_from(message)


@bot.message_handler(func=lambda message: message.text == '🇹🇳Тунис')
def send_calendar(message):
    log(message)
    country = message.text
    connection = sql.connect('DATABASE.sqlite')
    q = connection.cursor()
    q.execute("UPDATE user SET country='%s' WHERE id='%s'" % (f'{country[2:]},15', message.from_user.id))
    connection.commit()
    q.close()
    connection.close()
    ask_from(message)


@bot.message_handler(func=lambda message: message.text == '🇹🇷Турция')
def send_calendar(message):
    log(message)
    country = message.text
    connection = sql.connect('DATABASE.sqlite')
    q = connection.cursor()
    q.execute("UPDATE user SET country='%s' WHERE id='%s'" % (f'{country[2:]},5', message.from_user.id))
    connection.commit()
    q.close()
    connection.close()
    ask_from(message)


@bot.message_handler(func=lambda message: message.text == '🇭🇷Хорватия')
def send_calendar(message):
    log(message)
    country = message.text
    connection = sql.connect('DATABASE.sqlite')
    q = connection.cursor()
    q.execute("UPDATE user SET country='%s' WHERE id='%s'" % (f'{country[2:]},8', message.from_user.id))
    connection.commit()
    q.close()
    connection.close()
    ask_from(message)


@bot.message_handler(func=lambda message: message.text == '🇱🇰Шри-Ланка')
def send_calendar(message):
    log(message)
    country = message.text
    connection = sql.connect('DATABASE.sqlite')
    q = connection.cursor()
    q.execute("UPDATE user SET country='%s' WHERE id='%s'" % (f'{country[2:]},116', message.from_user.id))
    connection.commit()
    q.close()
    connection.close()
    ask_from(message)


@bot.message_handler(func=lambda message: message.text == '🇺🇦Київ')
def ask_date_from(message):
    log(message)
    city = message.text
    print(city[2:])
    connection = sql.connect('DATABASE.sqlite')
    q = connection.cursor()
    q.execute("UPDATE user SET city='%s' WHERE id='%s'" % (f'{city[2:]},149', message.from_user.id))
    connection.commit()
    q.close()
    connection.close()
    ask_when(message)


@bot.message_handler(func=lambda message: message.text == '🇺🇦Запоріжжя')
def ask_date_from(message):
    log(message)
    city = message.text
    connection = sql.connect('DATABASE.sqlite')
    q = connection.cursor()
    q.execute("UPDATE user SET city='%s' WHERE id='%s'" % (f'{city[2:]},648', message.from_user.id))
    connection.commit()
    q.close()
    connection.close()
    ask_when(message)


@bot.message_handler(func=lambda message: message.text == '🇺🇦Львів')
def ask_date_from(message):
    log(message)
    city = message.text
    connection = sql.connect('DATABASE.sqlite')
    q = connection.cursor()
    q.execute("UPDATE user SET city='%s' WHERE id='%s'" % (f'{city[2:]},534', message.from_user.id))
    connection.commit()
    q.close()
    connection.close()
    ask_when(message)


@bot.message_handler(func=lambda message: message.text == '🇺🇦Одесса')
def ask_date_from(message):
    log(message)
    city = message.text
    connection = sql.connect('DATABASE.sqlite')
    q = connection.cursor()
    q.execute("UPDATE user SET city='%s' WHERE id='%s'" % (f'{city[2:]},532', message.from_user.id))
    connection.commit()
    q.close()
    connection.close()
    ask_when(message)


@bot.message_handler(func=lambda message: message.text == '🇺🇦Харків')
def ask_date_from(message):
    log(message)
    city = message.text
    connection = sql.connect('DATABASE.sqlite')
    q = connection.cursor()
    q.execute("UPDATE user SET city='%s' WHERE id='%s'" % (f'{city[2:]},146', message.from_user.id))
    connection.commit()
    q.close()
    connection.close()
    ask_when(message)


@bot.message_handler(func=lambda message: message.text == 'Від 1🌙')
def ask_count_adult(message):
    log(message)
    nights = message.text
    connection = sql.connect('DATABASE.sqlite')
    q = connection.cursor()
    q.execute("UPDATE user SET nights='%s' WHERE id='%s'" % (nights[4], message.from_user.id))
    connection.commit()
    q.close()
    connection.close()
    count_of_adult(message)


@bot.message_handler(func=lambda message: message.text == 'Від 3🌙')
def ask_count_adult(message):
    log(message)
    nights = message.text
    connection = sql.connect('DATABASE.sqlite')
    q = connection.cursor()
    q.execute("UPDATE user SET nights='%s' WHERE id='%s'" % (nights[4], message.from_user.id))
    connection.commit()
    q.close()
    connection.close()
    count_of_adult(message)


@bot.message_handler(func=lambda message: message.text == 'Від 5🌙')
def ask_count_adult(message):
    log(message)
    nights = message.text
    connection = sql.connect('DATABASE.sqlite')
    q = connection.cursor()
    q.execute("UPDATE user SET nights='%s' WHERE id='%s'" % (nights[4], message.from_user.id))
    connection.commit()
    q.close()
    connection.close()
    count_of_adult(message)


@bot.message_handler(func=lambda message: message.text == 'Від 7🌙')
def ask_count_adult(message):
    log(message)
    nights = message.text
    connection = sql.connect('DATABASE.sqlite')
    q = connection.cursor()
    q.execute("UPDATE user SET nights='%s' WHERE id='%s'" % (nights[4], message.from_user.id))
    connection.commit()
    q.close()
    connection.close()
    count_of_adult(message)


@bot.message_handler(func=lambda message: message.text == 'Від 9🌙')
def ask_count_adult(message):
    log(message)
    nights = message.text
    connection = sql.connect('DATABASE.sqlite')
    q = connection.cursor()
    q.execute("UPDATE user SET nights='%s' WHERE id='%s'" % (nights[4], message.from_user.id))
    connection.commit()
    q.close()
    connection.close()
    count_of_adult(message)


@bot.message_handler(func=lambda message: message.text == 'Від 11🌙')
def ask_count_adult(message):
    log(message)
    nights = message.text
    connection = sql.connect('DATABASE.sqlite')
    q = connection.cursor()
    q.execute("UPDATE user SET nights='%s' WHERE id='%s'" % (nights[4], message.from_user.id))
    connection.commit()
    q.close()
    connection.close()
    count_of_adult(message)


@bot.message_handler(func=lambda message: message.text == 'Від 14🌙')
def ask_count_adult(message):
    log(message)
    nights = message.text
    connection = sql.connect('DATABASE.sqlite')
    q = connection.cursor()
    q.execute("UPDATE user SET nights='%s' WHERE id='%s'" % (nights[4], message.from_user.id))
    connection.commit()
    q.close()
    connection.close()
    count_of_adult(message)


@bot.message_handler(func=lambda message: message.text == '👤')
def ask_count_child(message):
    log(message)
    adults = message.text
    connection = sql.connect('DATABASE.sqlite')
    q = connection.cursor()
    q.execute("UPDATE user SET adults='%s' WHERE id='%s'" % (len(adults), message.from_user.id))
    connection.commit()
    q.close()
    connection.close()
    count_of_child(message)


@bot.message_handler(func=lambda message: message.text == '👤👤')
def ask_count_child(message):
    log(message)
    adults = message.text
    connection = sql.connect('DATABASE.sqlite')
    q = connection.cursor()
    q.execute("UPDATE user SET adults='%s' WHERE id='%s'" % (len(adults), message.from_user.id))
    connection.commit()
    q.close()
    connection.close()
    count_of_child(message)


@bot.message_handler(func=lambda message: message.text == '👤👤👤')
def ask_count_child(message):
    log(message)
    adults = message.text
    connection = sql.connect('DATABASE.sqlite')
    q = connection.cursor()
    q.execute("UPDATE user SET adults='%s' WHERE id='%s'" % (len(adults), message.from_user.id))
    connection.commit()
    q.close()
    connection.close()
    count_of_child(message)


@bot.message_handler(func=lambda message: message.text == '👤👤👤👤')
def ask_count_child(message):
    log(message)
    adults = message.text
    connection = sql.connect('DATABASE.sqlite')
    q = connection.cursor()
    q.execute("UPDATE user SET adults='%s' WHERE id='%s'" % (len(adults), message.from_user.id))
    connection.commit()
    q.close()
    connection.close()
    count_of_child(message)


@bot.message_handler(func=lambda message: message.text == '👶')
def ask_child_age(message):
    log(message)
    childs = message.text
    connection = sql.connect('DATABASE.sqlite')
    q = connection.cursor()
    q.execute("UPDATE user SET childs='%s' WHERE id='%s'" % (len(childs), message.from_user.id))
    connection.commit()
    q.close()
    connection.close()
    child_age(message)


@bot.message_handler(func=lambda message: message.text == '👶👶')
def ask_child_age(message):
    log(message)
    childs = message.text
    connection = sql.connect('DATABASE.sqlite')
    q = connection.cursor()
    q.execute("UPDATE user SET childs='%s' WHERE id='%s'" % (len(childs), message.from_user.id))
    connection.commit()
    q.close()
    connection.close()
    child_age(message)
    # TODO: Придумать как записывать несколько возрастов


@bot.message_handler(func=lambda message: message.text == '👶👶👶')
def ask_child_age(message):
    log(message)
    childs = message.text
    connection = sql.connect('DATABASE.sqlite')
    q = connection.cursor()
    q.execute("UPDATE user SET childs='%s' WHERE id='%s'" % (len(childs), message.from_user.id))
    connection.commit()
    q.close()
    connection.close()
    child_age(message)


@bot.message_handler(func=lambda message: message.text == 'Без дітей')
def ask_child_age(message):
    log(message)
    childs = message.text
    connection = sql.connect('DATABASE.sqlite')
    q = connection.cursor()
    q.execute("UPDATE user SET childs='%s' WHERE id='%s'" % ('0', message.from_user.id))
    connection.commit()
    q.close()
    connection.close()
    hotel_stars(message)


@bot.message_handler(func=lambda message: message.text == '⭐⭐')
def get_stars(message):
    log(message)
    stars = message.text
    connection = sql.connect('DATABASE.sqlite')
    q = connection.cursor()
    q.execute("UPDATE user SET stars='%s' WHERE id='%s'" % (len(stars), message.from_user.id))
    connection.commit()
    q.close()
    connection.close()
    expected_cost(message)


@bot.message_handler(func=lambda message: message.text == '⭐⭐⭐')
def get_stars(message):
    log(message)
    stars = message.text
    connection = sql.connect('DATABASE.sqlite')
    q = connection.cursor()
    q.execute("UPDATE user SET stars='%s' WHERE id='%s'" % (len(stars), message.from_user.id))
    connection.commit()
    q.close()
    connection.close()
    expected_cost(message)


@bot.message_handler(func=lambda message: message.text == '⭐⭐⭐⭐')
def get_stars(message):
    log(message)
    stars = message.text
    connection = sql.connect('DATABASE.sqlite')
    q = connection.cursor()
    q.execute("UPDATE user SET stars='%s' WHERE id='%s'" % (len(stars), message.from_user.id))
    connection.commit()
    q.close()
    connection.close()
    expected_cost(message)


@bot.message_handler(func=lambda message: message.text == '⭐⭐⭐⭐⭐')
def get_stars(message):
    log(message)
    stars = message.text
    connection = sql.connect('DATABASE.sqlite')
    q = connection.cursor()
    q.execute("UPDATE user SET stars='%s' WHERE id='%s'" % (len(stars), message.from_user.id))
    connection.commit()
    q.close()
    connection.close()
    expected_cost(message)


@bot.message_handler(func=lambda message: message.text == '💵0-300$')
def get_cost(message):
    log(message)
    bot.send_message(message.chat.id, 'Формуємо вашу персональну підбірку📠\nЗачекайте⏳')
    cost = message.text
    connection = sql.connect('DATABASE.sqlite')
    q = connection.cursor()
    q.execute("UPDATE user SET cost='%s' WHERE id='%s'" % (cost[1:-1], message.from_user.id))
    connection.commit()
    q.close()
    connection.close()
    request_zaraz_travel(message)


@bot.message_handler(func=lambda message: message.text == '💵300-600$')
def get_cost(message):
    log(message)
    bot.send_message(message.chat.id, 'Формуємо вашу персональну підбірку📠\nЗачекайте⏳')
    cost = message.text
    connection = sql.connect('DATABASE.sqlite')
    q = connection.cursor()
    q.execute("UPDATE user SET cost='%s' WHERE id='%s'" % (cost[1:-1], message.from_user.id))
    connection.commit()
    q.close()
    request_zaraz_travel(message)


@bot.message_handler(func=lambda message: message.text == '💵600-900$')
def get_cost(message):
    log(message)
    bot.send_message(message.chat.id, 'Формуємо вашу персональну підбірку📠\nЗачекайте⏳')
    cost = message.text
    connection = sql.connect('DATABASE.sqlite')
    q = connection.cursor()
    q.execute("UPDATE user SET cost='%s' WHERE id='%s'" % (cost[1:-1], message.from_user.id))
    connection.commit()
    q.close()
    request_zaraz_travel(message)


@bot.message_handler(func=lambda message: message.text == '💵900-1200$')
def get_cost(message):
    log(message)
    bot.send_message(message.chat.id, 'Формуємо вашу персональну підбірку📠\nЗачекайте⏳')
    cost = message.text
    connection = sql.connect('DATABASE.sqlite')
    q = connection.cursor()
    q.execute("UPDATE user SET cost='%s' WHERE id='%s'" % (cost[1:-1], message.from_user.id))
    connection.commit()
    q.close()
    request_zaraz_travel(message)


@bot.message_handler(func=lambda message: message.text == '💵1200-1500$')
def get_cost(message):
    log(message)
    bot.send_message(message.chat.id, 'Формуємо вашу персональну підбірку📠\nЗачекайте⏳')
    cost = message.text
    connection = sql.connect('DATABASE.sqlite')
    q = connection.cursor()
    q.execute("UPDATE user SET cost='%s' WHERE id='%s'" % (cost[1:-1], message.from_user.id))
    connection.commit()
    q.close()
    request_zaraz_travel(message)


@bot.message_handler(func=lambda message: message.text == '💵Від 1500$')
def get_cost(message):
    log(message)
    bot.send_message(message.chat.id, 'Формуємо вашу персональну підбірку📠\nЗачекайте⏳')
    cost = message.text
    connection = sql.connect('DATABASE.sqlite')
    q = connection.cursor()
    q.execute("UPDATE user SET cost='%s' WHERE id='%s'" % (cost[5:-1], message.from_user.id))
    connection.commit()
    q.close()
    request_zaraz_travel(message)


# BOT RUNNING
if __name__ == '__main__':
    bot.polling(none_stop=True)
