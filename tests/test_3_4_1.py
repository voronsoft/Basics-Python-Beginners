# 3_4_1 тест для задачи
def test_3_4_1(*args):

    expected = dict(
        sorted(
            {
                '\\N': 'Перевод строки',
                '\\\\': 'Символ обратного слеша',
                '\\’': 'Символ апострофа (одинарной кавычки)',
                '\\"': 'Символ двойной кавычки',
                '\\B': 'Эмуляция клавиши BackSpace',
                '\\R': 'Возврат каретки',
                '\\T': 'Горизонтальная табуляция',
            }.items()
        )
    )

    user_output = dict(sorted(args[0].items()))
    print(expected)
    print(user_output)
    assert expected == user_output, "Нет, это неправильный ответ."
