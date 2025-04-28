# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version 4.2.1-0-g80c4cb6)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################
import gettext
import multiprocessing
import subprocess

from pathlib import Path

import psutil
import wx
import wx.html2
import wx.stc
import wx.xrc

from app_ai_window import AiWindow
from app_statistics.app_statistics import StatisticsDialog
from clear_status.clear_status_task import ClearStatusTask
from config import IMAGES_PATH, JSON_COMPLETED_TASKS
from task_tree.task_tree import TaskTree
from tasks.welcome import WelcomePage
from utils.func_utils import (
    check_connect_internet,
    check_ide_thonny_pc,
    get_class,
    video_file_run,
    write_json_file,
)

_ = gettext.gettext


###########################################################################
## Class MainFrame
###########################################################################


class MainFrame(wx.Frame):
    """Класс главного окна приложения"""

    def __init__(self, parent):
        wx.Frame.__init__(
            self,
            parent,
            id=wx.ID_ANY,
            title=_("Тренажер Basics Python Beginners"),
            pos=wx.DefaultPosition,
            size=wx.Size(700, 700),
            style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL,
        )

        self.SetSizeHints(wx.Size(700, 700), wx.DefaultSize)
        # Установка шрифта
        self.SetFont(wx.Font(12, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Segoe UI"))
        # Устанавливаем иконку для окна
        icon = wx.Icon(str(IMAGES_PATH / "baby.ico"), wx.BITMAP_TYPE_ICO)
        self.SetIcon(icon)
        self.Maximize(True)

        # Переменная для хранения экземпляра Ai assistant
        self.ai_helper_window = None
        # Переменная для хранения экземпляра ClearStatusTasks
        self.clear_status_window = None
        # Переменная для хранения экземпляра StatisticsDialog
        self.statistics_window = None

        # Основной сайзер окна приложения
        main_sizer = wx.BoxSizer(wx.HORIZONTAL)
        # Задаем минимальный размер окна приложения
        main_sizer.SetMinSize(wx.Size(700, 700))
        # Создаем SplitterWindow для разделения окна на левую и правые части (левая/правая панели)
        self.splitter = wx.SplitterWindow(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.SP_LIVE_UPDATE)
        # Задаем минимальный размер для сжимания панелей
        self.splitter.SetMinimumPaneSize(200)

        # Левая панель в SplitterWindow -----------------------
        self.left_panel = wx.Panel(
            self.splitter, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.BORDER_THEME | wx.TAB_TRAVERSAL
        )

        # Создаем в левой панели сайзер (контейнер)
        left_sizer = wx.BoxSizer(wx.VERTICAL)

        # Добавляем класс Дерева заданий и задач
        self.task_tree = TaskTree(self.left_panel, -1)

        self.task_tree.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_BTNHIGHLIGHT))
        self.task_tree.SetMinSize(wx.Size(-1, -1))
        # Добавляем в сайзер левой панели класс дерева заданий-задач
        left_sizer.Add(self.task_tree, 1, wx.ALL | wx.EXPAND, 0)

        # ---- Кнопки помощников -----
        # Кнопка AI ассистента
        self.ai_astnt_button = wx.Button(
            self.left_panel, wx.ID_ANY, _("Ai assistant"), wx.DefaultPosition, wx.DefaultSize, 0
        )
        left_sizer.Add(self.ai_astnt_button, 0, wx.ALL | wx.EXPAND, 7)
        # Если интернета нет на пк, скрываем кнопку AI assistant
        if not check_connect_internet():
            self.ai_astnt_button.Hide()

        self.run_ide_thonny = wx.Button(
            self.left_panel, wx.ID_ANY, _("Открыть IDE Thonny"), wx.DefaultPosition, wx.DefaultSize, 0
        )
        left_sizer.Add(self.run_ide_thonny, 0, wx.ALL | wx.EXPAND, 7)
        # Если ide Thonny не установлен на пк скрываем кнопку запуска Thonny
        if not check_ide_thonny_pc():
            self.run_ide_thonny.Hide()

        self.clear_status_tasks = wx.Button(
            self.left_panel, wx.ID_ANY, _("Сброс статуса заданий"), wx.DefaultPosition, wx.DefaultSize, 0
        )
        left_sizer.Add(self.clear_status_tasks, 0, wx.ALL | wx.EXPAND, 7)

        self.show_statistics = wx.Button(
            self.left_panel, wx.ID_ANY, _("Статистика прогресса"), wx.DefaultPosition, wx.DefaultSize, 0
        )
        left_sizer.Add(self.show_statistics, 0, wx.ALL | wx.EXPAND, 7)
        # ------------ END -----------
        self.left_panel.SetSizer(left_sizer)
        self.left_panel.Layout()
        left_sizer.Fit(self.left_panel)

        # Правая панель в SplitterWindow -----------------------
        self.right_panel = wx.Panel(
            self.splitter, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.BORDER_THEME | wx.TAB_TRAVERSAL
        )

        # Создаем в правой панели сайзер (контейнер)
        right_sizer = wx.BoxSizer(wx.VERTICAL)

        # Создаем в правой части класса SplitterWindow дополнительный класс SplitterWindow
        # для разделения по вертикали, деля на две части по вертикали
        self.right_splitter = wx.SplitterWindow(
            self.right_panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.SP_LIVE_UPDATE
        )
        # Задаем минимальный размер для сжимания панелей правого сплиттера
        self.right_splitter.SetMinimumPaneSize(200)

        # 1 top часть - Подключения описание задачи для выполнения
        self.right_top_panel = wx.Panel(
            self.right_splitter, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.BORDER_THEME | wx.TAB_TRAVERSAL
        )
        # Сайзер для 1 top часть
        self.top_sizer = wx.BoxSizer(wx.VERTICAL)
        # Задания --------------------------------------------
        self.content_task = WelcomePage(self.right_top_panel)
        self.top_sizer.Add(self.content_task, 1, wx.ALL | wx.EXPAND, 0)
        # END -------------------------------------------------

        self.right_top_panel.SetSizer(self.top_sizer)
        self.right_top_panel.Layout()
        self.top_sizer.Fit(self.right_top_panel)

        # 2 bottom часть - Подключаем редактор кода (Python) или AI ассистента
        self.right_bot_panel = wx.Panel(
            self.right_splitter, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.BORDER_THEME | wx.TAB_TRAVERSAL
        )
        # Сайзер для 2 bottom часть
        self.bottom_sizer = wx.BoxSizer(wx.VERTICAL)
        # Редактора code-redactor --------------
        self.editor = None
        # END ----------------------------------

        self.right_bot_panel.SetSizer(self.bottom_sizer)
        self.right_bot_panel.Layout()
        self.bottom_sizer.Fit(self.right_bot_panel)

        # Этот код разделяет self.right_splitter горизонтально на две части.
        # Верхняя часть (self.right_top_panel) будет иметь высоту 350 пикселей,
        # а оставшееся пространство займёт нижняя часть (self.right_bot_panel).
        half_height = self.GetClientSize().height // 2
        self.right_splitter.SplitHorizontally(self.right_top_panel, self.right_bot_panel, half_height)
        # Установка начального размера выше не сработает, код ниже решает эту проблему !!!
        wx.CallAfter(self.right_splitter.SetSashPosition, half_height)  # Устанавливаем sash после инициализации

        right_sizer.Add(self.right_splitter, 1, wx.EXPAND, 5)

        self.right_panel.SetSizer(right_sizer)
        # Перерисовываем правую панель
        self.right_panel.Layout()
        right_sizer.Fit(self.right_panel)
        # Этот код разделяет self.splitter вертикально на две части.
        # Левая панель (self.left_panel) будет шириной 350 пикселей,
        # а оставшееся пространство займёт правая панель (self.right_panel).
        self.splitter.SplitVertically(self.left_panel, self.right_panel, 350)

        # Подключаем к главному сайзеру основной класс splitter
        main_sizer.Add(self.splitter, 1, wx.EXPAND, 5)

        self.SetSizer(main_sizer)

        self.Layout()

        self.Centre(wx.BOTH)

        # ==================== Статус бар =========================
        # Создаем статус-бар с 3 секциями (добавили для PID)
        self.status_bar = self.CreateStatusBar(3, wx.STB_SIZEGRIP, wx.ID_ANY)
        self.status_bar.SetStatusWidths([100, 150, -1])  # Гибкие размеры

        # Привязываем события мыши к статус-бару
        self.status_bar.Bind(wx.EVT_ENTER_WINDOW, self.on_statusbar_enter)
        self.status_bar.Bind(wx.EVT_LEAVE_WINDOW, self.on_statusbar_leave)
        # ==================== END Статус бар =====================

        # Подключаемые события в программе ----------------
        # Событие выбора элемента из дерева с заданиями (левый фрейм)
        self.task_tree.Bind(wx.EVT_TREE_SEL_CHANGED, self.on_item_selected)
        # Событие нажатия кнопки Ai асистент
        self.ai_astnt_button.Bind(wx.EVT_BUTTON, self.on_run_ai_assistant)
        # Событие нажатия кнопки Открыть IDE Thonny
        self.run_ide_thonny.Bind(wx.EVT_BUTTON, self.on_run_ide_thonny)
        # Событие сброса статуса задач
        self.clear_status_tasks.Bind(wx.EVT_BUTTON, self.on_clear_status_tasks)
        # Событие отображения статистики
        self.show_statistics.Bind(wx.EVT_BUTTON, self.on_show_statistics)
        # Обработчик события закрытия окна
        self.Bind(wx.EVT_CLOSE, self.on_close)
        # END ---------------------------------------------

    # --------------------------- Подключение обработчиков ---------------------------
    def on_item_selected(self, event):
        """Обработчик выбора элемента(задачи) в дереве заданий."""
        item = event.GetItem()  # Получаем выбранный элемент
        text = self.task_tree.GetItemText(item)  # Получаем текст элемента выбранный в дереве задач

        # Проверяем, что выбранный элемент является заданием, а не категорией
        # Если это видео передаем в обработку
        if "video" in text:  # Если видео
            # Очищаем переменные если они не пустые (заняты предыдущим заданием/задачей)
            self.clear_attr_content_and_editor()
            # Передаем в обработку - включаем видео во встроенном плеере ОС
            video_file_run(text.split("video: ")[1])

        # Если это задание/задача передаем в обработку
        elif "task" in text:  # Если не видео файл
            # Очищаем переменные если они не пустые (заняты предыдущим заданием/задачей)
            self.clear_attr_content_and_editor()
            # Передаем в обработку - передаем в обработку для загрузки задания/задачи
            self.processing_selected_item(text)

    def on_run_ai_assistant(self, event):
        """Обработчик запуска Ai assistant в отдельном окне"""
        if self.ai_helper_window and self.ai_helper_window.IsShown():
            # Если окно уже открыто, просто активируем его
            self.ai_helper_window.Raise()
        else:
            # Создаем новое окно помощника
            screen_width, screen_height = wx.GetDisplaySize()

            self.ai_helper_window = AiWindow(self)
            self.ai_helper_window.SetPosition((screen_width // 2, 0))  # Устанавливаем позицию на правый угол
            self.ai_helper_window.SetSize(
                (screen_width // 2, screen_height - 40)
            )  # Окно занимает правую половину экрана

    def on_run_ide_thonny(self, event):
        """Обработчик запуска IDE Thonny в отдельном окне"""
        # Получаем путь к домашней директории текущего пользователя с использованием pathlib
        user_home = Path.home()
        # Строим путь к установленному Thonny
        thonny_path = user_home / 'AppData' / 'Local' / 'Programs' / 'Thonny' / 'thonny.exe'

        # Проверяем, существует ли файл
        if thonny_path.exists():
            subprocess.Popen([str(thonny_path)])

        # Продолжаем обработку других событий
        event.Skip()

    def on_clear_status_tasks(self, event):
        """Обработчик запуска сброса статуса задач в отдельном окне"""
        if self.clear_status_window and self.clear_status_window.IsShown():
            # Если окно уже открыто, просто активируем его
            self.clear_status_window.Raise()
        else:
            # Создаем новое окно
            # Если окно еще не создано, создаем и показываем
            self.clear_status_window = ClearStatusTask(self)
            self.clear_status_window.ShowModal()

    def on_show_statistics(self, event):
        """Обработчик запуска окна статистики"""
        if self.statistics_window and self.statistics_window.IsShown():
            # Если окно уже открыто, просто активируем его
            self.statistics_window.Raise()
        else:
            # Создаем новое окно
            # Если окно еще не создано, создаем и показываем
            self.statistics_window = StatisticsDialog(self)
            self.statistics_window.ShowModal()

    def processing_selected_item(self, name_task):
        """Обрабатывает запуск файла выбранный из дерева заданий"""
        # Если контент есть в переменной с заданиями, или в переменной с редактором, очищаем
        # - self.content_task
        # - self.editor
        self.clear_attr_content_and_editor()

        # Задаем/загружаем контент (задание в переменную self.content_task)
        if not self.content_task:
            # Получаем общий класс для загрузки задания/задачи
            task_class = get_class()
            descr_task = name_task.split()[0].replace("task", "descr")
            # Передаем в общий класс название описания задания/задачи
            # Загружаем задание/задачу в атридут класса - self.content_task
            self.content_task = task_class(self.right_top_panel, descr_task)

            # Добавляем в сайзер новую задачу/задание
            self.top_sizer.Add(self.content_task, 1, wx.ALL | wx.EXPAND, 0)
            # Обновляем сайзер и перерисовываем интерфейс
            self.top_sizer.Layout()  # Перерисовываем сайзер
            self.right_top_panel.Layout()  # Перерисовываем саму панель
            self.right_top_panel.Refresh()  # Обновляем панель
        else:
            wx.MessageBox(
                f"1 Не удалось найти задание: {name_task.split()[0]}\nФайл в папке существует, видимо ошибка кода",
                "Выбор элемента",
                wx.OK | wx.ICON_WARNING,
            )

    def clear_attr_content_and_editor(self):
        """
        Очищает переменные интерфейса если в них есть контент
        - self.content_task правый верхний фрейм (описание задачи)
        - self.editor правый нижний фрейм (редактор кода для задачи)
        """
        # Очищаем переменную с контентом self.content_task правый верхний фрейм
        if self.content_task:
            self.top_sizer.Hide(self.content_task)  # Скрываем контент
            self.top_sizer.Detach(self.content_task)  # Открепляем, но не удаляем
            self.content_task.Destroy()  # Удаляем объект с заданием, после открепления
            self.content_task = None
        #
        # Очищаем переменную с редактором кода self.editor правый нижний фрейм
        if self.editor:
            self.top_sizer.Hide(self.editor)  # Скрываем контент
            self.top_sizer.Detach(self.editor)  # Открепляем, но не удаляем
            self.editor.Destroy()  # Удаляем объект с заданием, после открепления
            self.editor = None

    def on_close(self, event):
        """Обработчик закрытия приложения"""
        # Сохраняем данные состояния заданий
        write_json_file(self.task_tree.task_status, JSON_COMPLETED_TASKS)
        # Сохраняем состояние дерева задач на какой задаче активен пункт-задание
        # для запуска приложения с того места, на котором приложение было закрыто
        self.task_tree.save_state()

        # Продолжаем стандартную процедуру закрытия
        event.Skip()

    # Обработчики статус бара и статистики RAM
    def on_statusbar_enter(self, event):
        """При наведении на статус-бар"""
        self.update_system_stats(None)  # Немедленное обновление

    def on_statusbar_leave(self, event):
        """При уходе со статус-бара"""
        # Очищаем статус-бар
        self.status_bar.SetStatusText("", 0)  # Очищаем PID строку
        self.status_bar.SetStatusText("", 1)  # ... RAM
        self.status_bar.SetStatusText("", 2)  # ... CRU

    def update_system_stats(self, event):
        """Обновление статистики CPU, RAM и PID"""
        try:
            process = psutil.Process()
            cpu = process.cpu_percent(interval=0)
            ram = process.memory_info().rss / (1024 * 1024)  # MB
            pid = process.pid  # Получаем PID процесса

            self.status_bar.SetStatusText(f"PID: {pid}", 0)  # PID первая секция
            self.status_bar.SetStatusText(f"RAM: {ram:.1f} Mb", 1)  # RAM вторая секция
            self.status_bar.SetStatusText(f"CPU: {cpu:.1f}%", 2)  # CRU третья секция
        except Exception as e:
            print(f"Ошибка мониторинга: {e}")

    # END Обработчики статус бара и статистики RAM

    # --------------------------------------- END ------------------------------------


def main():
    """Запускает основное приложение"""
    # Создаем проверочный объект перед запуском приложения
    # для блокировки запуска второго экземпляра приложения
    checker = wx.SingleInstanceChecker("BasicsPythonBeginners_Trainer")

    # Проверка на запуск второго экземпляра приложения
    if checker.IsAnotherRunning():

        try:
            import ctypes

            # Используем Win32 API для системного окна Windows
            ctypes.windll.user32.MessageBoxW(
                0,
                "Приложение уже запущено",
                "Информация",
                0x40,
            )
            return
        except Exception:
            return

    app = wx.App()
    frame = MainFrame(None)
    frame.Show()
    app.MainLoop()


if __name__ == "__main__":
    # Защита для правильной работы многопоточности при сборке в .exe через PyInstaller
    # На Windows при запуске нового процесса копия этого файла выполняется заново.
    # freeze_support() нужен, чтобы различать:
    # - когда программа запускается впервые (основной процесс),
    # - а когда создается новый процесс для работы multiprocessing.
    # Без этой функции программа может зациклиться или упасть при запуске из .exe.
    multiprocessing.freeze_support()

    # Запуск основного приложения
    main()
# TODO [1]
#  В тестах нужно добавить защиту против зависания программы (основного потока).
#  Защиту от передачи в input() входных данных в тех тестах где идет импорт кода пользователя как модуль.
#  Если в таком месте будет не предусмотренный перехват входного потока stdin программа зависнет в ожидании ввода!!!!
#  Реализовать защиту или глобально на уровне программы или локально для определенных тестов.
#  Пример как зависает программа в задании task_7_5_3 в редакторе вводим input() программа зависнет в ожидании ввода..

# TODO [2]
#  Реализовать удаление временных файлов с кодом пользователя из папки Temp ос
#  после удачного выполнения задачи/задания

