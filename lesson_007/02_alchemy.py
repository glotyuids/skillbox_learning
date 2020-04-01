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

# Что-то не так сделали, покажите

# TODO предположим, пусть будет условный Fire2
# class Fire2:
#     ADDING_RESULTS = {
#         Water: Steam, Air: Lighting, Fire: Fire, Earth: Lava,
#         Storm: Steam, Steam: Water, Mud: Earth, Lighting: Plasma,
#         Dust: Lava, Lava: Lava,
#     }
# TODO Как я понял, это будет работать только в том случае, если я объявил все используемые классы ранее.
#  Так что сделаю так, как предложили вы - буду объявлять в __init__

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

# adding_results = {}
# Сделайте эту переменную атрибутом класса (константой) и обьявите в __init__
# TODO Объявить в __init__? Вы натолкнули меня на мысль...
#  Меня гнетёт куча повторяющегося кода в классах (честно, ощущаю физический дискомфорт),
#  поэтому можно я попробую забежать чуть-чуть вперёд и создам суперкласс Element, от которого унаследую все остальные?
#  Понадеюсь только, что всё делаю правильно


class Element:
    # TODO Атрибут приватный, поскольку нормально использовать его вне класса не получится,
    #  пока не будет создан хотя бы один экземпляр этого класса.
    _ADDING_RESULTS = {}
    _NAME = ''

    # TODO Я правильно обращаюсь к атрибутам класса?
    #  Потому что если обращаться просто через self, то получится обращение к атрибутам объекта
    def __str__(self):
        return type(self)._NAME

    def __add__(self, other):
        if type(other) in type(self)._ADDING_RESULTS:
            return type(self)._ADDING_RESULTS[type(other)]()
        return None


class Water(Element):
    def __init__(self):
        Water._NAME = 'Вода'
        Water._ADDING_RESULTS = {
            Water: Puddle, Air: Storm, Fire: Steam, Earth: Mud,
            Storm: Flood, Steam: Mist, Mud: Swamp, Lighting: Plasma,
            Dust: Mud, Lava: Stone
        }


class Air(Element):
    def __init__(self):
        Air._NAME = 'Воздух'
        Air._ADDING_RESULTS = {
            Water: Storm, Air: Air, Fire: Lighting, Earth: Dust,
            Storm: Mist, Steam: Mist, Mud: Dust, Lighting: Plasma,
            Dust: Storm, Lava: Stone,
        }


class Fire(Element):
    def __init__(self):
        Fire._NAME = 'Огонь'
        Fire._ADDING_RESULTS = {
            Water: Steam, Air: Lighting, Fire: Fire, Earth: Lava,
            Storm: Steam, Steam: Water, Mud: Earth, Lighting: Plasma,
            Dust: Lava, Lava: Lava,
        }


class Earth(Element):
    def __init__(self):
        Earth._NAME = 'Земля'
        Earth._ADDING_RESULTS = {
            Water: Mud, Air: Dust, Fire: Lava, Earth: Earth,
            Storm: Flood, Steam: Mud, Mud: Mud, Lighting: Stone,
            Dust: Dust, Lava: Stone,
        }


class Storm(Element):
    def __init__(self):
        Storm._NAME = 'Шторм'
        Storm._ADDING_RESULTS = {
            Water: Flood, Air: Mist, Fire: Steam, Earth: Flood,
            Storm: Flood, Steam: Lighting, Mud: Swamp, Lighting: Flood,
            Dust: Swamp, Lava: Stone,
        }


class Steam(Element):
    def __init__(self):
        Stone._NAME = 'Пар'
        Steam._ADDING_RESULTS = {
            Water: Mist, Air: Mist, Fire: Water, Earth: Mud,
            Storm: Lighting, Steam: Lighting, Mud: Swamp, Lighting: Plasma,
            Dust: Mud, Lava: Stone,
        }


class Mud(Element):
    def __init__(self):
        Mud._NAME = 'Грязь'
        Mud._ADDING_RESULTS = {
            Water: Swamp, Air: Dust, Fire: Earth, Earth: Mud,
            Storm: Swamp, Steam: Swamp, Mud: Swamp, Lighting: Stone,
            Dust: Earth, Lava: Stone,
        }


class Lighting(Element):
    def __init__(self):
        Lighting._NAME = 'Молния'
        Lighting._ADDING_RESULTS = {
            Water: Plasma, Air: Plasma, Fire: Plasma, Earth: Stone,
            Storm: Flood, Steam: Plasma, Mud: Stone, Lighting: Plasma,
            Dust: Stone, Lava: Plasma,
        }


class Dust(Element):
    def __init__(self):
        Dust._NAME = 'Пыль'
        Dust._ADDING_RESULTS = {
            Water: Mud, Air: Storm, Fire: Lava, Earth: Dust,
            Storm: Swamp, Steam: Mud, Mud: Earth, Lighting: Stone,
            Dust: Earth, Lava: Lava,
        }


class Lava(Element):
    def __init__(self):
        Lava._NAME = 'Лава'
        Lava._ADDING_RESULTS = {
            Water: Stone, Air: Stone, Fire: Lava, Earth: Stone,
            Storm: Stone, Steam: Stone, Mud: Stone, Lighting: Plasma,
            Dust: Lava, Lava: Lava,
        }


class Puddle(Element):
    def __init__(self):
        Puddle._NAME = 'Лужа'


class Flood(Element):
    def __init__(self):
        Flood._NAME = 'Потоп'


class Mist(Element):
    def __init__(self):
        Mist._NAME = 'Туман'


class Swamp(Element):
    def __init__(self):
        Swamp._NAME = 'Болото'


class Plasma(Element):
    def __init__(self):
        Plasma._NAME = 'Плазма'


class Stone(Element):
    def __init__(self):
        Stone._NAME = 'Камень'


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

# Красота! Надеюсь isinstance знаете? А то я беспокоюсь чисто за методологию курса,
#  так как именно применение этой функции  является целью задачи.

# TODO Само собой, isinstance знаю - функция в качестве аргументов принимает экземпляр и класс/кортеж классов,
#  возвращает флаг соответствия экземпляра классу/какому-либо классу из кортежа.
#  Просто в стремлении избежать механического бездумного набивания if isinstance(other, ...)
#  я получил алгоритм, который не потребовал её применения ¯\_(ツ)_/¯
#  Опять же, вы можете глянуть в предыдущих коммитах закомментированный код,
#  который я специально оставил в Water.__add__().
#  Он изначально использовался для поиска второго слагаемого в списке элементов именно с помощью isinstance()

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
