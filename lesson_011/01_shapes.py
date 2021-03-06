# -*- coding: utf-8 -*-

# TODO с вашего позволения и несмотря на ответ Владимира в чате,
#  я всё таки пофиксил баг с накоплением погрешности вычисления конечных точек векторов.
#  Владимира смутили дробные точки (могу понять почему - это ненужное дополнительное усложнение для учащихся),
#  но дробные координаты вполне успешно используются, например, в движке Source (в Half-Life 2 1 см равен 0.39 юнитов),
#  поэтому я счёл, что хотя бы для себя я могу этот баг пофиксить.
#  -
#  По сути, весь фикс сводится к хранению координат в виде натуральных чисел
#  и приведению их к целым при приведении к экранной системе координат.
#  -
#  И чтобы не таскать за собой всю библиотеку, воспользуемся наследованием.
#  Очевидно, что если в библиотеке хватило бы исправлений в 4 строках (448, 449, 460, 468),
#  то здесь придётся поработать несколько больше, переопределив 4 метода (и два попутно) в двух классах
#  -
#  Корректность работы можете проверить, увеличив количество сторон полигона хотя бы до 30
import numpy
import simple_draw as sd


class FloatPoint(sd.Point):
    def __init__(self, x=None, y=None, *args, **kwargs):
        super().__init__(x, y, *args, **kwargs)
        self._x = 0.0 if x is None else float(x)
        self._y = 0.0 if y is None else float(y)

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = value

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = value


class FloatVector(sd.Vector):
    @property
    def end_point(self):
        return FloatPoint(self.start_point.x + self.dx, self.start_point.y + self.dy, )

# На основе вашего кода из решения lesson_004/01_shapes.py сделать функцию-фабрику,
# которая возвращает функции рисования треугольника, четырехугольника, пятиугольника и т.д.
#
# Функция рисования должна принимать параметры
# - точка начала рисования
# - угол наклона
# - длина стороны
#
# Функция-фабрика должна принимать параметр n - количество сторон.


def get_polygon(n):
    def draw_polygon(point=None, angle=0.0, length=10):
        if not isinstance(point, (sd.Point, FloatPoint)):
            raise TypeError(f'Incorrect point object: expected Point or FloatPoint, got {type(point).__name__}')
        angle_step = 360 / n
        next_start_point = point
        # если итерироваться по numpy.arange(angle, 360 + angle, angle_step), то точность будет несколько выше,
        # но разница пляшет в районе 12 знака после запятой, поэтому смысла тащить сюда numpy нет
        for i in range(1, n + 1):
            v = FloatVector(start_point=next_start_point, direction=angle + angle_step * i, length=length)
            v.draw(color=sd.COLOR_YELLOW, width=1)
            next_start_point = v.end_point
    return draw_polygon


draw_triangle = get_polygon(n=27)
draw_triangle(point=sd.get_point(300, 100), angle=13, length=100)


sd.pause()

# зачет! Интересная работа! Но почему-то при числе граней 21-23 и 25-28 рисует не точно
