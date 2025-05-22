"""
stdin_stdout_stderr_interceptor.py

Модуль с контекстным менеджером stream_interceptor для удобного перехвата и подмены стандартных потоков:
- stdin (ввод)
- stdout (вывод)
- stderr (ошибки)

Этот инструмент полезен для тестирования и отладки пользовательского кода, чтобы:
- подставить тестовые данные вместо ввода (stdin),
- перехватить вывод программы (stdout),
- перехватить сообщения об ошибках (stderr).

---

Описание:

stream_interceptor — контекстный менеджер, который временно заменяет стандартные потоки ввода/вывода
на объекты StringIO для перехвата и анализа данных. После выхода из блока with потоки
восстанавливаются к исходному состоянию.

---

Аргументы:

- stdin_data (str или None) — если передать строку, она будет использоваться как поток ввода.
- capture_stdout (bool) — если True, stdout перехватывается и доступен через streams['stdout'].
- capture_stderr (bool) — если True, stderr перехватывается и доступен через streams['stderr'].

---

Возвращает (через yield):

Словарь с объектами StringIO для stdout и stderr, если они были перехвачены.
Если перехват не запрошен, в словаре будет None.

---

Примеры использования:

1) Перехват stdout:

    with stream_interceptor(capture_stdout=True) as streams:
        print("Hello")
    output = streams["stdout"].getvalue()
    print("Captured:", output)

2) Подмена stdin:

    with stream_interceptor(stdin_data="test input\n"):
        user_input = input()
    print("Input was:", user_input)

3) Полный пример:

    with stream_interceptor(stdin_data="42\n", capture_stdout=True, capture_stderr=True) as streams:
        val = input()
        print(f"Value is {val}")
        print("This is an error", file=sys.stderr)
    print("Captured stdout:", streams["stdout"].getvalue())
    print("Captured stderr:", streams["stderr"].getvalue())

---

Примечание:

- После выхода из блока with обязательно восстановятся оригинальные потоки.
- Если не нужен перехват stdout или stderr, не устанавливайте соответствующие флаги.
- Если не нужно менять stdin, передавайте stdin_data=None (по умолчанию).
"""

import sys

from contextlib import contextmanager
from io import StringIO


@contextmanager
def stream_interceptor(stdin_data=None, capture_stdout=False, capture_stderr=False):
    """
    Контекстный менеджер для временной подмены стандартных потоков ввода/вывода/ошибок.

    :param stdin_data: str или None — данные, которые будут подставлены в sys.stdin
    :param capture_stdout: bool — если True, перехватывать sys.stdout
    :param capture_stderr: bool — если True, перехватывать sys.stderr
    :yield: словарь {'stdout': StringIO или None, 'stderr': StringIO или None}
    """

    original_stdin = sys.stdin
    original_stdout = sys.stdout
    original_stderr = sys.stderr

    stdin_buffer = StringIO(stdin_data) if stdin_data is not None else None
    stdout_buffer = StringIO() if capture_stdout else None
    stderr_buffer = StringIO() if capture_stderr else None

    try:
        if stdin_buffer is not None:
            sys.stdin = stdin_buffer
        if stdout_buffer is not None:
            sys.stdout = stdout_buffer
        if stderr_buffer is not None:
            sys.stderr = stderr_buffer

        yield {
            "stdout": stdout_buffer,
            "stderr": stderr_buffer,
        }

    finally:
        sys.stdin = original_stdin
        sys.stdout = original_stdout
        sys.stderr = original_stderr
