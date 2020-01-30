#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Есть словарь координат городов

sites = {
    'Moscow': (550, 370),
    'London': (510, 510),
    'Paris': (480, 480),
}

# Составим словарь словарей расстояний между ними
# расстояние на координатной сетке - корень из (x1 - x2) ** 2 + (y1 - y2) ** 2

distances = {}


def calculate_distance(cite1, cite2):
    distance = ((cite1[0] - cite2[0]) ** 2 + (cite1[1] - cite2[1]) ** 2) ** 0.5
    return distance


moscow_london = calculate_distance(sites['Moscow'], sites['London'])
moscow_paris  = calculate_distance(sites['Moscow'], sites['Paris'])
london_paris  = calculate_distance(sites['London'], sites['Paris'])     # Голуби вверх, блики крыш...

distances['Moscow'] = {'London': moscow_london,
                       'Paris' : moscow_paris}

distances['London'] = {'Moscow': moscow_london,
                       'Paris' : london_paris}

distances['Paris']  = {'Moscow': moscow_paris,
                       'London': london_paris}


print(distances)




