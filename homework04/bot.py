import requests
import config
import telebot
from bs4 import BeautifulSoup

weekdays = {'/monday': '1', '/tuesday': '2', '/wednesday': '3', '/thursday': '4', '/friday': '5', '/saturday': '6',
            '/sunday': '1'}

telebot.apihelper.proxy = {'https': 'https://13.69.22.40:8080'}
bot = telebot.TeleBot(config.access_token)


def get_page(group, week=''):
    if week:
        week = str(week) + '/'
    url = '{domain}/{group}/{week}raspisanie_zanyatiy_{group}.htm'.format(
        domain=config.domain,
        week=week,
        group=group)
    response = requests.get(url)
    web_page = response.text

    # with open('web_page.txt', 'w') as f:
    #   f.write(web_page)

    return web_page


def parse_schedule_for_a_monday(web_page):
    soup = BeautifulSoup(web_page, "html.parser")
    # print(soup)

    # Получаем таблицу с расписанием на понедельник
    schedule_table = soup.find("table", attrs={"id": "2day"})

    # Время проведения занятий
    times_list = schedule_table.find_all("td", attrs={"class": "time"})
    times_list = [time.span.text for time in times_list]
    print(times_list)

    # Место проведения занятий
    locations_list = schedule_table.find_all("td", attrs={"class": "room"})
    locations_list = [room.span.text for room in locations_list]

    # Название дисциплин и имена преподавателей
    lessons_list = schedule_table.find_all("td", attrs={"class": "lesson"})
    lessons_list = [lesson.text.split('\n\n') for lesson in lessons_list]
    lessons_list = [', '.join([info for info in lesson_info if info]) for lesson_info in lessons_list]

    return times_list, locations_list, lessons_list


@bot.message_handler(commands=['monday'])
def get_monday(message):
    """ Получить расписание на понедельник """
    _, group = message.text.split()
    web_page = get_page(group)
    times_lst, locations_lst, lessons_lst = \
        parse_schedule_for_a_monday(web_page)
    resp = ''
    for time, location, lesson in zip(times_lst, locations_lst, lessons_lst):
        resp += '<b>{}</b>, {}, {}\n'.format(time, location, lesson)
    bot.send_message(message.chat.id, resp, parse_mode='HTML')


@bot.message_handler(commands=['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'])
def get_schedule(message):
    """ Получить расписание на указанный день """
    day, group, week = message.text.split()
    day = weekdays[day]
    web_page = get_page(group, week)

    soup = BeautifulSoup(web_page, "html.parser")
    schedule_table = soup.find("table", attrs={"id": day + "day"})

    if schedule_table is None:
        resp = "В этот день занятий нет"
    else:
        times_list = schedule_table.find_all("td", attrs={"class": "time"})
        times_list = [time.span.text for time in times_list]

        locations_list = schedule_table.find_all("td", attrs={"class": "room"})
        locations_list = [room.span.text for room in locations_list]

        lessons_list = schedule_table.find_all("td", attrs={"class": "lesson"})
        lessons_list = [lesson.text.split('\n\n') for lesson in lessons_list]
        lessons_list = [', '.join([info for info in lesson_info if info]) for lesson_info in lessons_list]

        resp = ''
        for time, location, lesson in zip(times_list, locations_list, lessons_list):
            resp += '<b>{}</b>, {}, {}\n'.format(time, location, lesson)
    bot.send_message(message.chat.id, resp, parse_mode='HTML')


@bot.message_handler(commands=['near'])
def get_near_lesson(message):
    """ Получить ближайшее занятие """
    # PUT YOUR CODE HERE
    pass


@bot.message_handler(commands=['tommorow'])
def get_tomorrow(message):
    """ Получить расписание на следующий день """
    # PUT YOUR CODE HERE
    pass


@bot.message_handler(commands=['all'])
def get_all_schedule(message):
    """ Получить расписание на всю неделю для указанной группы """
    _, group, week = message.text.split()
    web_page = get_page(group, week)
    soup = BeautifulSoup(web_page, "html.parser")
    print(soup)
    print("\n")

    resp = ''
    for day in range(1, 7):

        schedule_table = soup.find("table", attrs={"id": str(day) + "day"})

        print(day)
        print(schedule_table)
        print()

        if schedule_table is None:
            resp += "В этот день занятий нет" + "\n"
        else:
            times_list = schedule_table.find_all("td", attrs={"class": "time"})
            times_list = [time.span.text for time in times_list]

            locations_list = schedule_table.find_all("td", attrs={"class": "room"})
            locations_list = [room.span.text for room in locations_list]

            lessons_list = schedule_table.find_all("td", attrs={"class": "lesson"})
            lessons_list = [lesson.text.split('\n\n') for lesson in lessons_list]
            lessons_list = [', '.join([info for info in lesson_info if info]) for lesson_info in lessons_list]

            for time, location, lesson in zip(times_list, locations_list, lessons_list):
                resp += '<b>{}</b>, {}, {}\n'.format(time, location, lesson) + "\n"
    bot.send_message(message.chat.id, resp, parse_mode='HTML')


if __name__ == '__main__':
    bot.polling(none_stop=True)
