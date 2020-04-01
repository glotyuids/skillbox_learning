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


#  Для того, чтобы упростить себе работу, сложение я организовал таким образом:
#  Есть два списка: список классов элементов, с которым можно сложить текущий, и список классов - результатов сложения.
#  Соответственно, в первом списке ищем класс переданного элемента,
#  а из второго дёргаем класс с соответствующим номером и возвращаем объект этого класса

# Идея прикольная, только эти две константы должны быть атрибутами класса, а ещё лучше сделать это словарём где
#  ключ объект из elements, а значение элемент из results.

#  Я хотел вынести списки в атрибуты класса, но интерпретатор ругался на то, что элементы списка ещё не определены.
#   Два списка словарём заменил
# TODO Что-то не так сделали, покажите

#  Но самый шик был бы вложенный словарь один на все элементы, типа таблицы умножения где ряд числа в левой колонке
#  пересекатся с колонкой числа в верхней строке и так находится результат.
#  Что-то типа (но это будет работать только после определения классов):
# MAGIC_JAR = {}
# MAGIC_JAR[Water] = {}
# MAGIC_JAR[Water][Air] = Storm
#  Но эта задача просто на применение на практике функции isinstance, а тут похоже она и не пригодится.

#  Я подумывал как раз о подобном решении,
#  но в итоге пришёл к выводу, что для данного задания это будет уже оверкилл.
#  Хотя, можно попробовать, но тогда уже не нужна будет сама перегрузка оператора сложения,
#  поскольку вся арифметика будет осуществляться в основном коде программы

#  Реализовал такой подход ниже


class Water:

    def __str__(self):
        return 'Вода'

    def __add__(self, other):
        # elements = [Water, Air, Fire, Earth, Storm, Steam, Mud, Lighting, Dust, Lava]
        # results = [Puddle, Storm, Steam, Mud, Flood, Mist, Swamp, Plasma, Mud, Stone]

        adding_results = {
            Water: Puddle, Air: Storm, Fire: Steam, Earth: Mud,
            Storm: Flood, Steam: Mist, Mud: Swamp, Lighting: Plasma,
            Dust: Mud, Lava: Stone
        }
        # ToDO Сделайте эту переменную атрибутом класса (константой) и обьявите в __init__
        # for i, element in enumerate(elements):
        #     if isinstance(other, element):
        if type(other) in adding_results:
            return adding_results[type(other)]()
        return None


class Air:
    def __str__(self):
        return 'Воздух'

    def __add__(self, other):
        adding_results = {
            Water: Storm, Air: Air, Fire: Lighting, Earth: Dust,
            Storm: Mist, Steam: Mist, Mud: Dust, Lighting: Plasma,
            Dust: Storm, Lava: Stone,
        }
        if type(other) in adding_results:
            return adding_results[type(other)]()
        return None


class Fire:
    def __str__(self):
        return 'Огонь'

    def __add__(self, other):
        adding_results = {
            Water: Steam, Air: Lighting, Fire: Fire, Earth: Lava,
            Storm: Steam, Steam: Water, Mud: Earth, Lighting: Plasma,
            Dust: Lava, Lava: Lava,
        }
        if type(other) in adding_results:
            return adding_results[type(other)]()
        return None


class Earth:
    def __str__(self):
        return 'Земля'

    def __add__(self, other):
        adding_results = {
            Water: Mud, Air: Dust, Fire: Lava, Earth: Earth,
            Storm: Flood, Steam: Mud, Mud: Mud, Lighting: Stone,
            Dust: Dust, Lava: Stone,
        }
        if type(other) in adding_results:
            return adding_results[type(other)]()
        return None


class Storm:
    def __str__(self):
        return 'Шторм'

    def __add__(self, other):
        adding_results = {
            Water: Flood, Air: Mist, Fire: Steam, Earth: Flood,
            Storm: Flood, Steam: Lighting, Mud: Swamp, Lighting: Flood,
            Dust: Swamp, Lava: Stone,
        }
        if type(other) in adding_results:
            return adding_results[type(other)]()
        return None


class Steam:
    def __str__(self):
        return 'Пар'

    def __add__(self, other):
        adding_results = {
            Water: Mist, Air: Mist, Fire: Water, Earth: Mud,
            Storm: Lighting, Steam: Lighting, Mud: Swamp, Lighting: Plasma,
            Dust: Mud, Lava: Stone,
        }
        if type(other) in adding_results:
            return adding_results[type(other)]()
        return None


class Mud:
    def __str__(self):
        return 'Грязь'

    def __add__(self, other):
        adding_results = {
            Water: Swamp, Air: Dust, Fire: Earth, Earth: Mud,
            Storm: Swamp, Steam: Swamp, Mud: Swamp, Lighting: Stone,
            Dust: Earth, Lava: Stone,
        }
        if type(other) in adding_results:
            return adding_results[type(other)]()
        return None


class Lighting:
    def __str__(self):
        return 'Молния'

    def __add__(self, other):
        adding_results = {
            Water: Plasma, Air: Plasma, Fire: Plasma, Earth: Stone,
            Storm: Flood, Steam: Plasma, Mud: Stone, Lighting: Plasma,
            Dust: Stone, Lava: Plasma,
        }
        if type(other) in adding_results:
            return adding_results[type(other)]()
        return None


class Dust:
    def __str__(self):
        return 'Пыль'

    def __add__(self, other):
        adding_results = {
            Water: Mud, Air: Storm, Fire: Lava, Earth: Dust,
            Storm: Swamp, Steam: Mud, Mud: Earth, Lighting: Stone,
            Dust: Earth, Lava: Lava,
        }
        if type(other) in adding_results:
            return adding_results[type(other)]()
        return None


class Lava:
    def __str__(self):
        return 'Лава'

    def __add__(self, other):
        adding_results = {
            Water: Stone, Air: Stone, Fire: Lava, Earth: Stone,
            Storm: Stone, Steam: Stone, Mud: Stone, Lighting: Plasma,
            Dust: Lava, Lava: Lava,
        }
        if type(other) in adding_results:
            return adding_results[type(other)]()
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


ADDING_RESULTS = {
    Water: {
        Water: Puddle, Air: Storm, Fire: Steam, Earth: Mud, Storm: Flood, Steam: Mist, Mud: Swamp, Lighting: Plasma,
        Dust: Mud, Lava: Stone
    },
    Air: {
        Air: Air, Fire: Lighting, Earth: Dust, Storm: Mist, Steam: Mist, Mud: Dust, Lighting: Plasma, Dust: Storm,
        Lava: Stone,
    },
    Fire: {
        Fire: Fire, Earth: Lava, Storm: Steam, Steam: Water, Mud: Earth, Lighting: Plasma, Dust: Lava, Lava: Lava,
    },
    Earth: {
        Earth: Earth, Storm: Flood, Steam: Mud, Mud: Mud, Lighting: Stone, Dust: Dust, Lava: Stone,
    },
    Storm: {
        Storm: Flood, Steam: Lighting, Mud: Swamp, Lighting: Flood, Dust: Swamp, Lava: Stone,
    },
    Steam: {
        Steam: Lighting, Mud: Swamp, Lighting: Plasma, Dust: Mud, Lava: Stone,
    },
    Mud: {
        Mud: Swamp, Lighting: Stone, Dust: Earth, Lava: Stone,
    },
    Lighting: {
        Lighting: Plasma, Dust: Stone, Lava: Plasma,
    },
    Dust: {
        Dust: Earth, Lava: Lava,
    },
    Lava: {
        Lava: Lava,
    }
}


def add_elements(first_element, second_element):
    if type(second_element) in ADDING_RESULTS[type(first_element)]:
        return ADDING_RESULTS[type(first_element)][type(second_element)]()
    if type(first_element) in ADDING_RESULTS[type(second_element)]:
        return ADDING_RESULTS[type(second_element)][type(first_element)]()
    return None


#  Если речь зашла о словаре-таблице, то такие таблица и функция сложения
#  позволят сохранить коммутативность сложения, при этом избежав дублирования пар слагаемых в таблице
#  и, соответственно, избежать ошибок при добавлении новых элементов,
#  поскольку результат нужно будет внести в таблицу только один раз для любого из слагаемых
# TODO Красота! Надеюсь isinstance знаете? А то я беспокоюсь чисто за методологию курса,
#  так как именно применение этой функции  является целью задачи.

print(Water(), '+', Air(), '=', Water() + Air())
print(Water(), '+', Air(), '=', add_elements(Water(), Air()))
print()

print(Fire(), '+', Air(), '=', Fire() + Air())
print(Fire(), '+', Air(), '=', add_elements(Fire(), Air()))
print()

print(Earth(), '+', Air(), '=', Earth() + Air())
print(Earth(), '+', Air(), '=', add_elements(Earth(), Air()))
print()

print(Mud(), '+', Dust(), '=', Mud() + Dust())
print(Mud(), '+', Dust(), '=', add_elements(Mud(), Dust()))
# Усложненное задание (делать по желанию)
# Добавить еще элемент в игру.
# Придумать что будет при сложении существующих элементов с новым.
