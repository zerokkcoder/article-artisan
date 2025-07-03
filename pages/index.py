import flet as ft

class Index:
    def index(self, page: ft.Page):
        page.window.bgcolor = ft.Colors.TRANSPARENT
        page.window.icon = '../assets/favicon.ico'
        page.window.center()
        page.title = "Article Artisan"
        page.padding = 0
        page.theme_mode = ft.ThemeMode.SYSTEM
        page.update()
