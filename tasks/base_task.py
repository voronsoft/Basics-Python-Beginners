# -*- coding: utf-8 -*-


###########################################################################
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import gettext
import json
import os
import urllib.parse

import wx
import wx.html2
import wx.xrc

from cod_editor.code_editor import Editor
from config import TASKS_DESCR_HTML_PATH, VIDEO_PATH_DTL_SOL
from app_statistics.certificate_generation import CertificateFrame
from task_tree.code_for_tasks import code_tasks
from task_tree.task_structure import lst_task_type
from utils.func_utils import get_test_func, status_completed_tasks

_ = gettext.gettext


class BaseTask(wx.Panel):
    def __init__(
        self,
        parent,
        name_description,
        id=wx.ID_ANY,
        pos=wx.DefaultPosition,
        size=wx.Size(500, 500),
        style=wx.TAB_TRAVERSAL,
        name=wx.EmptyString,
    ):
        wx.Panel.__init__(self, parent, id=id, pos=pos, size=size, style=style, name=name)
        # Главный родитель класса
        self.top_parent = self.GetTopLevelParent()
        # print("22 base task:", self.top_parent)

        self.top_sizer = wx.BoxSizer(wx.VERTICAL)

        self.scrolledWindow = wx.ScrolledWindow(
            self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.HSCROLL | wx.VSCROLL
        )
        self.scrolledWindow.SetScrollRate(5, 5)
        self.sizer_scroll = wx.BoxSizer(wx.VERTICAL)


        # Инициализация браузера HTML2
        # Проверяем, доступен ли WebView2
        if wx.html2.WebView.IsBackendAvailable(wx.html2.WebViewBackendEdge):
            # Используем WebView2 (Edge)
            self.browser = wx.html2.WebView.New(self.scrolledWindow, style=wx.BORDER_NONE, backend=wx.html2.WebViewBackendEdge)
            #  Разрешаем включение консоли разработчика
            self.browser.EnableAccessToDevTools(True)

            # Формируем путь к файлу с описанием
            self.descr_file = name_description.lower().split()[0].replace("task", "descr") + ".html"
            # Формируем путь и URL
            file_path = TASKS_DESCR_HTML_PATH / self.descr_file
            file_url = file_path.as_uri()  # Автоматическое преобразование в file:// URL

            # print("1-Адрес загруженной страницы:", file_url)
            self.browser.LoadURL(file_url)

        else:
            wx.MessageBox(
                    "WebView2 (Edge) не установлен.\nУстановщик WebView2 Runtime не найден. Скачайте его по ссылке:\nhttps://developer.microsoft.com/en-us/microsoft-edge/webview2/?form=MA13LH#download",
                    "Ошибка",
                    wx.OK | wx.ICON_ERROR,
            )
            return

        self.sizer_scroll.Add(self.browser, 1, wx.EXPAND | wx.ALL, 0)
        self.scrolledWindow.SetSizer(self.sizer_scroll)
        self.scrolledWindow.Layout()
        self.sizer_scroll.Fit(self.scrolledWindow)
        self.top_sizer.Add(self.scrolledWindow, 1, wx.EXPAND | wx.ALL, 0)

        self.SetSizer(self.top_sizer)
        self.Layout()

        # Переменная для хранения выбранных данных
        self.user_selected_fields = []
        # переменная со списком задач и метками типа задачи
        self.lst_tasks_type = lst_task_type

        # Разрешаем передачу сообщений из JavaScript
        self.browser.AddScriptMessageHandler("wx")

        # Формируем название файла с тестами
        self.test_file_task = name_description.lower().split()[0].replace("task", "test")
        # формируем название файла с заданием
        self.task_file = name_description.split()[0].replace("descr", "task") + ".py"
        self.type_task = self.lst_tasks_type[self.task_file] if self.task_file in self.lst_tasks_type else None

        # Загружаем в главном окне приложения в нижнюю правую панель - класс редактора кода
        if self.type_task == "file":
            self.load_code_redactor()
        # ---------------------------- Connect Events --------------------------------
        # Событие от JavaScript на загруженной странице html (self.descr_file1)
        # Обработка кликов по ссылкам на странице HTML
        self.browser.Bind(wx.html2.EVT_WEBVIEW_NAVIGATING, self.on_webview_event)
        # Обработка данных из скрипта на html странице с описанием задачи/задания
        self.browser.Bind(wx.html2.EVT_WEBVIEW_SCRIPT_MESSAGE_RECEIVED, self.on_message_received)

    # --------------------------- Подключение обработчиков ---------------------------
    def on_webview_event(self, event):
        """Обработчик событий WebView (ссылки и drag-drop)."""
        url = event.GetURL()

        if url.startswith("local-video:///"):  # Если ссылка - это видео, выполняем код
            event.Veto()  # Отменяем переход
            relative_path = urllib.parse.unquote(url.replace("local-video:///", ""))
            abs_path = VIDEO_PATH_DTL_SOL / relative_path
            os.startfile(str(abs_path))  # Path -> str для совместимости с os.startfile

        elif url.startswith("wv-event://mapping"):  # Если это тип задачи drag-drop, выполняем код
            event.Veto()
            try:
                data_part = url.split("data=")[1]
                decoded_data = urllib.parse.unquote(data_part).replace(r"\n", " ").replace("  ", "")
                data_dict = json.loads(decoded_data)
                print("получ дан от пользователя dragdrop\n", data_dict)
                test_name = self.test_file_task
                # Получаем функцию для тестирования
                test_run = get_test_func(test_name)
                # Запускаем тестовую функцию
                test_run(data_dict)
                # Изменяем статус задачи в дереве заданий меняя стандартную иконку на иконку success.ico
                self.top_parent.task_tree.update_task_icon(self.test_file_task.replace("descr", "task"))
                print(f"(on_webview_event- {test_name.replace("descr","task")}) иконка в дереве заданий изменена на success.ico")

                wx.MessageBox("Правильно! Тест пройден успешно", f"{test_name} Результат")
            except Exception as e:
                wx.MessageBox(f"{e}", f"{self.__class__.__name__} Ошибка")

        elif url.startswith(("http://", "https://")):  # Если ссылка HTTP/HTTPS, открываем в системном браузере
            wx.LaunchDefaultBrowser(url)  # Открываем в браузере ОС
            event.Veto()  # Отменяем загрузку в WebView
        else:
            event.Skip()  # Передаем событие дальше, если оно не обработано

    def on_message_received(self, event):
        """Обработчик отвечает за тип задачи - Выберите правильный ответ"""
        print("Отработал - on_message_received")
        # Получаем данные из JavaScript на html странице
        selected_data = event.GetString() # .replace("[", "").replace("]", "")
        print("12366 Выбран ответ:", selected_data)

        if selected_data in self.user_selected_fields:
            event.Veto()

        # Сохраняем данные в переменную
        self.user_selected_fields = selected_data.replace('"', '')

        try:
            test_name = self.test_file_task
            # Получаем функцию для тестирования
            test_run = get_test_func(test_name)
            # Запускаем тестовую функцию
            test_run(self.user_selected_fields)
            # Изменяем статус задачи в дереве заданий меняя стандартную иконку на иконку success.ico
            self.top_parent.task_tree.update_task_icon(self.test_file_task.replace("descr","task"))
            print(f"(on_message_received- {test_name.replace("descr","task")}) иконка в дереве заданий изменена на success.ico")
            wx.MessageBox("Отлично! Тест пройден успешно", f"{test_name} Результат")

            # Если все задачи решены выводим окно поздравления (генерация сертификата)
            if status_completed_tasks():
                show_wnd_certificate = CertificateFrame(None)
                show_wnd_certificate.ShowModal()

        except Exception as e:
            wx.MessageBox(f"{e}", f"{self.__class__.__name__} Ошибка")

    def load_code_redactor(self):
        """Загружает редактор кода в нижнюю панель главного окна приложения"""
        main_frame = wx.GetTopLevelParent(self)  # Получаем ссылку на главное окно

        # Если в родительском классе есть переменная редактор и она не пустая очищаем
        if hasattr(main_frame, "editor") and main_frame.editor is not None:
            main_frame.top_sizer.Hide(main_frame.editor)  # Скрываем контент
            main_frame.top_sizer.Detach(main_frame.editor)  # Открепляем, но не удаляем
            main_frame.editor.Destroy()  # Удаляем объект с заданием, после открепления
            main_frame.editor = None

        # Если в родительском классе нет переменной редактор тогда создаем и регистрируем
        if hasattr(main_frame, "editor") and main_frame.editor is None:
            # Если для задания для которого создаем редактор есть предварительный код для задачи
            # подгружаем код из списка (from code_for_tasks import code_tasks)
            if self.task_file in code_tasks:
                print(f"Предварительный код для задания найден в списке {self.task_file}")
                # Получаем код из словаря
                code_task = code_tasks[self.task_file]
                # Создаём редактор передав:
                # - панель родительского класса
                # - предварительный код к задаче
                main_frame.editor = Editor(main_frame.right_bot_panel, code=code_task)
            else:
                # Если предварительного кода нет, просто создаем класс передав родителя.
                main_frame.editor = Editor(main_frame.right_bot_panel)

            # Добавляем в сайзер панели редактор кода
            main_frame.bottom_sizer.Add(main_frame.editor, 1, wx.EXPAND | wx.ALL, 5)  # Добавляем в сайзер
            # Обновляем интерфейс панели куда помещен редактор кода
            main_frame.right_bot_panel.Layout()

    # --------------------------------------- END ------------------------------------


if __name__ == '__main__':
    app = wx.App()
    frame = wx.Frame(None, size=(500, 500))

    # Создаем слайсер для frame, чтобы управлять компоновкой элементов
    frame_sizer = wx.BoxSizer(wx.HORIZONTAL)

    # Создаем экземпляр BaseTask и добавляем его в слайсер с флагом wx.EXPAND
    tst = BaseTask(frame, "task_1_2_1 Установите соответствия между функциями")
    frame_sizer.Add(tst, 1, flag=wx.EXPAND)

    # Устанавливаем слайсер для frame
    frame.SetSizer(frame_sizer)
    frame.Layout()

    frame.Show(True)
    app.MainLoop()
