# 8_1_7 тест для задачи
def test_8_1_7(*args):
    # Ожидается
    expected = sorted(
        [
            'from math import floor as fl, ceil as cl, pi',
            'from math import floor, ceil, pi',
            'Каждый с новой строки: import random import math import time',
        ]
    )
    # Получено
    user_output = sorted(args[0].split(";_"))

    assert expected == user_output, "Нет, это неправильный ответ."
