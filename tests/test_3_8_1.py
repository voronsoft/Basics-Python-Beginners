# 3_8_1 тест для задачи
def test_3_8_1(*args):

    expected = dict(
        sorted(
            {
                'append': 'Добавляет элемент в конец списка',
                'insert': 'Вставляет элемент в указанное место списка',
                'remove': 'Удаляет элемент по значению',
                'pop': 'Удаляет последний элемент, либо элемент с указанным индексом',
                'clear': 'Очищает список (удаляет все элементы)',
            }.items()
        )
    )

    user_output = dict(sorted(args[0].items()))
    # print(expected)
    # print(user_output)
    assert expected == user_output, "Нет, это неправильный ответ."
