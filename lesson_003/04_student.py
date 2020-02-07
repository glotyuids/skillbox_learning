# -*- coding: utf-8 -*-

# (цикл while)

# Ежемесячная стипендия студента составляет educational_grant руб., а расходы на проживание превышают стипендию
# и составляют expenses руб. в месяц. Рост цен ежемесячно увеличивает расходы на 3%, кроме первого месяца
# Составьте программу расчета суммы денег, которую необходимо единовременно попросить у родителей,
# чтобы можно было прожить учебный год (10 месяцев), используя только эти деньги и стипендию.
# Формат вывода:
#   Студенту надо попросить ХХХ.ХХ рублей

educational_grant, expenses = 10000, 12000

annual_grant = educational_grant * 10
last_month_expenses = expenses
total_expenses = last_month_expenses
month = 1
# Если бы не малоинформативное название переменной для номера текущего месяца "i", то зачёл бы. Но именование
#  очень важно и к этому надо привыкать сразу. Потратить на поиск подходящего имени много времени не жаль. Конечно, в
#  данном случае достаточно очевидно назначение i, но ради практики важно заостить на этом внимание
#  TODO Фактически тут и цикл while не особо нужен. Достаточно было бы for _ in range(9)
while month < 10:
    last_month_expenses *= 1.03
    total_expenses += last_month_expenses
    month += 1

borrow_from_parents = round(total_expenses - annual_grant, 2)
print(f'Студенту надо попросить {borrow_from_parents} рублей')

