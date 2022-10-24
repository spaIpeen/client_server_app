"""
2. Задание на закрепление знаний по модулю json. Есть файл orders в формате JSON с информацией о заказах.
Написать скрипт, автоматизирующий его заполнение данными. Для этого:
Создать функцию write_order_to_json(), в которую передается 5 параметров — товар (item), количество (quantity),
цена (price), покупатель (buyer), дата (date). Функция должна предусматривать запись данных в виде словаря в файл
orders.json. При записи данных указать величину отступа в 4 пробельных символа;
Проверить работу программы через вызов функции write_order_to_json() с передачей в нее значений каждого параметра.
"""

import json


def write_order_to_json(item, quantity, price, buyer, date):
    data = {'item': item, 'quantity': quantity, 'price': price, 'buyer': buyer, 'date': date}
    with open('orders.json') as f_r:
        obj = json.load(f_r)
        obj['orders'] += [data]

    with open('orders.json', 'w') as f_w:
        json.dump(obj, f_w, indent=4, ensure_ascii=False)


dict_a, dict_b, dict_c, dict_d = \
    {
        "item": "принтер",
        "quantity": "10",
        "price": "6700",
        "buyer": "Ivanov I.I.",
        "date": "24.09.2017"
    }, \
    {
        "item": "scaner",
        "quantity": "20",
        "price": "10000",
        "buyer": "Petrov P.P.",
        "date": "11.01.2018"
    }, \
    {
        "item": "scaner",
        "quantity": "20",
        "price": "10000",
        "buyer": "Петров P.P.",
        "date": "11.01.2018"
    }, \
    {
        "item": "scaner",
        "quantity": "20",
        "price": "10000",
        "buyer": "Petrov P.P.",
        "date": "11.01.2018"
    }
dicts = [dict_a, dict_b, dict_c, dict_d]

for d in dicts:
    write_order_to_json(d['item'], d['quantity'], d['price'], d['buyer'], d['date'])
