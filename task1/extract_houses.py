from dbfread import DBF
from tqdm import tqdm
import os
import sys

vo = '36'
voronezh = '36000001'

# сокращения объектов 5-ого уровня классификации
socrs = {
    'аал': 'Аал',
    'аллея': 'Аллея',
    'арбан': 'Арбан',
    'аул': 'Аул',
    'б-р': 'Бульвар',
    'вал': 'Вал',
    'въезд': 'Въезд',
    'высел': 'Выселки(ок)',
    'городок': 'Городок',
    'гск': 'Гаражно-строительный кооператив',
    'д': 'Деревня',
    'дор': 'Дорога',
    'ж/д_будка': 'Железнодорожная будка',
    'ж/д_казарм': 'Железнодорожная казарма',
    'ж/д_оп': 'ж/д остановочный (обгонный) пункт',
    'ж/д_платф': 'Железнодорожная платформа',
    'ж/д_пост': 'Железнодорожный пост',
    'ж/д_рзд': 'Железнодорожный разъезд',
    'ж/д_ст': 'Железнодорожная станция',
    'жт': 'Животноводческая точка',
    'заезд': 'Заезд',
    'зона': 'зона',
    'казарма': 'Казарма',
    'канал': 'Канал',
    'кв-л': 'Квартал',
    'км': 'Километр',
    'кольцо': 'Кольцо',
    'коса': 'Коса',
    'линия': 'Линия',
    'лпх': 'Леспромхоз',
    'м': 'Местечко',
    'мкр': 'Микрорайон',
    'мост': 'Мост',
    'наб': 'Набережная',
    'нп': 'Населенный пункт',
    'остров': 'Остров',
    'п': 'Поселок',
    'п/о': 'Почтовое отделение',
    'п/р': 'Планировочный район',
    'п/ст': 'Поселок и(при) станция(и)',
    'парк': 'Парк',
    'пер': 'Переулок',
    'переезд': 'Переезд',
    'пл': 'Площадь',
    'пл-ка': 'Площадка',
    'платф': 'Платформа',
    'полуст': 'Полустанок',
    'починок': 'Починок',
    'пр-кт': 'Проспект',
    'проезд': 'Проезд',
    'просек': 'Просек',
    'проселок': 'Проселок',
    'проток': 'Проток',
    'проулок': 'Проулок',
    'рзд': 'Разъезд',
    'с': 'Село',
    'сад': 'Сад',
    'сквер': 'Сквер',
    'сл': 'Слобода',
    'снт': 'Садовое некоммерческое товарищество',
    'спуск': 'Спуск',
    'ст': 'Станция',
    'стр': 'Строение',
    'тер': 'Территория',
    'тракт': 'Тракт',
    'туп': 'Тупик',
    'ул': 'Улица',
    'уч-к': 'Участок',
    'ферма': 'Ферма',
    'х': 'Хутор',
    'ш': 'Шоссе',
}

# Путь к разархивированому КЛАДР'у
path = sys.argv[1]


def get_db(name: str) -> DBF:
    return DBF(os.path.join(path, '{}.DBF'.format(name)), encoding='cp866')


def cladr_code(code: str) -> str:
    """
    Возвращает код объекта 4-ого уровня классификации
    :param code: код объекта
    """
    return code[8:11]


def street_code(code: str) -> str:
    """
    Возвращает код объекта 5-ого уровня классификации
    :param code: код объекта как миниму 5-ого уровня (длина кода должна быть не менее 15)
    :return:
    """
    return code[8:15]


def process_house(name: str) -> str:
    if name.startswith('влд'):
        return 'владение ' + name[3:]
    return name

'''to write to file
with open('cladr', 'w') as f:
    print('code;name;socr;', file=f)
    for r in tqdm(get_db('KLADR')):
        if r['CODE'].startswith(v) and r['CODE'].endswith('00'):
            print("{};{};{}".format(cladr_code(r['CODE']), r['NAME'], r['SOCR']), file=f)

with open('street', 'w') as f:
    print('code;name', file=f)
    for r in tqdm(get_db('STREET')):
        if r['CODE'].startswith(v) and r['CODE'].endswith('00'):
            print("{};{}".format(street_code(r['CODE']), socrs[r['SOCR']] + ' ' + r['NAME']), file=f)

Read from file
cladr = dict(line.strip().split(';')[:2] for line in open('cladr').readlines()[1:])
street = dict(line.strip().split(';')[:2] for line in open('street').readlines()[1:])
'''

'''One way to get data
print('precessing cladr')
cladr = {}
for r in tqdm(get_db('KLADR')):
    if r['CODE'].startswith(voronezh) and r['CODE'].endswith('00'):
        cladr[cladr_code(r['CODE'])] = r['NAME']

print('processing streets')
street = {}
for r in tqdm(get_db('STREET')):
    if r['CODE'].startswith(voronezh) and r['CODE'].endswith('00'):
        street[street_code(r['CODE'])] = socrs[r['SOCR']] + ' ' + r['NAME']
'''

# More functional way (little bit faster (~.2--2 sec))
print('processing cladr...')
cladr = {
    cladr_code(r['CODE']): r['NAME']
    for r in tqdm(get_db('KLADR'))
    if r['CODE'].startswith(voronezh) and r['CODE'].endswith('00')
}

print('processing streets...')
street = {
    street_code(r['CODE']): socrs[r['SOCR']] + ' ' + r['NAME']
    for r in tqdm(get_db('STREET'))
    if r['CODE'].startswith(voronezh) and r['CODE'].endswith('00')
}

print('processing houses...')
with open(os.path.join(path, 'houses_from_cladr.csv'), 'w') as f:
    # print('дом,улица,город,область', file=f)
    template = '{} {} Воронеж Воронежская область'
    for r in tqdm(get_db('DOMA')):
        if r['CODE'].startswith(voronezh):
            for d in r['NAME'].split(','):
                if not d.startswith('соор'):
                    try:
                        print(template.format(
                            process_house(d),
                            street[street_code(r['CODE'])]
                        ), file=f)
                    except (KeyError, UnicodeEncodeError):
                        print(d)
