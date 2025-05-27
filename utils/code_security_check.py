import ast


def check_code_safety(code_str: str, allowed_imports=None, allowed_calls=None):
    """
    Проверяет, что в пользовательском коде нет запрещённых импортов и вызовов из опасных модулей.

    Разрешены:
    - Любой код, если нет импортов.
    - Импорты только из разрешённых модулей.
    - Вызовы только из разрешённых функций разрешённых модулей.

    Аргументы:
        code_str (str): строка с кодом пользователя.
        allowed_imports (list[str]): список разрешённых опасных модулей.
        allowed_calls (list[str]): список разрешённых вызовов из опасных модулей (например, ["sys.stdin.readlines"]).
    """
    if allowed_imports is None:
        allowed_imports = []

    if allowed_calls is None:
        allowed_calls = []

    # Опасные модули, требующие контроля
    dangerous_modules = {
        "os",
        "sys",
        "subprocess",
        "socket",
        "shutil",
        "ctypes",
        "platform",
        "inspect",
        "builtins",
        "eval",
        "exec",
        "threading",
        "multiprocessing",
        "urllib",
        "http",
        "ftplib",
        "smtplib",
        "telnetlib",
        "xmlrpc",
        "webbrowser",
        "ssl",
        "requests",
    }
    # Парсим AST
    tree = ast.parse(code_str)

    imported_dangerous_modules = set()

    for node in ast.walk(tree):
        # Проверка обычных импортов
        if isinstance(node, ast.Import):
            for alias in node.names:
                module = alias.name.split('.')[0]
                if module in dangerous_modules:
                    if module not in allowed_imports:
                        raise RuntimeError(f"Запрещённый импорт модуля: {module}")
                    imported_dangerous_modules.add(module)

        # Проверка from-import
        elif isinstance(node, ast.ImportFrom):
            module = node.module.split('.')[0] if node.module else ''
            if module in dangerous_modules:
                if module not in allowed_imports:
                    raise RuntimeError(f"Запрещённый импорт из модуля: {module}")
                imported_dangerous_modules.add(module)

    # Если нет импортов из опасных модулей — остальной код можно не проверять
    if not imported_dangerous_modules:
        return

    # Проверка вызовов функций только если есть импорт опасных модулей
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
            # Получаем полное имя вызова, например: sys.stdin.readlines
            names = []
            current = node.func
            while isinstance(current, ast.Attribute):
                names.insert(0, current.attr)
                current = current.value
            if isinstance(current, ast.Name):
                names.insert(0, current.id)
                full_name = ".".join(names)
                root_module = names[0]

                if root_module in imported_dangerous_modules and full_name not in allowed_calls:
                    raise RuntimeError(f"Запрещён вызов: {full_name}")
