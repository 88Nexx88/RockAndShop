import time

import flet as ft
from flet import *

import element_product
class AppMain:
    

    def __init__(self, page):
        self.page = page
        # self.page.horizontal_alignment = 'center'
        # self.page.vertical_alignment = 'center'
        self.TextHeaderWelcome = Text('Привет, пришли за выгодными покупками?🤨', style="headlineLarge",
                                      text_align='center')
        self.create_appbar()
        self.start_view = Container(
            width=1000,
            height=900,
            border_radius=35,
            bgcolor='#2E4374',
            padding=padding.only(left=80, top=40, right=80),
            content=Column(controls=[
                Container(height=200),
                Container(height=150),
                Container(content=self.TextHeaderWelcome, alignment=alignment.center),
                Container(height=274),
                Container(content=Row(controls=
                                      [
                                            Container(width=100),
                                            TextButton(content=Row(controls=[
                                            Icon(icons.ARROW_RIGHT, size=140),
                                            Text(value='Да! Вперёд👍', size=40)
                                          
                            ]), on_click=self.to_next)
            ], alignment=MainAxisAlignment.SPACE_BETWEEN))
                
            ], alignment=alignment.center
            )
        )
    
        
        self.page.add(self.start_view)
        self.page.update()

    def to_next(self, event):
        self.page.controls.clear()
        AppFinder(self.page)
        self.page.update()
    
    def changetheme(self, event):
        # self.page.theme_mode = "light" if self.page.theme_mode == 'dark' else 'dark'
        # self.togglelight_dark.selected = not self.togglelight_dark.selected
        # time.sleep(0.2)
        # self.page.update()
        print("!!!!")

    def create_appbar(self):
        self.togglelight_dark = ft.IconButton(on_click=self.changetheme, icon=ft.icons.QUESTION_MARK)
        self.appbar = ft.AppBar(
            leading=ft.Icon(ft.icons.APPS),
            leading_width=40,
            title=ft.Text("Rock & Shop", weight=ft.FontWeight.BOLD),
            center_title=False,
            bgcolor=ft.colors.SURFACE_VARIANT,
            actions=[
                self.togglelight_dark
            ],
        )
        self.page.add(self.appbar)

class AppFinder:
    """
    """

    def __init__(self, page):
        self.page = page
        self.page.horizontal_alignment = 'center'
        self.page.vertical_alignment = 'start'
        self.Is_has_validate_name = {'status_name': 0, 'status_surname': 0}
        self.Is_has_name_surname = 0
        self.Is_has_session = 0

        self.finder_app()

    def korzina_click(self, page):
        print("!!!")
        self.page.update()

    def changetheme(self, event):
        # self.page.theme_mode = "light" if self.page.theme_mode == 'dark' else 'dark'
        # self.togglelight_dark.selected = not self.togglelight_dark.selected
        # time.sleep(0.2)
        # self.page.update()
        print("!!!!")


    def create_appbar(self):
        self.togglelight_dark = ft.IconButton(on_click=self.changetheme, icon=ft.icons.QUESTION_MARK)
        self.list_product_button = ft.TextButton(
            content=ft.Row(
                [
                    ft.Text(value='Корзина:', size=20, weight=ft.FontWeight.BOLD),
                    ft.Text(value='0', size=20, weight=ft.FontWeight.BOLD, color='#E5C3A6')
                ]
        ), on_click=self.korzina_click)
        self.appbar = ft.AppBar(
            leading=ft.Icon(ft.icons.APPS),
            leading_width=40,
            title=ft.Text("Rock & Shop", weight=ft.FontWeight.BOLD),
            center_title=False,
            bgcolor=ft.colors.SURFACE_VARIANT,
            actions=[
                self.togglelight_dark,
                self.list_product_button
            ],
        )
        self.page.add(self.appbar)

    def find_product(self, e):
        print(e.control.value)
        # list_p = self.generate_product_list(zapros=e.control.value)
        self.list_find_product.controls.clear()
        self.generate_product_list(e.control.value)
        # for i in list_p:
        #     self.list_find_product.controls.append(i)
        self.page.update()

    def minus_click(self, e):
        if int(self.txt_number.value) > 1:
            self.txt_number.value = int(self.txt_number.value) - 1
        else:
            self.txt_number.value = 1
        self.page.update()

    def plus_click(self, e):
        self.txt_number.value = int(self.txt_number.value) + 1
        self.page.update()

    def add_click(self, e):
        self.dialog.open = False
        old_value = int(self.list_product_button.content.controls[1].value)
        self.list_product_button.content = ft.Row(
            [
                ft.Text(value='Корзина', size=20, weight=ft.FontWeight.BOLD),
                ft.Text(value=old_value+1, size=20, weight=ft.FontWeight.BOLD, color='#E5C3A6')
            ]
        )
        self.page.update()

    def exit_add_click(self, e):
        self.dialog.open = False
        self.page.update()
    
    def element_click(self, e):
        self.txt_number = Text(value='1')
        self.dialog = ft.AlertDialog(
            title=ft.Text("Укажите количество товара: "),
            modal=True,
            actions = [
                    TextButton(text='Отмена', on_click=self.exit_add_click),
                    IconButton(icons.REMOVE, on_click=self.minus_click),
                    self.txt_number,
                    IconButton(icons.ADD, on_click=self.plus_click),
                    TextButton(text='Добавить', on_click=self.add_click)],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        self.page.dialog = self.dialog
        self.dialog.open = True
        self.page.update()

    def generate_product_list(self, zapros):
        if int(zapros) > 10:
            for i in range(10):
                r = Container(
                    content= Column(controls=[
                        Container(content=Text(value='"Вино Пьетраме Монтепульчано Д`Абруццо DOP красное полусухое"', size=24, color='#132043'),padding=padding.only(left=10, top=5), alignment=alignment.center_left),
                        Row(controls=
                        [
                            Container(width=20),
                            Container(content = Text(value='Италия, 0.75 л., Абруццо, 13%', size=20, color='#132043'), padding=padding.only(bottom=5)),
                            Container(width=20),
                            Container(content = Text(value='КБ', size=20,  color='#132043'), padding=padding.only(bottom=5)),
                        ])
                    ], alignment=MainAxisAlignment.SPACE_BETWEEN
                    ),
                    on_click=self.element_click, bgcolor='#ADC4CE', height=80

                )
                self.list_find_product.controls.append(r)
        else:
            for i in range(80):
                r = Container(
                    content=Column(controls=[
                        Container(content=Text(value='"Вино Пьетраме Монтепульчано Д`Абруццо DOP красное полусухое"',
                                               size=24, color='#132043'), padding=padding.only(left=10, top=5),
                                  alignment=alignment.center_left),
                        Row(controls=
                        [
                            Container(width=20),
                            Container(content=Text(value='Италия, 0.75 л., Абруццо, 13%', size=20,  color='#132043'),
                                      padding=padding.only(bottom=5)),
                            Container(width=20),
                            Container(content=Text(value='КБ', size=20,  color='#132043'), padding=padding.only(bottom=5)),
                        ])
                    ], alignment=MainAxisAlignment.SPACE_BETWEEN
                    ),
                    on_click=self.element_click, bgcolor='#ADC4CE', height=80

                )
                self.list_find_product.controls.append(r)

    def find_to_back(self, e):
        self.page.controls.clear()
        AppMain(self.page)
        self.page.update()
    
    def find_to_next(self, e):
        self.page.controls.clear()
        self.page.controls.add(Row(controls=Text('Дальше больше!')))


    def finder_app(self):
        self.create_appbar()
        self.list_find_product = Column(
            height=400,
            scroll='auto',
            controls=[
                Container(height=40)
            ]
        )
        page_1 = Container(
            width=1000,
            height=900,
            border_radius=35,
            bgcolor='#2E4374',
            alignment=alignment.center,
            padding=padding.only(left=80, top=40, right=80, bottom=60),

            content=Column(
                alignment=alignment.top_right,
                controls=[
                    Container(height=40),
                    Text('Добрый день, давайте выберем товары необходимые вам: ', size=44, weight='bold'),
                    Container(height=25),
                    TextField(
                        hint_text='Введите название продукта: ',
                    text_size=20, height=50, on_change=self.find_product, border=border.all(2, '#2E4374')),
                    self.list_find_product,
                    Container(height=10),
                    Row(
                        controls=[
                            TextButton(content=Row(controls=[
                                Text(value= 'Назад',size=40),
                                Icon(icons.ARROW_LEFT, size=140)
                            ]), on_click=self.find_to_back),
                            TextButton(content=Row(controls=[
                                      Icon(icons.ARROW_RIGHT, size=140),
                                      Text(value='В корзину', size=40)
                            ]), on_click=self.find_to_next),
                        ], alignment=MainAxisAlignment.SPACE_BETWEEN
                    )

                ]
            )
        )

        self.page.add(page_1)


def main(page: Page):
    page.title = 'Rock and Shop? Yeep!'
    page.theme = theme.Theme(color_scheme_seed='#654E92')
    page.theme.scrollbar_theme = ft.ScrollbarTheme(thumb_color='black')
    page.theme_mode = "dark"
    page.horizontal_alignment = 'center'
    AppMain(page)

    page.update()


# ft.app(target=main, view=ft.WEB_BROWSER)
ft.app(target=main)