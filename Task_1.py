# По ссылке https://www.liveinternet.ru/rating/ можно посмотреть рейтинги сайтов рунета.
# На каждой странице представлены 30 сайтов, где рядом с описанием сайта есть количество посетителей за день.
# Для ответа на вопрос предлагается следующий алгоритм:
# 1 (2 балла) Скачаем информацию об описании сайта и количестве посетителей.
# И так для каждой из первых 20 страниц. Получится топ. 600 сайтов.
# Считаем, что остальные не смогут внести вклад в определение главых тематик рунета.
# 2 (2 балла) Разобьем описание сайта на слова, очистим их от знаков препинания и приведем к нижнему регистру.
# Опционально вы можете лемматизировать слова с помощью библиотеки pymorphy2 (ее сперва придется установить).
# 3 (1 балл) Заведем словарь (или defaultdict), куда в качестве ключей будем добавлять полученные слова,
# а в качестве значений - суммарное количество посетителей сайтов в описании которых употребляется данное слово.
# 4 (2 балла) Выведем топ 100 популярных слов. Они нам и подскажут самые популярные тематики в рунете.
# 5 (1 балл) Получившийся топ кажется немного странным.
# Расскажите, как еще можно было бы ответить на вопрос с помощью сайта liveinternet.ru/rating/ ?

import requests
import pymorphy2
import string
import re
import collections

morph = pymorphy2.MorphAnalyzer()
page = 1
content_all = ''
all = []
pattern = re.compile("всего[\s]\d{6}[\s]\d{1}[\s]\d{1}")


while page <= 20:
    """Добавление первых 20-ти страниц с сайтами(пункт 1) """
    response = requests.get('https://www.liveinternet.ru/rating///today.tsv?page={}'.format(page))
    content = response.text
    formating_content = content.replace('\t', ' ')
    formating_content = re.sub(pattern, '', formating_content)
    formating_content = re.sub(r'&quot;', '', formating_content)
    content_all += formating_content
    page += 1

for line in content_all.split('\n'):
    """Форматирование контента(пункт 2)"""
    formating_line = line.replace('—', '').replace(',', '').lower()
    all.append(formating_line)
    all = list(filter(None, all))

remove = string.punctuation
big_d = {}

for item in all:
    """(пункт 3)"""
    item = re.sub('[{}]'.format(remove), '', item)
    item = item.split(' ')
    item = list(filter(None, item))
    d = dict.fromkeys(item[2:-3], item[-3])
    big_d.update(d)

top = collections.Counter(big_d.keys())
print(top)



