# -*- coding: utf-8 -*-

# Создать модуль my_burger. В нем определить функции добавления инградиентов:
#  - булочки
#  - котлеты
#  - огурчика
#  - помидорчика
#  - майонеза
#  - сыра
# В каждой функции выводить на консоль что-то вроде "А теперь добавим ..."

# В этом модуле создать рецепт двойного чизбургера (https://goo.gl/zA3goZ)
# с помощью фукций из my_burger и вывести на консоль.

# Создать рецепт своего бургера, по вашему вкусу.
# Если не хватает инградиентов - создать соответствующие функции в модуле my_burger

import my_burger as burger

burger.add_bun()
burger.add_beefsteak()
burger.add_cheese()
burger.add_cucumber()
burger.add_sauce()
burger.add_bun(top=True)

print('\n\n')

burger.add_beefsteak(my_burger=True)
burger.add_sauce(my_burger=True)
burger.add_cheese(my_burger=True)
burger.add_cucumber(my_burger=True)
burger.add_lettuce()
burger.add_onion()
burger.add_bun(my_burger=True)
burger.pack()

# зачет!
