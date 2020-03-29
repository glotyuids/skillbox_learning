# -*- coding: utf-8 -*-

# Создать прототип игры Алхимия: при соединении двух элементов получается новый.
# Реализовать следующие элементы: Вода, Воздух, Огонь, Земля, Шторм, Пар, Грязь, Молния, Пыль, Лава.
# Каждый элемент организовать как отдельный класс.
# Таблица преобразований:
#   Вода + Воздух = Шторм
#   Вода + Огонь = Пар
#   Вода + Земля = Грязь
#   Воздух + Огонь = Молния
#   Воздух + Земля = Пыль
#   Огонь + Земля = Лава

# Сложение элементов реализовывать через __add__
# Если результат не определен - то возвращать None
# Вывод элемента на консоль реализовывать через __str__
#
# Примеры преобразований:
#   print(Water(), '+', Air(), '=', Water() + Air())
#   print(Fire(), '+', Air(), '=', Fire() + Air())


# TODO Для того, чтобы упростить себе работу, сложение я организовал таким образом:
#  Есть два списка: список классов элементов, с которым можно сложить текущий, и список классов - результатов сложения.
#  Соответственно, в первом списке ищем класс переданного элемента,
#  а из второго дёргаем класс с соответствующим номером и возвращаем объект этого класса


class Water:

    def __str__(self):
        return 'Вода'

    def __add__(self, other):
        elements = [Water, Air, Fire, Earth, Storm, Steam, Mud, Lighting, Dust, Lava]
        results = [Puddle, Storm, Steam, Mud, Flood, Mist, Swamp, Plasma, Mud, Stone]
        for i, element in enumerate(elements):
            if isinstance(other, element):
                return results[i]()
        return None


class Air:
    def __str__(self):
        return 'Воздух'

    def __add__(self, other):
        elements = [Water, Air, Fire, Earth, Storm, Steam, Mud, Lighting, Dust, Lava]
        results = [Storm, Air, Lighting, Dust, Mist, Mist, Dust, Plasma, Storm, Stone]
        for i, element in enumerate(elements):
            if isinstance(other, element):
                return results[i]()
        return None


class Fire:
    def __str__(self):
        return 'Огонь'

    def __add__(self, other):
        elements = [Water, Air, Fire, Earth, Storm, Steam, Mud, Lighting, Dust, Lava]
        results = [Steam, Lighting, Fire, Lava, Steam, Water, Earth, Plasma, Lava, Lava]
        for i, element in enumerate(elements):
            if isinstance(other, element):
                return results[i]()
        return None


class Earth:
    def __str__(self):
        return 'Земля'

    def __add__(self, other):
        elements = [Water, Air, Fire, Earth, Storm, Steam, Mud, Lighting, Dust, Lava]
        results = [Mud, Dust, Lava, Earth, Flood, Mud, Mud, Stone, Dust, Stone]
        for i, element in enumerate(elements):
            if isinstance(other, element):
                return results[i]()
        return None


class Storm:
    def __str__(self):
        return 'Шторм'

    def __add__(self, other):
        elements = [Water, Air, Fire, Earth, Storm, Steam, Mud, Lighting, Dust, Lava]
        results = [Flood, Mist, Steam, Flood, Flood, Lighting, Swamp, Flood, Swamp, Stone]
        for i, element in enumerate(elements):
            if isinstance(other, element):
                return results[i]()
        return None


class Steam:
    def __str__(self):
        return 'Пар'

    def __add__(self, other):
        elements = [Water, Air, Fire, Earth, Storm, Steam, Mud, Lighting, Dust, Lava]
        results = [Mist, Mist, Water, Mud, Lighting, Lighting, Swamp, Plasma, Mud, Stone]
        for i, element in enumerate(elements):
            if isinstance(other, element):
                return results[i]()
        return None


class Mud:
    def __str__(self):
        return 'Грязь'

    def __add__(self, other):
        elements = [Water, Air, Fire, Earth, Storm, Steam, Mud, Lighting, Dust, Lava]
        results = [Swamp, Dust, Earth, Mud, Swamp, Swamp, Swamp, Stone, Earth, Stone]
        for i, element in enumerate(elements):
            if isinstance(other, element):
                return results[i]()
        return None


class Lighting:
    def __str__(self):
        return 'Молния'

    def __add__(self, other):
        elements = [Water, Air, Fire, Earth, Storm, Steam, Mud, Lighting, Dust, Lava]
        results = [Plasma, Plasma, Plasma, Stone, Flood, Plasma, Stone, Plasma, Stone, Plasma]
        for i, element in enumerate(elements):
            if isinstance(other, element):
                return results[i]()
        return None


class Dust:
    def __str__(self):
        return 'Пыль'

    def __add__(self, other):
        elements = [Water, Air, Fire, Earth, Storm, Steam, Mud, Lighting, Dust, Lava]
        results = [Mud, Storm, Lava, Dust, Swamp, Mud, Earth, Stone, Earth, Lava]
        for i, element in enumerate(elements):
            if isinstance(other, element):
                return results[i]()
        return None


class Lava:
    def __str__(self):
        return 'Лава'

    def __add__(self, other):
        elements = [Water, Air, Fire, Earth, Storm, Steam, Mud, Lighting, Dust, Lava]
        results = [Stone, Stone, Lava, Stone, Stone, Stone, Stone, Plasma, Lava, Lava]
        for i, element in enumerate(elements):
            if isinstance(other, element):
                return results[i]()
        return None


class Puddle:
    def __str__(self):
        return 'Лужа'


class Flood:
    def __str__(self):
        return 'Потоп'


class Mist:
    def __str__(self):
        return 'Туман'


class Swamp:
    def __str__(self):
        return 'Болото'


class Plasma:
    def __str__(self):
        return 'Плазма'


class Stone:
    def __str__(self):
        return 'Камень'


print(Water(), '+', Air(), '=', Water() + Air())
print(Fire(), '+', Air(), '=', Fire() + Air())
print(Earth(), '+', Air(), '=', Earth() + Air())

print(Mud(), '+', Dust(), '=', Mud() + Dust())
# Усложненное задание (делать по желанию)
# Добавить еще элемент в игру.
# Придумать что будет при сложении существующих элементов с новым.
