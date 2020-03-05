# -*- coding: utf-8 -*-

# Составить список всех живущих на районе и Вывести на консоль через запятую
# Формат вывода: На районе живут ...
# подсказка: для вывода элементов списка через запятую можно использовать функцию строки .join()
# https://docs.python.org/3/library/stdtypes.html#str.join


import district.central_street.house1.room1 as central_house1_room1
import district.central_street.house1.room2 as central_house1_room2
import district.central_street.house2.room1 as central_house2_room1
import district.central_street.house2.room2 as central_house2_room2
import district.soviet_street.house1.room1 as soviet_house1_room1
import district.soviet_street.house1.room2 as soviet_house1_room2
import district.soviet_street.house2.room1 as soviet_house2_room1
import district.soviet_street.house2.room2 as soviet_house2_room2


district_rooms = [
    central_house1_room1, central_house1_room2,
    central_house2_room1, central_house2_room2,
    soviet_house1_room1, soviet_house1_room2,
    soviet_house2_room1, soviet_house2_room2,
]

district_residents = []
for room in district_rooms:
    district_residents.extend(room.folks)

print('На районе живут', ', '.join(district_residents))



