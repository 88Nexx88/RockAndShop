import time

import flet as ft
from flet import *

from value_class import *

class Shop_box():

    def __init__(self, page, value_page):
        self.page = page
        self.value_page = value_page
        self.shop_box()
        self.page.update()



    def create_appbar(self):
        self.list_product_button_clear = ft.TextButton(
            content=ft.Row(
                [
                    Image(src='..\\resources\\icons\\clear_korzina.png'),
                    ft.Text(value='Очистить корзину', size=20, weight=ft.FontWeight.BOLD)
                ]
        ), on_click=self.korzina_full_clear_click)
        self.question = ft.IconButton(on_click=self.quastion_find, icon=ft.icons.QUESTION_MARK)
        self.appbar = AppBar(
            leading=Icon(icons.APPS),
            leading_width=40,
            title=Text("Rock & Shop", weight=FontWeight.BOLD),
            center_title=False,
            bgcolor=colors.SURFACE_VARIANT,
            actions=[
                self.question,
                self.list_product_button_clear
            ]
        )
        self.page.add(self.appbar)


    def minus_click(self, e):
        if int(self.txt_number.value) > 1:
            self.txt_number.value = int(self.txt_number.value) - 1
        else:
            self.txt_number.value = 1
        self.page.update()

    def plus_click(self, e):
        self.txt_number.value = int(self.txt_number.value) + 1
        self.page.update()

    def ok_click(self, e):
        self.dialog.open = False
        index = self.value_page.list_korzina.index(self.product)
        self.value_page.list_korzina[index].count = self.txt_number.value
        self.page.update()
        self.generate_korzina_list()
        
        
        self.page.update()

    def exit_add_click(self, e):
        self.dialog.open = False
        self.page.update()
    
    def delete_click(self, e):
        self.dialog.open = False

        index = self.value_page.list_korzina.index(self.product)
        self.value_page.delete_korzina_product(self.value_page.list_korzina[index])

        
        self.page.clean()
        Shop_box(self.page, self.value_page)
        

    def element_click(self, e):
        count = int(e.control.content.controls[3].controls[3].content.value.replace('Количество товара в штуках: ', ''))
        name = e.control.content.controls[3].controls[1].content.value
        self.txt_number = Text(value=count)
        self.dialog = ft.AlertDialog(
            title=ft.Text("Укажите количество товара: "),
            content=Text(value=name, size=24, max_lines=5, text_align='CENTER', width=100),
            modal=True,
            actions = [
                Column(controls=[ Row(controls=[
                    TextButton(text='Отмена', on_click=self.exit_add_click),
                    IconButton(icons.REMOVE, on_click=self.minus_click),
                    self.txt_number,
                    IconButton(icons.ADD, on_click=self.plus_click),
                    TextButton(text='Изменить', on_click=self.ok_click)], alignment=MainAxisAlignment.SPACE_BETWEEN),
                    TextButton(text='Удалить товар', on_click=self.delete_click)])],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        for i in self.value_page.list_korzina:
            f_name = i.name.content.value
            if f_name == name:
                self.product = i
        self.page.dialog = self.dialog
        self.dialog.open = True
        self.page.update()

    def generate_korzina_list(self):
        self.list_korzina_product.content.controls.clear()
        for i in self.value_page.list_korzina:
            r = Container(
                            content= Row(controls=[
                                Container(width=15),
                                i.image,
                                Container(width=15),
                                Column(controls=[
                                    Container(height=30),
                                    i.name, 
                                    i.info,
                                    Container(Text(value='Количество товара в штуках: '+str(i.count), size=20, color='#75602F', text_align='CENTER'), width=500)
                                    ])
                            ]
                            ),
                            # on_click=self.element_click, bgcolor='#ADC4CE', height=200, border_radius=10)
                            on_click=self.element_click, bgcolor=colors.WHITE, height=200, border_radius=10)
            self.list_korzina_product.content.controls.append(r)
            

    def shop_box(self):
        self.create_appbar()
        if self.value_page.korzina_len == 0:
            self.list_korzina_product = Container(content=Column(
                height=540,
                controls=[
                    Container(height=40),
                    Container(content = Column(controls=[
                        Container(Text(value='Если добавить товары в корзину, она не будет пустой!', size=24, weight=ft.FontWeight.BOLD, color='#1d1e33'), alignment=alignment.center),
                        Container(Image(src='..\\resources\\icons\\void_korzina_rofl.png', height=256, width=256), alignment=alignment.center, padding=padding.only(right=40))]
                    ), bgcolor='#ADC4CE', border_radius=10)
                ]
            ),
            )
        else:
            self.list_korzina_product = Container(content=Column(
                height=540,
                scroll='auto',
                controls=[
                ]
            )
            )
            self.generate_korzina_list()
            
        self.len_korzina = Text(value='Позиций в корзине: '+str(self.value_page.korzina_len), size=24, weight=ft.FontWeight.BOLD, color='#E5C3A6')

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
                    Container(height=20),
                    Text('Корзина: ', size=40, weight='bold'),
                    Container(height=10),
                    self.len_korzina,
                    self.list_korzina_product,
                    Row(
                        controls=[
                            TextButton(content=Row(controls=[
                                Text(value= 'Назад',size=40),
                                Icon(icons.ARROW_LEFT, size=140)
                            ]), on_click=self.find_to_back),
                            TextButton(content=Row(controls=[
                                      Icon(icons.ARROW_RIGHT, size=140),
                                      Text(value='Рассчитать!', size=40)
                            ]), on_click=self.to_calc_page),
                        ], alignment=MainAxisAlignment.SPACE_BETWEEN
                    )

                ]
            )
        )

        self.page.add(page_1)

    def find_to_back(self, e):
        self.page.controls.clear()
        AppFinder(self.page, self.value_page)
    
    def to_calc_page(self, e):
        self.page.controls.clear()
        AppMain(self.page, self.value_page)


    def korzina_full_clear_click(self, e):
        self.dialog = ft.AlertDialog(
            title=ft.Text("Вы уверены?"),
            content=Text('Будет очищена вся корзина!'),
            modal=True,
            actions = [
                    TextButton(text='Нет', on_click=self.not_full_clear_click),
                    TextButton(text='Да', on_click=self.full_clear_click)],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        self.page.dialog = self.dialog
        self.dialog.open = True
        
        self.page.update()
    
    def not_full_clear_click(self, e):
        self.dialog.open = False
        self.page.update()
    
    def full_clear_click(self, e):
        self.dialog.open = False
        self.value_page = Value_page()

        self.page.clean()
        Shop_box(self.page, self.value_page)

        self.page.update()

    def quastion_find(self, event):
        dlg = ft.AlertDialog(title=ft.Text("Нужна помощь?"),content=Column(controls=[
            Text('В данном окне .....'),
            Text('Если ошиблись с выбором, или хотите увеличить количество товара в позиции то ....')
        ], width=400, height=400))
        self.page.dialog = dlg
        dlg.open =True
        self.page.update()


class AppFinder:
  
    def __init__(self, page, value_page):
        self.page = page
        self.value_page = value_page
        self.page.horizontal_alignment = 'center'
        self.page.vertical_alignment = 'start'
        self.Is_has_validate_name = {'status_name': 0, 'status_surname': 0}
        self.Is_has_name_surname = 0
        self.Is_has_session = 0

        self.finder_app()

    def korzina_click(self, e):
        self.page.controls.clear()
        Shop_box(self.page, self.value_page)
    
    def find_to_back(self, e):
        self.page.controls.clear()
        AppMain(self.page, self.value_page)
        

    def quastion_find(self, event):
        # self.page.theme_mode = "light" if self.page.theme_mode == 'dark' else 'dark'
        # self.togglelight_dark.selected = not self.togglelight_dark.selected
        # time.sleep(0.2)
        # self.page.update()
        dlg = ft.AlertDialog(title=ft.Text("Нужна помощь?"),content=Column(controls=[
            Text('В данном окне .....'),
            Text('Если ошиблись с выбором, или хотите увеличить количество товара в позиции то ....')
        ], width=400, height=400))
        self.page.dialog = dlg
        dlg.open =True
        self.page.update()


    def create_appbar(self):
        self.question = ft.IconButton(on_click=self.quastion_find, icon=ft.icons.QUESTION_MARK)
        if self.value_page.korzina_len != 0:
            image = Image(src='..\\resources\\icons\\korzina_add.png')
        else:
            image = Image(src='..\\resources\\icons\\korzina_void.png')
        self.list_product_button = ft.TextButton(
            content=ft.Row(
                [
                    image,
                    ft.Text(value='Корзина:', size=20, weight=ft.FontWeight.BOLD),
                    ft.Text(value=self.value_page.korzina_len, size=20, weight=ft.FontWeight.BOLD, color='#fb2b3a')
                ]
        ), on_click=self.korzina_click)
        self.appbar = ft.AppBar(
            leading=ft.Icon(ft.icons.APPS),
            leading_width=40,
            title=ft.Text("Rock & Shop", weight=ft.FontWeight.BOLD),
            center_title=False,
            bgcolor=ft.colors.SURFACE_VARIANT,
            actions=[
                self.question,
                self.list_product_button
            ],
        )
        self.page.add(self.appbar)

    def find_product(self, e):
        if e.control.value != '':
            self.list_find_product.bgcolor = '#2E4374'
            self.list_find_product.height = 405
            self.list_find_product.content.controls.clear()
            self.list_find_product.content.controls.append(Container(height=1))
            self.generate_product_list(e.control.value)
            self.count_product_find.value = 'Найдено $ товаров!👩🏿‍💻'

            self.page.update()
        else:
            self.list_find_product.content.controls.clear()
            self.list_find_product.content.controls.append(Container(height=1))
            self.count_product_find.value = 'Не знаете что купить? Попробуйте эти товары!👩🏿‍💻'
            self.generate_recom_list()
            self.page.update()

    def generate_recom_list(self):
        for i in range(5):
               r = Container(
                            content= Row(controls=[
                                Container(width=15),
                                Image(src='..\\resources\\vodka_medved.png', width=256, height=190, fit=ft.ImageFit.NONE,
                                    repeat=ft.ImageRepeat.NO_REPEAT,
                                    border_radius=ft.border_radius.all(10)),
                                Container(width=15),
                                Column(controls=[
                                    Container(height=30),
                                    Container(content=Text(value='"Вино Пьетраме Монтепульчано Д`Абруццо DOP красное полусухое"'+str(i), size=24, color='#1d1e33', max_lines=3, text_align='CENTER'), width=500), 
                                    Container(content=
                                            Text(value='Италия, 0.75 л., Абруццо, 13%', size=20, color='#53377a', text_align='CENTER'), width=500)
                                    ])
                            ]
                            ),
                            on_click=self.element_click, bgcolor='#ADC4CE', height=200, border_radius=10)
               self.list_find_product.content.controls.append(r)

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
        self.page.update()
        for i in self.value_page.list_korzina:
            if self.product.name.content.value == i.name.content.value:
                self.dublicate_product()
                return
            
        old_value = self.value_page.korzina_len
        self.list_product_button.content = ft.Row(
            [  
                Image(src='..\\resources\\icons\\korzina_add.png'),
                ft.Text(value='Корзина:', size=20, weight=ft.FontWeight.BOLD),
                ft.Text(value=old_value+1, size=20, weight=ft.FontWeight.BOLD, color='#fb2b3a')
            ]
        )
        self.product.count = self.txt_number.value
        self.value_page.add_korzina_product(self.product)
        
        self.page.update()

    def end_dublicate(self, e):
        self.dialog.open = False
        self.page.update()

    def dublicate_product(self):
        self.dialog = ft.AlertDialog(title=ft.Text("Дубликат!", size=34), modal=True, content=Column(controls=[Text('Вы добавили в корзину товар, который уже в ней присутствует!', size=20),
                                                                  Text('Если вы хотите увеличить количество товара данной позиции, перейдите в корзину!', size=20)], width=400, height=180), 
                                                                  actions=[
                                                                      Row(controls=[Image(src='..\\resources\\icons\\dublicate.png'),
                                                                                    TextButton(content=Text('Ок', size=34), on_click=self.end_dublicate, )], alignment=MainAxisAlignment.SPACE_BETWEEN)
                                                                            ]
                                    )
        self.page.dialog = self.dialog
        self.dialog.open = True
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
        image = e.control.content.controls[1]
        name = e.control.content.controls[3].controls[1]
        info = e.control.content.controls[3].controls[2]
        self.product = Product(name, info, 0, image)
        self.page.dialog = self.dialog
        self.dialog.open = True
        self.page.update()

    def generate_product_list(self, zapros):
            for i in range(80):
               r = Container(
                            content= Row(controls=[
                                Container(width=15),
                                Container(Image(src='..\\resources\\vodka_medved.png', fit=ft.ImageFit.NONE,
                                    repeat=ft.ImageRepeat.NO_REPEAT),
                                    border_radius=ft.border_radius.all(10), width=200, height=190, bgcolor=colors.WHITE),
                                Container(width=15),
                                Column(controls=[
                                    Container(height=30),
                                    Container(content=Text(value='"Вино Пьетраме Монтепульчано Д`Абруццо DOP красное полусухое"'+str(i), size=24, color='#1d1e33', max_lines=3, text_align='CENTER'), width=500), 
                                    Container(content=
                                            Text(value='Италия, 0.75 л., Абруццо, 13%', size=20, color='#53377a', text_align='CENTER'), width=500)
                                    ])
                            ]
                            ),
                            # on_click=self.element_click, bgcolor='#ADC4CE', height=200, border_radius=10)
                            on_click=self.element_click, bgcolor=colors.WHITE, height=200, border_radius=10)
               self.list_find_product.content.controls.append(r)

    
    def finder_app(self):
        self.create_appbar()
        self.list_find_product = Container(content=Column(
            height=400,
            scroll='auto',
            controls=[
                Container(height=40)
            ]
        )
        )
        
        self.count_product_find = Text(value='', size=24, weight=ft.FontWeight.BOLD, color='#E5C3A6')
        self.find_label = TextField(
                        hint_text='Введите название продукта: ',text_size=20, height=50, on_change=self.find_product, border=border.all(2, '#2E4374'), 
                        # bgcolor='#ADC4CE', text_style=TextStyle(color='black'))
                        bgcolor=colors.WHITE, text_style=TextStyle(color='black'))
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
                    Container(height=20),
                    Text('Добрый день, давайте выберем товары необходимые вам: ', size=44, weight='bold'),
                    Container(height=20),
                    self.find_label,
                    self.count_product_find,
                    self.list_find_product,
                    Row(
                        controls=[
                            TextButton(content=Row(controls=[
                                Text(value= 'Назад',size=40),
                                Icon(icons.ARROW_LEFT, size=140)
                            ]), on_click=self.find_to_back),
                            TextButton(content=Row(controls=[
                                      Icon(icons.ARROW_RIGHT, size=140),
                                      Text(value='В корзину', size=40)
                            ]), on_click=self.korzina_click),
                        ], alignment=MainAxisAlignment.SPACE_BETWEEN
                    )

                ]
            )
        )

        self.page.add(page_1)


class AppMain:
    

    def __init__(self, page, value_page):
        self.page = page
        self.value_page = value_page
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
                                            Text(value='Вперёд👍', size=41)
                                          
                            ]), on_click=self.to_next)
            ], alignment=MainAxisAlignment.SPACE_BETWEEN))
                
            ], alignment=alignment.center
            )
        )
    
        
        self.page.add(self.start_view)
        self.page.update()

    def to_next(self, event):
        self.page.controls.clear()
        AppFinder(self.page, self.value_page)
        self.page.update()

    def create_appbar(self):
        self.appbar = ft.AppBar(
            leading=ft.Icon(ft.icons.APPS),
            leading_width=40,
            title=ft.Text("Rock & Shop", weight=ft.FontWeight.BOLD),
            center_title=False,
            bgcolor=ft.colors.SURFACE_VARIANT
        )
        self.page.add(self.appbar)


def main(page: Page):
        page.title = 'Rock and Shop? Yeep!'
        page.theme = theme.Theme(color_scheme_seed='#654E92')
        page.theme.scrollbar_theme = ScrollbarTheme(thumb_color='black')
        page.theme_mode = "dark"
        page.horizontal_alignment = 'center'
        page.window_min_width = 1080
        page.window_min_height = 1080
        page.window_max_height = 1080
        page.window_max_width = 1920
        page.window_width = 1080
        # page.window_height = 1080
        value_korzina = Value_page()
        AppMain(page, value_korzina)

    
        page.update()


# ft.app(target=main, view=ft.WEB_BROWSER)
app(target=main)