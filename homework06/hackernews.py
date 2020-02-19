from bottle import (
    route, run, template, request, redirect
)
from scraputils import get_news
from db import News, session

from bayes import NaiveBayesClassifier
import string


@route("/news")
def news_list():
    s = session()
    rows = s.query(News).filter(News.label == None).all()
    return template('news_template', rows=rows)


@route("/add_label/")
def add_label():
    # 1. Получить значения параметров label и id из GET-запроса
    label = request.query.label
    id = request.query.id

    # 2. Получить запись из БД с соответствующим id (такая запись только одна!)
    # 3. Изменить значение метки записи на значение label
    s = session()
    s.query(News).filter(News.id == id).update({'label': label})

    # 4. Сохранить результат в БД
    s.commit()

    redirect("/news")


@route("/update")
def update_news():
    # 1. Получить данные с новостного сайта
    news = get_news('https://news.ycombinator.com/newest', 1)

    # 2. Проверить, каких новостей еще нет в БД. Будем считать,
    #    что каждая новость может быть уникально идентифицирована
    #    по совокупности двух значений: заголовка и автора

    s = session()
    for item in news:
        if s.query(News).filter(News.title == item['title'], News.author == item['author']).first():
            continue
        s.add(News(**item))

    # 3. Сохранить в БД те новости, которых там нет
    s.commit()
    redirect("/news")


@route('/recommendations')
def recommendations():
    # 1. Получить список неразмеченных новостей из БД
    s = session()
    rows_unlabelled = s.query(News).filter(News.label == None).all()
    X = [clean(row.title).lower() for row in rows_unlabelled]

    # 2. Получить прогнозы для каждой новости
    predictions = model.predict(X)
    rows_good = [rows_unlabelled[i] for i in range(len(rows_unlabelled)) if predictions[i] == 'good']
    rows_maybe = [rows_unlabelled[i] for i in range(len(rows_unlabelled)) if predictions[i] == 'maybe']
    rows_never = [rows_unlabelled[i] for i in range(len(rows_unlabelled)) if predictions[i] == 'never']

    # 3. Вывести ранжированную таблицу с новостями
    return template('recommendations_template', rows_good=rows_good, rows_maybe=rows_maybe, rows_never=rows_never)


def clean(s):
    translator = str.maketrans("", "", string.punctuation)
    return s.translate(translator)


if __name__ == "__main__":
    s = session()
    rows = s.query(News).filter(News.label != None).all()
    X_train = [clean(row.title).lower() for row in rows]
    y_train = [row.label for row in rows]
    model = NaiveBayesClassifier(alpha=0.05)
    model.fit(X_train, y_train)

    run(host="localhost", port=8080)
