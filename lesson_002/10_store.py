#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Есть словарь кодов товаров

goods = {
    'Лампа': '12345',
    'Стол': '23456',
    'Диван': '34567',
    'Стул': '45678',
}

# Есть словарь списков количества товаров на складе.

store = {
    '12345': [
        {'quantity': 27, 'price': 42},
    ],
    '23456': [
        {'quantity': 22, 'price': 510},
        {'quantity': 32, 'price': 520},
    ],
    '34567': [
        {'quantity': 2, 'price': 1200},
        {'quantity': 1, 'price': 1150},
    ],
    '45678': [
        {'quantity': 50, 'price': 100},
        {'quantity': 12, 'price': 95},
        {'quantity': 43, 'price': 97},
    ],
}

# Рассчитать на какую сумму лежит каждого товара на складе
# например для ламп

lamps_cost = store[goods['Лампа']][0]['quantity'] * store[goods['Лампа']][0]['price']
# или проще (/сложнее ?)
lamp_code = goods['Лампа']
lamps_item = store[lamp_code][0]
lamps_quantity = lamps_item['quantity']
lamps_price = lamps_item['price']
lamps_cost = lamps_quantity * lamps_price
print('Лампа -', lamps_quantity, 'шт, стоимость', lamps_cost, 'руб')

# Вывести стоимость каждого вида товара на складе:
# один раз распечать сколько всего столов и их общая стоимость,
# один раз распечать сколько всего стульев и их общая стоимость,
#   и т.д. на складе
# Формат строки <товар> - <кол-во> шт, стоимость <общая стоимость> руб

# WARNING для знающих циклы: БЕЗ циклов. Да, с переменными; да, неэффективно; да, копипаста.
# Это задание на ручное вычисление - что бы потом понять как работают циклы и насколько с ними проще жить.

# TODO попробую переносами разделять логические блоки. Это допустимо?
table_code = goods['Стол']
tables_item_1 = store[table_code][0]
tables_item_2 = store[table_code][1]

tables_quantity = tables_item_1['quantity'] + tables_item_2['quantity']

tables_item_1_cost = tables_item_1['price'] * tables_item_1['quantity']
tables_item_2_cost = tables_item_2['price'] * tables_item_2['quantity']
total_tables_cost = tables_item_1_cost + tables_item_2_cost

print('Стол -', tables_quantity, 'шт, стоимость', total_tables_cost, 'руб')


sofa_code = goods['Диван']
sofas_item_1 = store[sofa_code][0]
sofas_item_2 = store[sofa_code][1]

sofas_quantity = sofas_item_1['quantity'] + sofas_item_2['quantity']

sofas_item_1_cost = sofas_item_1['price'] * sofas_item_1['quantity']
sofas_item_2_cost = sofas_item_2['price'] * sofas_item_2['quantity']
total_sofas_cost = sofas_item_1_cost + sofas_item_2_cost

print('Диван -', sofas_quantity, 'шт, стоимость', total_sofas_cost, 'руб')


chair_code = goods['Стул']
chairs_item_1 = store[chair_code][0]
chairs_item_2 = store[chair_code][1]
chairs_item_3 = store[chair_code][2]

chairs_quantity = chairs_item_1['quantity'] + chairs_item_2['quantity'] + chairs_item_3['quantity']

chairs_item_1_cost = chairs_item_1['price'] * chairs_item_1['quantity']
chairs_item_2_cost = chairs_item_2['price'] * chairs_item_2['quantity']
chairs_item_3_cost = chairs_item_3['price'] * chairs_item_3['quantity']
total_chairs_cost = chairs_item_1_cost + chairs_item_2_cost + chairs_item_3_cost

print('Стул -', chairs_quantity, 'шт, стоимость', total_chairs_cost, 'руб')

##########################################################################################
# ВНИМАНИЕ! После того как __ВСЯ__ домашняя работа сделана и запушена на сервер,         #
# нужно зайти в ЛМС (LMS - Learning Management System ) по адресу http://go.skillbox.ru  #
# и оформить попытку сдачи ДЗ! Без этого ДЗ не будет проверяться!                        #
# Как оформить попытку сдачи смотрите видео - https://youtu.be/qVpN0L-C3LU               #
##########################################################################################






