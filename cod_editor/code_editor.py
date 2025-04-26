# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version 4.2.1-0-g80c4cb6)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import codecs
import gettext
import importlib
import subprocess

from pathlib import Path

import jedi
import wx
import wx.stc as stc
import wx.xrc

from app_statistics.certificate_generation import CertificateFrame
from utils.func_utils import (
    check_syntax,
    formated_code_pep8,
    save_code_to_temp_file,
    status_completed_tasks,
    run_test_function_with_timeout,
)

_ = gettext.gettext


###########################################################################
## Class Editor
###########################################################################
class Editor(wx.Panel):
    """Окно редактора кода"""

    def __init__(
        self,
        parent,
        code="""# Форматирование кода Ctrl+Alt+l или Ctrl+Alt+f\n""",
        id=wx.ID_ANY,
        pos=wx.DefaultPosition,
        size=wx.Size(500, 500),
        style=wx.TAB_TRAVERSAL,
        name=wx.EmptyString,
    ):
        wx.Panel.__init__(self, parent, id=id, pos=pos, size=size, style=style, name=name)
        # Главный родитель класса
        self.top_parent = self.GetTopLevelParent()
        # print("code_editor parent:", self.top_parent)
        top_sizer = wx.BoxSizer(wx.VERTICAL)

        #  Подключаем класс редактора кода для python
        self.editor = PythonEditor(self)
        # Если в задании есть предварительный код от автора записываем в переменную
        self.code = code
        self.editor.SetText(self.code)

        top_sizer.Add(self.editor, 1, wx.ALL | wx.EXPAND, 0)

        # Кнопка проверки пользовательского кода
        self.run_button = wx.Button(self, wx.ID_ANY, _("Run"), wx.DefaultPosition, wx.DefaultSize, 0)
        top_sizer.Add(self.run_button, 0, wx.ALL | wx.EXPAND, 0)
        # Кнопка открыть файл с заданием в ide Thonny
        self.run_btn_edit_task_in_thonny = wx.Button(
            self, wx.ID_ANY, _("Edit Task in Thonny IDE"), wx.DefaultPosition, wx.DefaultSize, 0
        )
        top_sizer.Add(self.run_btn_edit_task_in_thonny, 0, wx.ALL | wx.EXPAND, 0)

        self.SetSizer(top_sizer)
        self.Layout()

        # Подключаемые события в программе ----------------
        self.run_button.Bind(wx.EVT_BUTTON, self.on_run_button)
        self.run_btn_edit_task_in_thonny.Bind(wx.EVT_BUTTON, self.open_in_thonny)
        # Подключаем события при вводе в редакторе любого символа с клавиатуры
        self.editor.Bind(stc.EVT_STC_CHARADDED, self.editor.on_char_added)

    # --------------------------- Подключение обработчиков ---------------------------

    def on_run_button(self, event):
        """Обработчик нажатия на кнопку Run"""
        code = self.editor.GetText()  # Получаем код пользователя

        # 1--------Проверяем синтаксис
        try:
            check_syntax(code)
            # wx.MessageBox("Код синтаксически верный.\n\n", "Check syntax")
        except SyntaxError as e:
            # wx.MessageBox(f"SyntaxError: {e.msg}\nСтрока {e.lineno}:\n{e.text}", "ERROR syntax")
            wx.MessageBox(f"{e}", "Syntax Error")
            return

        # 2--------Форматируем код пользователя перед записью в файл убирая лишние строки пробелы отступы
        try:
            code_formated = formated_code_pep8(code)
        except Exception as e:
            wx.MessageBox(f"{e}", "Ошибка форматирования:")
            return

        # 3--------Запускаем тесты передав в тестовую функцию которая динамически импортируется из модуля
        if hasattr(self.top_parent, "task_tree"):
            selected_item = self.top_parent.task_tree.GetSelection()  # Получаем текстовое название задания

            # Если элемент был выбран в дереве, формируем название теста для задачи из названия элемента
            if selected_item.IsOk():
                item_text = self.top_parent.task_tree.GetItemText(selected_item)
                # Формируем название модуля
                module = f"tests.{(item_text.split(" ")[0]).replace("task", "test")}"
                print("Назв модуля", module)
                # Формируем имя тестовой функции
                task_num_test = (item_text.split(" ")[0]).replace("task", "test")
                print("Назв теста задачи:", task_num_test)

                # 4--------Сохраняем отформатированный код пользователя во временный файл
                task_name = item_text.split(" ")[0]
                print("Префикс названия для временного файла:", task_name)
                path, name = save_code_to_temp_file(code_formated, task_name)

                # Динамически импортируем модуль с тестом
                try:
                    test_module = importlib.import_module(module)
                    print(f"Модуль {module} успешно импортирован!")
                except ImportError as e:
                    print(f"Ошибка импорта модуля: {e}")
                    wx.MessageBox(f"Ошибка импорта модуля:\n\n{e}", f"({item_text.split(" ")[0]}) Ошибка")
                    return

                # Получаем функцию, которую нужно запустить (название как и у импортируемого модуля)
                try:
                    test_function = getattr(test_module, task_num_test)
                    print(f"Функция {task_num_test} найдена в модуле!\n")
                except AttributeError as e:
                    print(f"Функция {task_num_test} не найдена в модуле: {e}")
                    wx.MessageBox(
                        f"Функция {task_num_test} не найдена в модуле:\n\n{e}", f"({item_text.split(" ")[0]}) Ошибка"
                    )
                    return

                # Запускаем функцию, передавая путь к временному файлу с кодом пользователя
                try:
                    with wx.BusyInfo("Проверка кода... Пожалуйста, подождите.", self.top_parent):
                        # TODO Запуск теста в основном потоке...
                        # success, message = test_function(path, name)
                        # TODO [1 done] Запуск теста в отдельном процессе...
                        success, message = run_test_function_with_timeout(test_function, path, name)

                    # Изменяем статус задачи в дереве заданий меняя стандартную иконку на иконку success.ico
                    self.top_parent.task_tree.update_task_icon(task_name)
                    print(f"(on_run_button- {task_name}) иконка в дереве заданий изменена на success.ico")
                    wx.MessageBox(f"Правильно! Тест пройден успешно\n\n{message}", f"Task OK ! ({task_num_test})")

                    # Если все задачи решены выводим окно поздравления (генерация сертификата)
                    if status_completed_tasks():
                        show_wnd_certificate = CertificateFrame(None)
                        show_wnd_certificate.ShowModal()

                except Exception as e:
                    print(str(e))
                    if isinstance(e, EOFError) or "EOF when reading a line" in str(e):
                        wx.MessageBox(f"Неверное решение...\n\nПопробуйте ещё раз.", f"Ошибка ({item_text.split(" ")[0]})")
                    else:
                        wx.MessageBox(f"{e}", f"Ошибка ({item_text.split(" ")[0]})")

    def open_in_thonny(self, event):
        """Открывает заданный файл в Thonny"""
        code = self.editor.GetText()  # Получаем код пользователя

        # 1--------Проверяем синтаксис
        try:
            check_syntax(code)
            # wx.MessageBox("Код синтаксически верный.\n\n", "Check syntax")
        except SyntaxError as e:
            # wx.MessageBox(f"SyntaxError: {e.msg}\nСтрока {e.lineno}:\n{e.text}", "ERROR syntax")
            wx.MessageBox(f"{e}", "Syntax Error")
            return

        # 2--------Форматируем код пользователя перед записью в файл убирая лишние строки пробелы отступы
        code_formated = formated_code_pep8(code)

        # 3--------Создаем файл с заданием во временной директории
        main_frame = self.top_parent  # Получаем ссылку на главное приложения

        # Если у редактора кода родительский класс основного приложения
        # имеет атрибут task_tree (класс дерева заданий).
        if hasattr(main_frame, "task_tree"):
            # Получаем текстовое название задания
            selected_item = main_frame.task_tree.GetSelection()

            # Если елемент был выбран в дереве, формируем название файла задачи из названия элемента
            if selected_item.IsOk():
                item_text = main_frame.task_tree.GetItemText(selected_item)
                # Формируем название(префикс) временного файла с заданием
                task_num = item_text.split(" ")[0]
                print("22 Назв задачи:", task_num)

                # Сохраняем код пользователя во временный файл
                file_path, file_name = save_code_to_temp_file(code_formated, task_num)

                # Получаем путь к домашней директории текущего пользователя с использованием pathlib
                user_home = Path.home()
                # Строим путь к установленному Thonny
                thonny_path = user_home / 'AppData' / 'Local' / 'Programs' / 'Thonny' / 'thonny.exe'

                # Проверяем, существует ли файл
                if thonny_path.exists():
                    subprocess.Popen([str(thonny_path), file_path])  # Запускаем Thonny с файлом
                else:
                    wx.MessageBox(
                        "IDE Thonny не найдено на ПК\n\nЧто бы открыть задание, переустановите приложение",
                        "Not found - Thonny IDE ",
                    )

                # Продолжаем обработку других событий
                event.Skip()


###########################################################################
## PythonEditor
###########################################################################
class PythonEditor(stc.StyledTextCtrl):
    """Редактор кода Python"""

    def __init__(self, parent, id=wx.ID_ANY):
        # Инициализация родительского класса (StyledTextCtrl)
        stc.StyledTextCtrl.__init__(self, parent, id)
        # Создаем объект wx.Font с конкретным шрифтом и размером
        font = wx.Font(12, wx.FONTFAMILY_MODERN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, faceName="Consolas")
        # Устанавливаем шрифт в редактор
        self.StyleSetFont(stc.STC_STYLE_DEFAULT, font)

        # Создаем кодировщик один раз в конструкторе
        self.encoder = codecs.getencoder("utf-8")
        # Устанавливаем язык Python
        self.SetLexer(stc.STC_LEX_PYTHON)

        # ------------------ Включаем подсветку синтаксиса -------------------------------
        self.StyleSetSpec(stc.STC_P_DEFAULT, "fore:#000000")
        self.StyleSetSpec(stc.STC_P_COMMENTLINE, "fore:#7a7a7a")  # Комментарии
        self.StyleSetSpec(stc.STC_P_TRIPLE, "fore:#7a7a7a")  # Серый для '''
        self.StyleSetSpec(stc.STC_P_TRIPLEDOUBLE, "fore:#7a7a7a")  # Серый для """
        self.StyleSetSpec(stc.STC_P_NUMBER, "fore:#007F7F")  # Числа
        self.StyleSetSpec(stc.STC_P_STRING, "fore:#006b00")  # Строки (двойные кавычки) зеленый
        self.StyleSetSpec(stc.STC_P_CHARACTER, "fore:#006b00")  # Символы/одинарные кавычки зеленый
        self.StyleSetSpec(stc.STC_P_WORD, "fore:#00007F,bold")  # Ключевые слова -keywords
        self.StyleSetSpec(stc.STC_P_OPERATOR, "fore:#000000,bold")  # Операторы
        self.StyleSetSpec(stc.STC_P_IDENTIFIER, "fore:#000000")  # Переменные
        self.StyleSetSpec(stc.STC_P_CLASSNAME, "fore:#0000FF,bold")  # Имена классов
        self.StyleSetSpec(stc.STC_P_DEFNAME, "fore:#007F7F,bold")  # Имена функций
        # Стиль для парных скобок - синий цвет текста
        self.StyleSetSpec(stc.STC_STYLE_BRACELIGHT, "fore:#0000FF,back:#f4f4f4")
        # Стиль для непарных скобок (ошибочных) - красный цвет текста
        self.StyleSetSpec(wx.stc.STC_STYLE_BRACEBAD, "fore:#FF0000,back:#f4f4f4")

        # Список ключевых слов Python
        keywords = " ".join(
            [
                # 1. Ключевые слова (из вашего кода)
                "and as assert break class continue def del elif else except False finally for from global if "
                "import in is lambda None nonlocal not or pass raise return True try while with yield "
                # 2. Встроенные функции/типы (проверено на Python 3.10)
                "abs aiter all anext any ascii bin bool breakpoint bytearray bytes callable chr "
                "classmethod compile complex delattr dict dir divmod enumerate eval exec filter "
                "float format frozenset getattr globals hasattr hash help hex id input int "
                "isinstance issubclass iter len list locals map max memoryview min next object "
                "oct open ord pow print property range repr reversed round self set setattr slice "
                "sorted staticmethod str sum super tuple type vars zip split end sep "
                "BaseException Exception ArithmeticError BufferError LookupError AttributeError "
                "EOFError FloatingPointError GeneratorExit ImportError ModuleNotFoundError "
                "IndexError KeyError KeyboardInterrupt MemoryError NameError NotImplementedError "
                "OSError OverflowError RecursionError ReferenceError RuntimeError StopIteration "
                "StopAsyncIteration SyntaxError IndentationError TabError SystemError SystemExit "
                "TypeError UnboundLocalError UnicodeError UnicodeEncodeError UnicodeDecodeError "
                "UnicodeTranslateError ValueError ZeroDivisionError "
                "Warning UserWarning DeprecationWarning PendingDeprecationWarning SyntaxWarning "
                "RuntimeWarning FutureWarning ImportWarning UnicodeWarning EncodingWarning "
                "BytesWarning ResourceWarning ConnectionError BlockingIOError ChildProcessError "
                "ConnectionAbortedError ConnectionRefusedError ConnectionResetError FileExistsError "
                "FileNotFoundError InterruptedError IsADirectoryError NotADirectoryError "
                "PermissionError ProcessLookupError TimeoutError "
                "BaseObjectGroup ObjectGroup Generic AbstractBaseClass Final "
                "Union Optional Protocol runtime_checkable"
            ]
        )
        self.SetKeyWords(0, keywords)

        # Включаем авто отступы
        self.SetIndentationGuides(True)
        self.SetTabWidth(4)
        self.SetUseTabs(False)
        self.SetIndent(4)

        # Включаем номера строк
        self.SetMarginType(0, stc.STC_MARGIN_NUMBER)
        self.SetMarginWidth(0, 40)

        # Подсветка текущей строки
        self.SetCaretLineVisible(True)
        # Задаем цвет подсветки
        self.SetCaretLineBackground("#f4f4f4")

        # Подключаем событие - Подсветки парных/непарных скобок
        self.Bind(stc.EVT_STC_UPDATEUI, self.highlighting_of_matching_brackets)

        # Подключаем событие - Автодополнение
        self.AutoCompSetIgnoreCase(True)

        # Подключаем событие - авто-закрытия кавычек {([
        self.Bind(wx.stc.EVT_STC_CHARADDED, self.auto_close_quotes)
        # Подключаем событие - автоматического добавления отступов
        self.Bind(wx.stc.EVT_STC_CHARADDED, self.auto_indent)
        # Подключаем событие - обработка нажатия Backspace
        self.Bind(wx.EVT_KEY_DOWN, self.on_backspace_down)
        # Привязка события для перехода по Ctrl+ЛКМ
        self.Bind(wx.EVT_LEFT_DOWN, self.on_ctrl_plus_lft_mouse_btn)
        # Подключаем обработчики для сочетаний клавиш Ctrl+Alt+l or Ctrl+Alt+f
        self.Bind(wx.EVT_KEY_DOWN, self.on_format_code_ctrl_alt_l_f)

    # --------------------------- Подключение обработчиков ---------------------------

    def on_format_code_ctrl_alt_l_f(self, event):
        """Обработчик сочетания клавиш Ctrl+Alt+l or Ctrl+Alt+f для форматирования кода пользователя"""
        print(event.GetKeyCode())
        if event.ControlDown() and event.AltDown() and event.GetKeyCode() in (76, 70):
            print(_("Сработал обработчик форматирования кода"))
            # Получаем текст из редактора
            code = self.GetText()  # Получаем текст из редактора

            # Форматируем код (используем autopep8 для примера, можно использовать другой инструмент)
            formatted_code = formated_code_pep8(code)
            if formatted_code:
                # Обновляем текст в редакторе
                self.SetValue(str(formatted_code))
                # Устанавливаем курсор в конец текста (по желанию)
                self.SetInsertionPointEnd()
            elif formatted_code is None:
                wx.MessageBox(
                    _(
                        "Невозможно отформатировать код !\n\n1- Код содержит синтаксические ошибки !!\n2- Проверьте код, удалите синтаксические ошибки !\n3- После можно провести повторное форматирование кода."
                    ),
                    _("Ошибка при форматировании кода пользователя"),
                )
                return

        # Продолжаем обработку других событий
        event.Skip()

    # ----------------------------- Авто-отступы -----------------------------
    def auto_indent(self, event):
        """Обрабатывает корректные отступы в коде."""

        text = self.GetText()  # Получаем текст в редакторе
        print("текст текущей строки", text)

        # Получаем текст до курсора в текущей строке (до текущей позиции курсора)
        current_line_text = self.GetCurLine()[0]  # GetCurLine возвращает кортеж (строка, позиция курсора)
        print("Получаем текст до курсора в текущей строке", current_line_text)

        # Получаем номер в строке, на которой находится курсор
        position = self.GetCurrentPos()
        line, column = self.get_line_column_from_pos(text, position)
        print("Строка-позиция курсора:", line, ":", column)
        print("Код кнопки", event.GetKey())

        # Получаем номер предыдущей строки
        prev_line = self.GetCurrentLine() - 1
        print("Получаем номер предыдущей строки", prev_line)
        # Получаем текст предыдущей строки
        prev_line_text = self.GetLine(prev_line) if prev_line >= 0 else ""
        print("Получаем текст предыдущей строки", prev_line_text)

        # Получаем количество пробелов в начале предыдущей строки.
        prev_line_indent = self.count_leading_spaces(prev_line_text)
        print("Получаем количество пробелов в начале предыдущей строки", prev_line_indent)
        print("------------------------")

        keywords = ("if ", "elif ", "else ", "for ", "while ", "def ", "class ")
        if any(word for word in keywords if word in prev_line_text) and event.GetKey() == 10:
            print("отработал перенос самого нажатия enter")
            self.AddText("    ")  # Добавляем 4 пробела в начале строки

            # Обработка отступов если это вложенный блок кода
            if prev_line_indent and prev_line_text.rstrip('\r\n').endswith(":") and event.GetKey() == 10:
                print("Блок для вложенных")
                self.AddText(str(" " * prev_line_indent))

        if prev_line_indent and (not prev_line_text.rstrip('\r\n').endswith(":")) and event.GetKey() == 10:
            print("2 Блок для вложенных")
            print(prev_line_indent)
            self.AddText(str(" " * prev_line_indent))

        # Пропускаем это событие, чтобы другие обработчики могли сработать
        event.Skip()

    # --------------------------- END Авто-отступы ---------------------------

    # --------------------------- Переход к искомому объекту -----------------
    def on_ctrl_plus_lft_mouse_btn(self, event):
        """Обработчик нажатия левой кнопки мыши с Ctrl"""
        if event.ControlDown():  # Проверяем, зажата ли клавиша Ctrl
            self.goto_definition()
        else:
            event.Skip()  # Пропускаем событие, если Ctrl не зажат

    def goto_definition(self):
        """Переход к определению объекта под курсором"""
        # Получаем текущий текст из редактора
        code = self.GetText()

        # Получаем текущую позицию курсора
        cursor_pos = self.GetCurrentPos()

        # Преобразуем позицию курсора в строку и столбец
        line, column = self.get_line_column_from_pos(code, cursor_pos)

        # Используем Jedi для поиска определения
        script = jedi.Script(code=code, path="<string>")
        definitions = script.goto(line=line, column=column)

        if definitions:
            # Берем первое определение (если их несколько)
            definition = definitions[0]

            # Получаем позицию определения
            def_line = definition.line
            def_column = definition.column

            # Переходим к позиции определения
            self.GotoPos(self.PositionFromLine(def_line - 1) + def_column)
        else:
            wx.MessageBox("Определение не найдено", "Ошибка", wx.OK | wx.ICON_INFORMATION)

    # --------------------------- END Переход к искомому объекту -------------

    def count_leading_spaces(self, text):
        """Возвращает количество пробелов в начале предыдущей строки."""
        return len(text) - len(text.lstrip(" "))

    def auto_close_quotes(self, event):
        # Получим код нажатой клавиши
        key_val = event.GetKey()

        # Нас не интересуют нажатые клавиши с кодом больше 127
        if key_val > 127:
            return

        # Получим символ нажатой клавиши
        key = chr(key_val)

        # Варианты открывающихся скобок
        open = "{(["

        # Пары закрывающихся скобок к открывающимся
        close = "})]"

        keyindex = open.find(key)

        if keyindex != -1:
            pos = self.GetCurrentPos()
            text = self.GetText()

            self.AddText(close[keyindex])

            # Установим каретку перед закрывающейся скобкой
            self.GotoPos(pos)

    def on_char_added(self, event):
        """Автодополнение при вводе кода с использованием Jedi"""
        # Получаем код нажатой клавиши
        char = event.GetKey()
        # Проверяем, является ли символ печатаемым (буква, цифра или точка)
        # Если символ не является печатаемым (например, Enter, Tab, Backspace)
        # игнорируем такие клавиши, что бы не запускать автодополнение
        try:
            char_str = chr(char)  # Преобразуем код в символ
        except ValueError:
            # Если символ не может быть преобразован (например, для специальных клавиш), пропускаем автодополнение
            event.Skip()
            return

        # Если символ не является частью идентификатора (буква, цифра, точка), пропускаем автодополнение
        if not (char_str.isalnum() or char_str == '.'):
            event.Skip()
            return

        # Получаем текущий текст из редактора
        code = self.GetText()
        # Получаем текущую позицию курсора
        cursor_pos = self.GetCurrentPos()
        # Преобразуем позицию курсора в строку и столбец
        line, column = self.get_line_column_from_pos(code, cursor_pos)
        # Получаем текущую строку до курсора
        current_line = self.GetCurLine()[0]  # GetCurLine возвращает кортеж (строка, позиция курсора)
        current_line = current_line.rstrip('\r\n')  # Удаляем символы перевода строки

        # Если строка пустая, пропускаем автодополнение
        if not current_line.strip():
            event.Skip()
            return

        # Убедимся, что column не выходит за пределы длины строки
        if column > len(current_line):
            column = len(current_line)

        # Используем Jedi для автодополнения
        script = jedi.Script(code=code, path="<string>")  # path="<string>" для работы с текстом в памяти
        completions = script.complete(line=line, column=column)  # Новый метод complete()

        if completions:
            # Получаем текущее слово (для фильтрации подсказок)
            current_word = self.get_current_word()

            # Формируем список подсказок, отфильтрованных по текущему слову
            suggestions = [comp.name for comp in completions if comp.name.startswith(current_word)]

            if suggestions:
                # Преобразуем список подсказок в строку, разделенную пробелами
                suggestions_str = " ".join(suggestions)

                if not suggestions:
                    return

                # Показываем автодополнение
                self.AutoCompShow(len(current_word), suggestions_str)

        # Отключаем дальнейшую обработку события
        event.Skip()  # Позволяет другим обработчикам срабатывать

    def get_current_word(self):
        """Получает текущее слово под курсором."""
        pos = self.GetCurrentPos()
        start = pos
        while start > 0 and chr(self.GetCharAt(start - 1)).isalnum():
            start -= 1
        return self.GetTextRange(start, pos)

    def get_line_column_from_pos(self, text, pos):
        """Преобразует позицию курсора в строку и столбец.
        :param text - str
        :param pos - int
        """
        lines = text[:pos].split("\n")
        line = len(lines)
        column = len(lines[-1]) if lines else 0
        return line, column

    def calcByteLen(self, text):
        """Посчитать длину строки в байтах, а не в символах"""
        return len(self.encoder(text)[0])

    def highlighting_of_matching_brackets(self, event):
        """Подсветка парных скобок"""

        pos = self.GetCurrentPos()  # Получим текущую позицию каретки в байтах

        # Получим набранный текст и посчитаем его длину
        text = self.GetText()
        text_len = self.calcByteLen(text)

        # Получим текст, расположенные слева от каретки
        text_left = ""
        if pos > 0:
            text_left = self.GetTextRange(0, pos)

        # Получим текст расположенный справа от каретки
        text_right = ""
        if pos < text_len:
            text_right = self.GetTextRange(pos, text_len)

        # Проверим есть ли слева скобка (круглая, квадратная или фигурная)
        if len(text_left) > 0 and text_left[-1] in "{}()[]":
            # Попытаемся найти парную скобку
            match = self.BraceMatch(pos - 1)

            # нашли парную скобку
            if match != wx.stc.STC_INVALID_POSITION:
                # Подсветим обе
                self.BraceHighlight(pos - 1, match)
                return
            else:
                # Иначе подсветим первую скобку как ошибочную
                self.BraceBadLight(pos - 1)
                return
        else:
            # В этой позиции не скобка, отключим подсветку
            self.BraceBadLight(wx.stc.STC_INVALID_POSITION)

        # Если не нашли скобку слева, проверим есть ли она справа
        if len(text_right) > 0 and text_right[0] in "{}()[]":
            match = self.BraceMatch(pos)

            # нашли парную скобку
            if match != wx.stc.STC_INVALID_POSITION:
                # Подсветим обе
                self.BraceHighlight(pos, match)
                return
            else:
                # Иначе подсветим первую скобку как ошибочную
                self.BraceBadLight(pos)
                return
        else:
            # В этой позиции не скобки, отключим подсветку
            self.BraceBadLight(wx.stc.STC_INVALID_POSITION)

    # ------------------- Удаление пробелов (Backspace) -----------------------
    def on_backspace_down(self, event):
        """Обрабатывает нажатие Backspace для удаления 4 пробелов или 1 символа"""
        key = event.GetKeyCode()

        if key == wx.WXK_BACK:
            # Проверяем, есть ли выделенный текст если есть удаляем одним нажатием на Backspace
            if self.GetSelectedText():
                # Удаляем выделенный текст
                self.ReplaceSelection("")
                return

            current_pos = self.GetCurrentPos()

            if current_pos > 0:
                # Берём текст перед курсором, но с учётом возможной ошибки с байтами
                text_before_cursor = self.GetTextRange(0, current_pos)

                if not text_before_cursor:
                    event.Skip()
                    return

                # Преобразуем текст в нормальную строку (работаем с символами, а не байтами)
                text_before_cursor = text_before_cursor.encode("utf-8").decode("utf-8")

                # Берём последний символ перед курсором
                last_char = text_before_cursor[-1]
                print("Символ перед курсором", last_char)

                # Вычисляем его длину в байтах
                char_size = len(last_char.encode("utf-8"))

                # Удаляем 4 пробела, если они кратны 4.
                # Получаем текст строки, где стоит курсор
                text_line = self.GetCurLine()[0]

                if text_line.isspace():
                    # Количество пробелов перед курсором
                    spaces_count = len(text_line.rstrip('\r\n'))
                    print("spaces_count", spaces_count)

                    # Определяем, есть ли остаточные пробелы
                    remainder = spaces_count % 4

                    if remainder > 0:
                        # Удаляем по 1 пробелу, пока не уберём остаток
                        self.SetTargetStart(current_pos - 1)
                        self.SetTargetEnd(current_pos)
                        self.ReplaceTarget("")
                        return
                    else:
                        # Если остатка нет, удаляем 4 пробела сразу
                        self.SetTargetStart(current_pos - 4)
                        self.SetTargetEnd(current_pos)
                        self.ReplaceTarget("")
                        return

                # Удаляем 1 символ (правильное количество байтов)
                self.SetTargetStart(current_pos - char_size)
                self.SetTargetEnd(current_pos)
                self.ReplaceTarget("")
                return

        event.Skip()

    # -------------------------- END Backspace --------------------------------


def main():
    app = wx.App(False)
    frame = wx.Frame(None, title="Python Editor", size=(500, 500))
    editor = Editor(frame)
    frame.Show()
    app.MainLoop()


# Запуск
if __name__ == "__main__":
    main()
