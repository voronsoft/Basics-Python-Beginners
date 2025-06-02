# 6_1_2 тест для задачи
def test_6_1_2(*args):
    expected = sorted(
        [
            "d['dict'] = {'one': 1, 'two': 2}",
            "d[1] = 'one'",
            'd[5.6] = 5.6',
            "d[True] = 'истина'",
            "d[house] = ['дом', 'жилище', 'хижина']",
        ]
    )
    user_output = sorted(args[0].split(";_"))
    assert expected == user_output, "Нет, это неправильный ответ."
