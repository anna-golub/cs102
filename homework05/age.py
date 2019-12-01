import datetime as dt
from statistics import median
from typing import Optional

from api import get_friends


# from api_models import User


def age_predict(user_id: int) -> Optional[float]:
    """ Наивный прогноз возраста по возрасту друзей
    Возраст считается как медиана среди возраста всех друзей пользователя
    :param user_id: идентификатор пользователя
    :return: медианный возраст пользователя
    """
    assert isinstance(user_id, int), "user_id must be positive integer"
    assert user_id > 0, "user_id must be positive integer"

    friends = get_friends(user_id, 'bdate')
    if friends is None:
        return -1

    today = dt.datetime.now()
    ages = []

    for friend in friends:
        try:
            day, month, year = map(int, friend['bdate'].split('.'))
            bdate = dt.datetime(year, month, day)
            ages.append((today - bdate).days // 365)
        except:
            pass
    return median(ages)


if __name__ == "__main__":
    print(age_predict(8606586))
