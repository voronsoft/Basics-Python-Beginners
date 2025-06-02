# 3_6_11 тест для задачи
def test_3_6_11(*args):
    expected = dict(
        sorted(
            {
                '*': 'дублирование списка',
                '+': 'соединение двух списков в один',
                'del': 'удаление элемента списка',
                'in': 'проверка вхождения элемента в список',
            }.items()
        )
    )

    user_output = dict(sorted(args[0].items()))
    assert expected == user_output, "Нет, это неправильный ответ."
