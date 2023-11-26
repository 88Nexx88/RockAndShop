import pyautogui
from flet import *

from flet_gui.app_build import AppMain
from storage.value_class import Value_page


def main(page: Page):
    page.title = 'Rock and Shop? Yeep!'
    page.theme = theme.Theme(color_scheme_seed='#654E92')
    page.theme.scrollbar_theme = ScrollbarTheme(thumb_color='black')
    page.theme_mode = "dark"
    page.horizontal_alignment = 'center'
    page.window_min_width = 1080
    page.window_min_height = 600
    size = pyautogui.size()
    if size[1] == 1080:
        page.window_height = size[1] - 24
    else:
        page.window_height = size[1] - 28
    # page.window_width = size[0]
    page.window_max_height = size[1]
    page.window_max_width = size[0]
    page.window_maximized = True
    page.window_resizable = False
    value_korzina = Value_page()
    AppMain(page, value_korzina)

    page.update()


# app(target=main, view=WEB_BROWSER)
app(target=main)