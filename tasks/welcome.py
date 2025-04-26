import wx
import wx.html2

from config import TASKS_DESCR_HTML_PATH


###########################################################################
## Class WelcomePage
###########################################################################
class WelcomePage(wx.Panel):
    """Класс запуск страницы приветствия"""
    def __init__(
        self,
        parent,
        id=wx.ID_ANY,
        pos=wx.DefaultPosition,
        size=wx.Size(500, 300),
        style=wx.TAB_TRAVERSAL,
        name=wx.EmptyString,
    ):
        wx.Panel.__init__(self, parent, id=id, pos=pos, size=size, style=style, name=name)

        # Инициализация браузера HTML2
        # Проверяем, доступен ли WebView2
        if wx.html2.WebView.IsBackendAvailable(wx.html2.WebViewBackendEdge):
            # Используем WebView2 (Edge)
            self.browser = wx.html2.WebView.New(self, style=wx.BORDER_NONE, backend=wx.html2.WebViewBackendEdge)
            # Разрешаем включение консоли разработчика
            self.browser.EnableAccessToDevTools(True)

            # Формируем путь к файлу с описанием
            file_path = TASKS_DESCR_HTML_PATH / "a_welcome.html"
            file_url = file_path.as_uri()  # Автоматически формирует file:// URL
            # print("Адрес загруженной страницы:", file_url)
            self.browser.LoadURL(file_url)

        else:
            wx.MessageBox(
                "WebView2 (Edge) не установлен.\nУстановщик WebView2 Runtime не найден. Скачайте его по ссылке:\nhttps://developer.microsoft.com/en-us/microsoft-edge/webview2/?form=MA13LH#download",
                "Ошибка",
                wx.OK | wx.ICON_ERROR,
            )
            return

        # Растягиваем браузер на всю панель
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.browser, 1, wx.EXPAND, 0)
        self.SetSizer(sizer)
        self.Layout()

        # Обработка кликов по ссылкам на странице HTML
        self.browser.Bind(wx.html2.EVT_WEBVIEW_NAVIGATING, self.on_webview_event)

    # --------------------------- Подключение обработчиков ---------------------------
    def on_webview_event(self, event):
        """Обработчик событий WebView (ссылки и drag-drop)."""
        url = event.GetURL()

        if url.startswith(("http://", "https://")):  # Если ссылка HTTP/HTTPS, открываем в системном браузере
            wx.LaunchDefaultBrowser(url)  # Открываем в браузере ОС
            event.Veto()  # Отменяем загрузку в WebView
        else:
            event.Skip()  # Передаем событие дальше, если оно не обработано


def main():
    app = wx.App()  # Создаем приложение wxPython
    frame = wx.Frame(None, title="Основы Python", size=(500, 500))  # Создаем главное окно
    panel = WelcomePage(frame)  # Создаем панель и передаем ей родительское окно
    frame.Show()  # Показываем окно
    app.MainLoop()  # Запускаем главный цикл приложения


if __name__ == '__main__':
    main()
