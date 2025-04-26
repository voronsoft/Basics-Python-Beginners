import datetime
import webbrowser

import wx
import wx.html2

from config import IMAGES_PATH, TASKS_DESCR_HTML_PATH


###########################################################################
## Class CertificatePage
###########################################################################
class CertificateFrame(wx.Dialog):
    def __init__(self, parent):
        wx.Dialog.__init__(
            self,
            parent=parent,
            id=wx.ID_ANY,
            title="Генератор сертификата",
            pos=wx.DefaultPosition,
            size=wx.Size(800, 800),
            style=wx.DEFAULT_FRAME_STYLE,
            name=wx.EmptyString,
        )

        self.SetSizeHints(wx.Size(800, 800), wx.DefaultSize)
        self.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_BTNFACE))
        # Установка шрифта
        self.SetFont(wx.Font(12, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Segoe UI"))
        # Устанавливаем иконку для окна
        icon = wx.Icon(str(IMAGES_PATH / "baby.ico"), wx.BITMAP_TYPE_ICO)
        self.SetIcon(icon)

        # Проверяем, доступен ли WebView2
        if wx.html2.WebView.IsBackendAvailable(wx.html2.WebViewBackendEdge):
            # Используем WebView2 (Edge)
            self.browser_sert = wx.html2.WebView.New(self, style=wx.BORDER_NONE, backend=wx.html2.WebViewBackendEdge)
            # Разрешаем включение консоли разработчика
            self.browser_sert.EnableAccessToDevTools(True)

            # Формируем путь к файлу с описанием
            file_path = TASKS_DESCR_HTML_PATH / "certificate.html"
            file_url = file_path.as_uri()  # Автоматически формирует file:// URL
            print("Адрес загруженной страницы:", file_url)
            self.browser_sert.LoadURL(file_url)

        else:
            wx.MessageBox(
                "WebView2 (Edge) не установлен.\nУстановщик WebView2 Runtime не найден. Скачайте его по ссылке:\n"
                "https://developer.microsoft.com/en-us/microsoft-edge/webview2/?form=MA13LH#download",
                "Ошибка",
                wx.OK | wx.ICON_ERROR,
            )
            return

        # Главный sizer
        main_sizer = wx.BoxSizer(wx.VERTICAL)

        # Создаем sizer для элементов управления
        control_sizer = wx.BoxSizer(wx.HORIZONTAL)

        self.name_label = wx.StaticText(self, label="Введите имя фамилия:")
        control_sizer.Add(self.name_label, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 5)

        self.name_input = wx.TextCtrl(self, style=wx.TE_PROCESS_ENTER)
        control_sizer.Add(self.name_input, 1, wx.EXPAND)

        self.update_btn = wx.Button(self, label="Обновить сертификат")
        control_sizer.Add(self.update_btn, 0, wx.LEFT, 5)

        self.save_btn = wx.Button(self, label="Сохранить файл на ПК")
        control_sizer.Add(self.save_btn, 0, wx.LEFT, 5)

        main_sizer.Add(control_sizer, 0, wx.EXPAND | wx.ALL, 5)
        main_sizer.Add(self.browser_sert, 1, wx.EXPAND | wx.ALL, 5)

        self.SetSizer(main_sizer)
        self.Layout()
        self.Centre(wx.BOTH)

        # Привязка событий
        self.update_btn.Bind(wx.EVT_BUTTON, self.update_certificate)
        self.save_btn.Bind(wx.EVT_BUTTON, self.save_certif)
        self.name_input.Bind(wx.EVT_TEXT_ENTER, self.update_certificate)
        # Событие обработки ссылок при нажатии
        self.browser_sert.Bind(wx.html2.EVT_WEBVIEW_NAVIGATING, self.on_navigation)
        # Событие закрытие окна
        self.Bind(wx.EVT_CLOSE, self.on_close)

    def update_certificate(self, event):
        """Обновление данных в сертификате"""
        student_name = self.name_input.GetValue().strip()
        if not student_name:
            wx.MessageBox("Введите имя студента!", "Ошибка", wx.OK | wx.ICON_WARNING)
            return

        # Форматирование текущей даты
        current_date = datetime.datetime.now().strftime("%d %B %Y")

        # JavaScript для обновления данных
        js_code = f"""
            document.getElementById('student-name').textContent = '{student_name}';
            document.getElementById('date_gen_sert').textContent = '{current_date}';
        """
        self.browser_sert.RunScript(js_code)

    def save_certif(self, event):
        """Сохранение сертификата как автономной HTML страницы со всеми стилями"""
        if not self.name_input.GetValue().strip():
            wx.MessageBox("Сначала введите имя студента!", "Ошибка", wx.OK | wx.ICON_WARNING)
            return

        with wx.FileDialog(
            self,
            "Сохранить автономную HTML страницу",
            "",
            f"Сертификат_{self.name_input.GetValue()}.html",
            "HTML files (*.html)|*.html",
            wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT,
        ) as dlg:
            if dlg.ShowModal() == wx.ID_CANCEL:
                return

            try:
                # Получаем текущий HTML с уже применёнными стилями
                html_content = self.browser_sert.GetPageSource()

                # Сохраняем как полноценный HTML файл
                with open(dlg.GetPath(), 'w', encoding='utf-8') as f:
                    f.write(html_content)

                wx.MessageBox("HTML страница c сертификатом сохранена.", "Готово", wx.OK | wx.ICON_INFORMATION)
            except Exception as e:
                wx.MessageBox(f"Ошибка при сохранении: {str(e)}", "Ошибка", wx.OK | wx.ICON_ERROR)

    def on_navigation(self, event):
        """Обработчик навигации в WebView - открывает внешние ссылки в системном браузере"""
        url = event.GetURL()

        # Если ссылка начинается с http:// или https://, открываем в системном браузере
        if url.startswith(('http://', 'https://')):
            webbrowser.open(url)  # Открываем в браузере по умолчанию
            event.Veto()  # Отменяем загрузку в WebView
        else:
            event.Skip()  # Пропускаем все остальные ссылки

    def on_close(self, event):
        """Обработчик закрытия окна"""
        self.Destroy()


def main():
    app = wx.App()
    frame = CertificateFrame(None)
    frame.ShowModal()  # Показываем окно
    app.MainLoop()


if __name__ == '__main__':
    main()
