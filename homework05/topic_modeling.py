import config

import pandas as pd
import requests
import textwrap
import pymorphy2
import gensim
import pyLDAvis.gensim

from pandas.io.json import json_normalize
from string import Template
from tqdm import tqdm


def get_wall(
        owner_id: str = '',
        domain: str = '',
        offset: int = 0,
        count: int = 10,
        filter: str = 'owner',
        extended: int = 0,
        fields: str = '',
        v: str = '5.103'
) -> pd.DataFrame:
    """
    Возвращает список записей со стены пользователя или сообщества.

    @see: https://vk.com/dev/wall.get

    :param owner_id: Идентификатор пользователя или сообщества, со стены которого необходимо получить записи.
    :param domain: Короткий адрес пользователя или сообщества.
    :param offset: Смещение, необходимое для выборки определенного подмножества записей.
    :param count: Количество записей, которое необходимо получить (0 - все записи).
    :param filter: Определяет, какие типы записей на стене необходимо получить.
    :param extended: 1 — в ответе будут возвращены дополнительные поля profiles и groups, содержащие информацию о пользователях и сообществах.
    :param fields: Список дополнительных полей для профилей и сообществ, которые необходимо вернуть.
    :param v: Версия API.
    """

    access_token = config.VK_CONFIG['access_token']
    code = Template("""return API.wall.get({
        "owner_id": "$owner_id",
        "domain": "$domain",
        "offset": $offset,
        "count": $count,
        "filter": "$filter",
        "extended": $extended,
        "fields": "$fields",
        "v":"$v"
    });""")
    code = code.safe_substitute(owner_id=owner_id, domain=domain, offset=offset, count=count, filter=filter,
                                extended=extended, fields=fields, v=v)

    response = requests.post(
        url="https://api.vk.com/method/execute",
        data={"code": code, "access_token": access_token, "v": v})

    df = pd.DataFrame(response.json()['response']['items'])['text']
    df.to_csv(r'data_frame.txt', header=False, index=None, mode='a', sep=' ')
    return df


def text_normalize(data_file, corpora_file):
    with open(data_file, 'r', encoding='utf8') as file_in, open(corpora_file, 'a', encoding='utf8') as file_out:
        text = textwrap.wrap(file_in.read(), 200)
        res = []

        for s in tqdm(text):
            s = s.strip().split(' ')
            for word in s:
                if not is_word_in_russian(word):
                    continue
                word_arr = clean(word)

                for w in word_arr:
                    check_if_stop_word = is_stop_word(w)
                    if check_if_stop_word is True:
                        continue
                    res.append(check_if_stop_word[1])

        res = ' '.join(res)
        file_out.write('\n'.join(textwrap.wrap(res, 120)))
        return res


def is_word_in_russian(word) -> bool:
    for ch in word:
        if not 1040 <= ord(ch) <= 1103:
            return False
    return True


def is_stop_word(word):
    morph = pymorphy2.MorphAnalyzer()
    stop_tags = {'NUMR', 'NPRO', 'PREP', 'CONJ', 'PRCL', 'INTJ', 'PRED'}

    word_parsed = morph.parse(word)[0]
    tag = word_parsed.tag
    pos = tag.POS
    if pos in stop_tags:
        return True
    if pos == 'ADJF' and 'Apro' in tag or pos == 'ADVB' and 'Ques' in tag:
        return True

    normal = word_parsed.normal_form
    if normal == 'быть':
        return True
    return False, normal


def clean(word):
    # удаляем лишние символы вначале и в конце
    word = list(word.strip())
    start = 0
    while True:
        if word[start].isalpha():
            break
        start += 1

    end = len(word) - 1
    while True:
        if word[end].isalpha():
            break
        end -= 1
    word = word[start:end + 1]

    # делаем все буквы маленькими; ё -> е
    for j in range(len(word)):
        if word[j].isalpha():
            word[j] = word[j].lower()
            if word[j] == 'ё':
                word[j] = 'е'
    word = ''.join(word)

    # разделяем по дефисам или слешам
    if '-' in word:
        return word.split('-')
    return word.split('/')


if __name__ == "__main__":
    publics = ['awesomelanguages', 'akademia_pauk', 'linguista_sum', 'public68409238', 'pss_languages',
               'linguaehobbitique', 'languageroutine', 'lousylinguist', 'glutton4langs', 'languagesandme', 'loveguages']

    for public in tqdm(publics):
        data_frame = get_wall(domain=public, count=0).to_string()
    print('got data')

    text_normalize('data_frame.txt', 'corpora.txt')
    print('texts normalized')

    texts = []
    with open('corpora.txt', 'r', encoding='utf8') as corp_file:
        for s in corp_file:
            texts.append(s.split())

    dictionary = gensim.corpora.Dictionary(texts)
    print('dictionary created')
    corpora = [dictionary.doc2bow(text) for text in texts]
    print('corpora created')

    lda_model = gensim.models.ldamodel.LdaModel(corpus=corpora, id2word=dictionary, num_topics=10)
    print('model created')
    vis = pyLDAvis.gensim.prepare(lda_model, corpora, dictionary)
    pyLDAvis.show(vis)
