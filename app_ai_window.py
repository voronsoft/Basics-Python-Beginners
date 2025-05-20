# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version 4.2.1-0-g80c4cb6)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import gettext

import wx
import wx.html
import wx.html2
import wx.xrc

_ = gettext.gettext


###########################################################################
## Class AiWindow
## Класс окно для загрузки и отображения HTML-страницы по URL с внешнего источника,
## внешним источником является чат GPT с авторизацией и без (https://chatgpt.com/)
###########################################################################


class AiWindow(wx.Frame):

    def __init__(self, parent):
        wx.Frame.__init__(
            self,
            parent,
            id=wx.ID_ANY,
            title=_(u"Ai assistant"),
            pos=wx.DefaultPosition,
            size=wx.Size(700, 700),
            style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL,
        )

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)

        main_sizer_ai = wx.BoxSizer(wx.VERTICAL)

        # Создаём WebView для отображения HTML-страниц
        self.htmlWinAI = wx.html2.WebView.New(self, style=wx.BORDER_NONE)

        # Загружаем страницу с ИИ (страница с ChatGPT)
        self.htmlWinAI.LoadURL("https://chatgpt.com/")

        main_sizer_ai.Add(self.htmlWinAI, 1, wx.ALL | wx.EXPAND, 0)

        self.SetSizer(main_sizer_ai)
        self.Layout()
        self.Centre(wx.BOTH)

        # Обработчик изменения размера окна
        self.Bind(wx.EVT_SIZE, self.on_resize)
        # Перехватываем закрытие окна, чтобы обнулить ссылку в главном окне
        self.Bind(wx.EVT_CLOSE, self.on_close)

        # Отображаем окно
        self.Show()

    def on_resize(self, event):
        """Обновляет размер WebView при изменении размера окна"""
        self.htmlWinAI.SetSize(self.GetSize())
        event.Skip()

    def on_close(self, event):
        """Обнуляем ссылку при закрытии окна"""
        # print("!!!!", self.GetParent())
        if self.GetParent():
            # print(self.GetParent().ai_helper_window)
            self.GetParent().ai_helper_window = None
            # print(self.GetParent().ai_helper_window)
        self.Destroy()


def main_singl_window(self=None):
    """Запуск окна приложения с Ai ассистентом"""
    app = wx.App(False)
    screen_width, screen_height = wx.GetDisplaySize()
    # print(screen_width, screen_height)
    ai_frame = AiWindow(self)
    ai_frame.Show()
    app.MainLoop()


# Запуск
if __name__ == "__main__":
    main_singl_window()
