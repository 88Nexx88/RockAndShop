import re
import time
import flet as ft
from flet import *
from ymaps import *

from flet_gui.AutomaticImageCarousel import AutomaticImageCarousel
from storage.value_class import *
import find_products
from storage import result_find


class Calc_reclam():
    def __init__(self, page, result):
        self.page = page
        self.result = result
        self.calc_reclam()
        self.page.update()
        self.calculation()

    def create_appbar(self):
        self.appbar = ft.AppBar(
            leading=ft.Icon(ft.icons.APPS),
            leading_width=40,
            title=ft.Text("Rock & Shop", weight=ft.FontWeight.BOLD),
            center_title=False,
            bgcolor=ft.colors.SURFACE_VARIANT,
            actions=[
            ],
        )
        self.page.add(self.appbar)

    def next_page(self, e):
        print("!!!")

    def calculation(self):
        time.sleep(10)
        self.progress_bar.content.controls[0].value = 'Рассчёт окончен!'
        self.page.update()
        time.sleep(2)
        self.progress_bar.content = Row(
            controls=[
                Text(value=''),
                TextButton(content=Row(controls=[
                    Icon(icons.ARROW_RIGHT, size=self.page.window_height * 0.1056),
                    Text(value='Далее', size=self.page.window_height * 0.024)
                ]), on_click=self.next_page),
            ], alignment=MainAxisAlignment.SPACE_BETWEEN
        )
        self.page.update()

    def exit_reclama(self):
        self.progress_bar.content.controls[0].value = 'Рассчёт окончен!'
    def calc_reclam(self):
        self.create_appbar()
        self.progress_bar = Container()
        self.progress_bar.content = Column(controls=[Text(value='', style="headlineSmall"),
                                                     ft.ProgressBar(width=self.page.window_width * 0.75, height=self.page.window_height * 0.037, bgcolor="white")],
                                           alignment=alignment.center)
        self.progress_bar.content.controls[0].value = 'Рассчитываем вашу покупку...'
        if self.page.window_height > 900:
            images = [['..\\resources\\reclam\\1080\\vlsu.png', 'https://prkom.vlsu.ru/'],['..\\resources\\reclam\\1080\\izi1.png', 'http://izi.vlsu.ru/index.php?id=2'], ['..\\resources\\reclam\\1080\\izi2.png', 'https://vk.com/izivlsu']]
        else:
            images = [['..\\resources\\reclam\\768\\vlsu.png', 'https://prkom.vlsu.ru/'],
                      ['..\\resources\\reclam\\768\\izi1.png', 'http://izi.vlsu.ru/index.php?id=2'],
                      ['..\\resources\\reclam\\768\\izi2.png', 'https://vk.com/izivlsu']]

        page_1 = Container(
            width=1000,
            height=self.page.window_height * 0.87,
            border_radius=35,
            bgcolor='#2E4374',
            alignment=alignment.center,
            padding=padding.only(left=80, top=self.page.window_height * 0.037, right=80),
            content=Column(
                alignment=MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    Column(alignment=MainAxisAlignment.SPACE_BETWEEN, controls=[
                        Container(height=10),
                        Container(content=Text('Пока программа рассчитывает оптимальный вариант покупки, ознакомьтесь с предложением наших спонсоров!',
                                               size=self.page.window_height * 0.0296,
                                               weight='bold'), alignment=alignment.center, width=900),
                            Container(content=AutomaticImageCarousel(
                                images_list=images,
                                perseverance_time=7.0,
                                animations=[ft.AnimationCurve.EASE_IN, ft.AnimationCurve.EASE_IN_OUT_CUBIC_EMPHASIZED],
                                descriptive=True), height=self.page.window_height * 0.56, alignment=alignment.center)
                            ]
                    ),
                    self.progress_bar,
                    Container(height=20),

                ]
            )
        )

        self.page.add(page_1)

        # self.page.update()

class Calc_param():
    def __init__(self, page, value_page):
        self.page = page
        self.value_page = value_page
        self.calc_param()
        self.page.update()
        self.address = ''
        self.mode = ''
        self.effects_mode = ''

    def korzina_click(self, e):
        self.page.controls.clear()
        Shop_box(self.page, self.value_page)

    def quastion_find(self, event):
        dlg = ft.AlertDialog(title=ft.Text("Нужна помощь?"), content=Column(controls=[
            Text('В данном окне .....'),
            Text('Если ошиблись с выбором, или хотите увеличить количество товара в позиции то ....')
        ], width=400, height=self.page.window_height * 0.37037))
        self.page.dialog = dlg
        dlg.open = True
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

    def find_to_back(self, e):
        self.page.controls.clear()
        Shop_box(self.page, self.value_page)

    def find_geo(self, e):
        client = Geocode('9fa910c6-ae58-4d88-972f-d0d5aae763ca')
        response = client.geocode(self.find_geolo.value + ' ' + self.find_geolo.suffix_text, sco='latlong')
        coordinates = response['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos']
        name_img = response['response']['GeoObjectCollection']['featureMember'][0]['GeoObject'][
            'metaDataProperty']['GeocoderMetaData']['text']
        client = Static(url='1.x')
        self.address = [coordinates, name_img]
        name_img = re.sub('[^A-Za-zА-Яа-я0-9 ]+', '', name_img)
        client.load_image(path='user\\' + name_img + '.png', l=['map'], ll=coordinates.split(' '), z=16, scale=1.2,
                          size=[350, 350],
                          pt=[
                              coordinates.replace(' ', ',') + ',pmwtm1'])
        self.geolo_pos.content = Image(src='user\\' + name_img + '.png')
        dlg_modal = ft.AlertDialog(
            modal=True,
            title=ft.Text("Это геолокация та, что вы указали?", weight=FontWeight.BOLD, size=24),
            content=self.geolo_pos,
            actions=[
                ft.TextButton(content=Text("Нет!", weight=FontWeight.BOLD, size=20),
                              on_click=self.exit_click),
                ft.TextButton(content=Text("Да!", weight=FontWeight.BOLD, size=20),
                              on_click=self.exit_ok_click),
            ],
            actions_alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
        self.dialog = dlg_modal
        self.page.dialog = self.dialog
        self.dialog.open = True

        self.page.update()

    def dropdown_changed_mode(self, e):
        self.mode = e.control.value

    def dropdown_changed_effects(self, e):
        self.effects_mode = e.control.value
    def dropdown_changed(self, e):
        self.find_geolo.value = e.control.value
        client = Geocode('9fa910c6-ae58-4d88-972f-d0d5aae763ca')
        response = client.geocode(self.find_geolo.value + ' ' + self.find_geolo.suffix_text, sco='latlong')
        coordinates = response['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos']
        client = Static(url='1.x')
        name_img = response['response']['GeoObjectCollection']['featureMember'][0]['GeoObject'][
            'metaDataProperty']['GeocoderMetaData']['text']
        self.address = [coordinates, name_img]
        name_img = re.sub('[^A-Za-zА-Яа-я0-9 ]+', '', name_img)
        client.load_image(path='user\\' + name_img + '.png', l=['map'], ll=coordinates.split(' '), z=16, scale=1.2,
                          size=[350, 350],
                          pt=[
                              coordinates.replace(' ', ',') + ',pmwtm1'])
        self.geolo_pos.content = Image(src='user\\'+name_img+'.png')
        dlg_modal = ft.AlertDialog(
            modal=True,
            title=ft.Text("Это геолокация та, что вы указали?", weight=FontWeight.BOLD, size=24),
            content=self.geolo_pos,
            actions=[
                ft.TextButton(content=Text("Нет!", weight=FontWeight.BOLD, size=20),
                              on_click=self.exit_click),
                ft.TextButton(content=Text("Да!", weight=FontWeight.BOLD, size=20),
                              on_click=self.exit_ok_click),
            ],
            actions_alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
        self.dialog = dlg_modal
        self.page.dialog = self.dialog
        self.dialog.open = True

        self.page.update()

    def exit_ok_click(self, e):
        self.dialog.open = False
        self.page.update()

    def exit_click(self, e):
        self.address = ''
        self.dialog.open = False
        self.page.update()


    def write_save_address(self, address):
        with open('user/save_addr', encoding='utf-8', mode='r') as file:
            for line in file.readlines():
                if line.rstrip() == address:
                    return
        with open('user/save_addr', encoding='utf-8', mode='a') as file:
            file.write('\n'+address)
            file.close()

    def next_page(self, e):
        products = []
        counts = []
        shops = []
        prices = []
        user_counts = []
        adr = self.address
        if adr == '':
            dlg_modal = ft.AlertDialog(
                modal=True,
                title=ft.Text("Укажите ваше местоположение!", weight=FontWeight.BOLD, size=24),
                actions=[
                    ft.Text(),
                    ft.TextButton(content=Text("Хорошо", weight=FontWeight.BOLD, size=20),
                                  on_click=self.exit_ok_click),
                ],
                actions_alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
            self.dialog = dlg_modal
            self.page.dialog = self.dialog
            self.dialog.open = True

            self.page.update()
            return
        self.write_save_address(adr[1].split('Владимир, ')[1])
        effects_mode = self.effects_mode
        auto_mode = self.mode
        if effects_mode == '':
            effects_mode = self.page.controls[1].content.controls[0].controls[3].controls[0].value
        if auto_mode == '':
            auto_mode = self.page.controls[1].content.controls[0].controls[3].controls[1].value

        for i in self.value_page.list_korzina:
            res = find_products.search_products(i.name.content.content.value)
            user_counts.append(i.count)
            products.append(res[0]['name'])
            prices.append(res[0]['price'])
            counts.append(res[0]['count'])
            shops.append(res[0]['address'])

        self.result = result_find.Result(products, prices, counts, shops, adr, effects_mode, auto_mode, user_counts)
        print(products, prices, counts, shops, adr, effects_mode, auto_mode, user_counts)
        self.page.controls.clear()
        Calc_reclam(self.page, self.result)

    def calc_param(self):
        self.create_appbar()

        cg = Dropdown(
                          value='Самый оптимальный',
                          label="Параметр эффективности варианта",
                          bgcolor='#667FBA',
                          focused_bgcolor='#667FBA',
                          filled=True,
                          label_style=TextStyle(size=18, color='white', weight='bold'),

                          text_style=TextStyle(size=self.page.window_height * 0.0185, color='white',
                                 weight='bold'),
                          width=400, on_change=self.dropdown_changed_effects,
                          border_color='gray', border_width=1.5,
                          border_radius=10, options=[
                              ft.dropdown.Option("Самый быстрый"),
                              ft.dropdown.Option("Самый выгодный по цене"),
                              ft.dropdown.Option("Самый оптимальный")
            ])

        rg = Dropdown(
                          value='Пешком',
                          label="Параметры маршрута",
                          bgcolor='#667FBA',
                          focused_bgcolor='#667FBA',
                          filled=True,
                          label_style=TextStyle(size=18, color='white', weight='bold'),

                          text_style=TextStyle(size=self.page.window_height * 0.0185, color='white',
                                                 weight='bold'),
                          width=400, on_change=self.dropdown_changed_mode,
                          border_color='gray', border_width=1.5,
                          border_radius=10, options=[
                              ft.dropdown.Option("Пешком"),
                              ft.dropdown.Option("На машине")])

        self.parametr_var = Row(controls=[
                    cg,rg], alignment=MainAxisAlignment.SPACE_BETWEEN)

        self.find_geolo =  TextField(
                    keyboard_type='STREET_ADDRESS',
                    prefix_icon=ft.icons.SEARCH,
                    # suffix=Text('Владимир, Россия'),
                    suffix_text='Владимир, Россия',
                    hint_text='Введите ваш адрес: ', hint_style=TextStyle(color='#6B6767'),
                    text_size=self.page.window_height * 0.0225, height=self.page.window_height * 0.06,
                    border=border.all(2, '#2E4374'),
                    # bgcolor='#ADC4CE', text_style=TextStyle(color='black'))
                    bgcolor=colors.WHITE, text_style=TextStyle(color='black', weight='bold'), on_submit=self.find_geo)
        self.geolo_pos = Container(height=400, content=Text(value=''), alignment=alignment.center, width=400)

        options = []
        with open('user\\save_addr', encoding='utf-8', mode='r') as file:
            lines = file.readlines()
            for line in lines:
                options.append(ft.dropdown.Option(line.rstrip('\n')))

        page_1 = Container(
            width=1000,
            height=self.page.window_height * 0.87,
            border_radius=35,
            bgcolor='#2E4374',
            alignment=alignment.center,
            padding=padding.only(left=80, top=self.page.window_height*0.037, right=80),

            content=Column(
                alignment=MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    Column(controls=[
                    Container(height=10),
                    Container(content=Text('Остался заключительный этап. Выберите предпочтения по покупке: ', size=self.page.window_height * 0.0296,
                                           weight='bold'), alignment=alignment.center, width=900),
                    Container(height=10),
                    self.parametr_var,
                    Container(height=10),
                    Container(content=Text('А теперь определим ваше местоположение: ',
                                           size=self.page.window_height * 0.0296,
                                           weight='bold'), alignment=alignment.center, width=900),
                    self.find_geolo,
                    Row(controls=[Text(value=''),
                                  Dropdown(
                                      value='',
                                      label="Сохранённые точки!",
                                      bgcolor='#667FBA',
                                      focused_bgcolor='#667FBA',
                                      filled=True,
                                      label_style=TextStyle(size=18, color='white', weight='bold'),

                                      text_style=TextStyle(size=self.page.window_height * 0.0185, color='white',
                                                           weight='bold'),
                                      width=400, on_change=self.dropdown_changed,
                                      border_color='gray', border_width=1.5,
                                      border_radius=10, options=options
                                          )
                                  ], alignment=MainAxisAlignment.SPACE_BETWEEN),]
                    ),
                    Row(
                        controls=[
                            TextButton(content=Row(controls=[
                                Text(value='Назад', size=self.page.window_height * 0.024),
                                Icon(icons.ARROW_LEFT, size=self.page.window_height * 0.1056)
                            ]), on_click=self.find_to_back),
                            TextButton(content=Row(controls=[
                                Icon(icons.ARROW_RIGHT, size=self.page.window_height * 0.1056),
                                Text(value='Далее', size=self.page.window_height * 0.024)
                            ]), on_click=self.next_page),
                        ], alignment=MainAxisAlignment.SPACE_BETWEEN
                    )

                ]
            )
        )

        self.page.add(page_1)


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

    def dropdown_changed(self, e):
        self.sort_list = e.control.value
        self.value_page.sort_list_korzina(e.control.value)
        self.generate_korzina_list()
        self.page.update()
    def minus_click(self, e):
        if int(self.txt_number.value) > 1:
            self.txt_number.value = int(self.txt_number.value) - 1
        else:
            self.txt_number.value = 1
        self.page.update()

    def plus_click(self, e):
        if int(self.txt_number.value) + 1 <= self.product.max_count:
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
        count = int(e.control.content.controls[3].controls[5].content.value.replace('Количество товара в штуках: ', ''))
        name = e.control.content.controls[3].controls[2].content.content.value
        self.txt_number = Text(value=count)
        self.dialog = ft.AlertDialog(
            title=ft.Text("Укажите количество товара: "),
            content=Text(value=name, size=24, max_lines=5, text_align='CENTER', width=100),
            modal=True,
            actions=[
                Column(controls=[Row(controls=[
                    TextButton(text='Отмена', on_click=self.exit_add_click),
                    IconButton(icons.REMOVE, on_click=self.minus_click),
                    self.txt_number,
                    IconButton(icons.ADD, on_click=self.plus_click),
                    TextButton(text='Изменить', on_click=self.ok_click)], alignment=MainAxisAlignment.SPACE_BETWEEN),
                    TextButton(text='Удалить товар', on_click=self.delete_click)])],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        for i in self.value_page.list_korzina:
            f_name = i.name.content.content.value
            if f_name == name:
                self.product = i
        self.page.dialog = self.dialog
        self.dialog.open = True
        self.page.update()

    def generate_korzina_list(self):
        self.list_korzina_product.content.controls.clear()
        for i in self.value_page.list_korzina:
            r = Container(
                content=Row(controls=[
                    Container(width=15),
                    i.image,
                    Container(width=15),
                    Column(controls=[
                        Container(height=10),
                        i.shops,
                        i.name,
                        i.info,
                        i.price,
                        Container(Text(value='Количество товара в штуках: ' + str(i.count), size=20, color='#75602F',
                                       text_align='CENTER'), width=500)
                    ], alignment=MainAxisAlignment.SPACE_BETWEEN)
                ]
                ),
                # on_click=self.element_click, bgcolor='#ADC4CE', height=200, border_radius=10)
                on_click=self.element_click, bgcolor=colors.WHITE, height=250, border_radius=10, padding=padding.all(10))
            self.list_korzina_product.content.controls.append(r)

    def shop_box(self):
        self.create_appbar()


        if self.value_page.korzina_len == 0:
            self.list_korzina_product = Container(content=Column(
                height=self.page.window_height * 0.5055,
                controls=[
                    Container(height=10),
                    Container(content=Column(controls=[
                        Container(Text(value='Если добавить товары в корзину, она не будет пустой!', size=24,
                                       weight=ft.FontWeight.BOLD, color='#1d1e33'), alignment=alignment.center),
                        Container(Image(src='..\\resources\\icons\\void_korzina_rofl.png', height=256, width=256),
                                  alignment=alignment.center, padding=padding.only(right=40))]
                    ), bgcolor='white', border_radius=10)
                ]
            ),
            )
        else:
            self.list_korzina_product = Container(content=Column(
                height=self.page.window_height * 0.5055,
                scroll='ALWAYS',
                controls=[
                ]
            )
            )
            self.generate_korzina_list()

        self.len_korzina = Text(value='Позиций в корзине: ' + str(self.value_page.korzina_len), size=24,
                                weight=ft.FontWeight.BOLD, color='#E5C3A6')
        self.block_bottom_finder = Row(controls=[self.len_korzina,
                                                 # Row(controls=[Text('Сортировать по: ', size=22, weight=ft.FontWeight.BOLD), Dropdown(value='Названию',width=400, on_change=self.dropdown_changed, text_size= 22,
                                                 Row(controls=[Dropdown(value='Названию', label="Сортировать по:",
                                                                        # bgcolor='#9966cc',
                                                                        bgcolor='#667FBA',
                                                                        focused_bgcolor='#667FBA',
                                                                        filled=True,
                                                                        label_style=TextStyle(
                                                                            size=self.page.window_height * 0.0225,
                                                                            color='white',
                                                                            weight='bold'),
                                                                        width=400,
                                                                        text_style=TextStyle(
                                                                            size=self.page.window_height * 0.0185,
                                                                            color='white',
                                                                            weight='bold'),
                                                                        on_change=self.dropdown_changed,
                                                                        border_color='gray', border_width=1.5,
                                                                        border_radius=10, options=[
                                                         ft.dropdown.Option("Названию"),
                                                         ft.dropdown.Option("Минимальной цене"),
                                                         ft.dropdown.Option("Максимальной цене"),
                                                         ft.dropdown.Option("Магазин Бристоль"),
                                                         ft.dropdown.Option("Магазин КБ")])])],
                                       alignment=MainAxisAlignment.SPACE_BETWEEN)

        page_1 = Container(
            width=1000,
            height=self.page.window_height * 0.87,
            border_radius=35,
            bgcolor='#2E4374',
            alignment=alignment.center,
            padding=padding.only(left=80, top=self.page.window_height*0.037, right=80),

            content=Column(
                alignment=MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    Container(height=7),
                    Text('Корзина: ', size=self.page.window_height * 0.037, weight='bold'),
                    Container(height=2),
                    self.block_bottom_finder,
                    self.list_korzina_product,
                    Row(
                        controls=[
                            TextButton(content=Row(controls=[
                                Text(value='Назад', size=self.page.window_height * 0.024),
                                Icon(icons.ARROW_LEFT, size=self.page.window_height * 0.1056)
                            ]), on_click=self.find_to_back),
                            TextButton(content=Row(controls=[
                                Icon(icons.ARROW_RIGHT, size=self.page.window_height * 0.1056),
                                Text(value='Рассчитать!', size=self.page.window_height * 0.024)
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
        if self.value_page.korzina_len != 0:
            self.page.controls.clear()
            Calc_param(self.page, self.value_page)
        else:
            dlg_modal = ft.AlertDialog(
                modal=True,
                title=ft.Text("Внимание!", weight=FontWeight.BOLD, size=24),
                content=ft.Text("С пустой корзиной, приложение вам ничего не рассчитает 😭", weight=FontWeight.BOLD,
                                size=20),
                actions=[
                    ft.Text(value=''),
                    ft.TextButton(content=Text("Сейчас добавлю товар!", weight=FontWeight.BOLD, size=20),
                                  on_click=self.exit_add_click),
                ],
                actions_alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
            self.dialog = dlg_modal
            self.page.dialog = self.dialog
            self.dialog.open = True
        self.page.update()

    def korzina_full_clear_click(self, e):
        self.dialog = ft.AlertDialog(
            title=ft.Text("Вы уверены?"),
            content=Text('Будет очищена вся корзина!'),
            modal=True,
            actions=[
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
        dlg = ft.AlertDialog(title=ft.Text("Нужна помощь?"), content=Column(controls=[
            Text('В данном окне .....'),
            Text('Если ошиблись с выбором, или хотите увеличить количество товара в позиции то ....')
        ], width=400, height=self.page.window_height * 0.37))
        self.page.dialog = dlg
        dlg.open = True
        self.page.update()


class AppFinder:

    def __init__(self, page, value_page):
        self.page = page
        self.page.on_resize = None
        # self.page.on_resize = self.change_window_2
        self.value_page = value_page
        self.page.horizontal_alignment = 'center'
        self.page.vertical_alignment = 'start'
        self.Is_has_validate_name = {'status_name': 0, 'status_surname': 0}
        self.Is_has_name_surname = 0
        self.Is_has_session = 0
        self.sort_list = 'Названию'
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
        dlg = ft.AlertDialog(title=ft.Text("Нужна помощь?"), content=Column(controls=[
            Text('В данном окне .....'),
            Text('Если ошиблись с выбором, или хотите увеличить количество товара в позиции то ....')
        ], width=400, height=400))
        self.page.dialog = dlg
        dlg.open = True
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
        # if e.control.value != '':
        self.find_page = 0
        self.list_find_product.bgcolor = '#2E4374'
        self.list_find_product.height = self.page.window_height * 0.440
        self.list_find_product.content.controls.clear()
        self.list_find_product.content.controls.append(Container(height=1))
        self.generate_product_list(e.control.value)

        self.page.update()

    # else:
    # self.list_find_product.content.controls.clear()
    # self.list_find_product.content.controls.append(Container(height=1))
    # self.count_product_find.value = 'Не знаете что купить? Попробуйте эти товары!'
    # self.generate_recom_list()
    # self.page.update()


    def minus_click(self, e):
        if int(self.txt_number.value) > 1:
            self.txt_number.value = int(self.txt_number.value) - 1
        else:
            self.txt_number.value = 1
        self.page.update()

    def plus_click(self, e):
        if (int(self.txt_number.value) + 1) <= self.max_count_product:
            self.txt_number.value = int(self.txt_number.value) + 1
        self.page.update()

    def add_click(self, e):
        self.dialog.open = False
        self.page.update()
        for i in self.value_page.list_korzina:
            if self.product.name.content.content.value == i.name.content.content.value:
                self.dublicate_product()
                return
            if self.value_page.korzina_len > 100:
                self.len_korzina_left()
                return

        old_value = self.value_page.korzina_len
        self.list_product_button.content = ft.Row(
            [
                Image(src='..\\resources\\icons\\korzina_add.png'),
                ft.Text(value='Корзина:', size=20, weight=ft.FontWeight.BOLD),
                ft.Text(value=old_value + 1, size=20, weight=ft.FontWeight.BOLD, color='#fb2b3a')
            ]
        )

        self.product.count = self.txt_number.value
        self.value_page.add_korzina_product(self.product)
        self.list_find_product.content.controls.clear()
        self.generate_product_list(self.find_label.value)
        self.page.update()

    def end_dublicate(self, e):
        self.dialog.open = False
        self.page.update()


    def len_korzina_left(self):
        self.dialog = ft.AlertDialog(title=ft.Text("Лимит корзины!", size=34), modal=True, content=Column(
            controls=[Text('Вы добавили в корзину слишком много позиций!', size=20)],
            width=400, height=180),
                                     actions=[
                                         Row(controls=[Text(),
                                                       TextButton(content=Text('Ок', size=34),
                                                                  on_click=self.end_dublicate, )],
                                             alignment=MainAxisAlignment.SPACE_BETWEEN)
                                     ]
                                     )
        self.page.dialog = self.dialog
        self.dialog.open = True
        self.page.update()
    def dublicate_product(self):
        self.dialog = ft.AlertDialog(title=ft.Text("Дубликат!", size=34), modal=True, content=Column(
            controls=[Text('Вы добавили в корзину товар, который уже в ней присутствует!', size=20),
                      Text('Если вы хотите увеличить количество товара данной позиции, перейдите в корзину!', size=20)],
            width=400, height=180),
                                     actions=[
                                         Row(controls=[Image(src='..\\resources\\icons\\dublicate.png'),
                                                       TextButton(content=Text('Ок', size=34),
                                                                  on_click=self.end_dublicate, )],
                                             alignment=MainAxisAlignment.SPACE_BETWEEN)
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
        self.max_count_product = int((e.control.content.controls[4].content.controls[0].content.message).split(': ')[1])
        self.dialog = ft.AlertDialog(
            title=ft.Text("Укажите количество товара: "),
            modal=True,
            actions=[
                TextButton(text='Отмена', on_click=self.exit_add_click),
                IconButton(icons.REMOVE, on_click=self.minus_click),
                self.txt_number,
                IconButton(icons.ADD, on_click=self.plus_click),
                TextButton(text='Добавить', on_click=self.add_click)],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        image = e.control.content.controls[0]
        shops = e.control.content.controls[2].controls[1]
        name = e.control.content.controls[2].controls[2]
        info = e.control.content.controls[2].controls[3]
        price = e.control.content.controls[2].controls[4]
        self.product = Product(name, info, 0, image, shops, price, self.max_count_product)
        self.page.dialog = self.dialog
        self.dialog.open = True
        self.page.update()


    def right_padej(self, n):
        if (n % 100 / 10 == 1):
            return "товаров"
        if (n % 10 == 1):
            return "товар"
        if (n % 10 == 2 or n % 10 == 3 or n % 10 == 4):
            return "товарa"
        else:
            return "товаров"


    def sort_res(self, res):
        if self.sort_list == 'Названию':
            return res
        elif self.sort_list == 'Минимальной цене':
            a = sorted(res.items(), key=lambda x: float(x[1]['price']))
            res_new = {}
            for i, val in a:
                res_new[i] = val
            return res_new
        elif self.sort_list == 'Максимальной цене':
            a = sorted(res.items(), key=lambda x: float(x[1]['price']), reverse=True)
            res_new = {}
            for i, val in a:
                res_new[i] = val
            return res_new
        elif self.sort_list == 'Магазин КБ':
            a = sorted(res.items(), key=lambda x: x[1]['name_shop'], reverse=True)
            res_new = {}
            for i, val in a:
                res_new[i] = val
            return res_new
        elif self.sort_list == 'Магазин Бристоль':
            a = sorted(res.items(), key=lambda x: x[1]['name_shop'])
            res_new = {}
            for i, val in a:
                res_new[i] = val
            return res_new
        else:
            return res

    def click_page(self, e):
        self.more_list_find_product.content.controls.clear()
        self.list_find_product.content.controls.clear()
        self.list_find_product.content.controls.append(Container(height=1))
        self.find_page = e.control.content.value
        if int(e.control.content.value) == self.current_pages_find:

                keys = list(self.res.keys())[int(e.control.content.value)*50 - 50:]
                self.more_list_find_product.content.controls.append(
                    TextButton(content=Text(str(int(e.control.content.value) - 1), size=25), on_click=self.click_page))
                self.more_list_find_product.content.controls.append(
                    Text('Страница товаров ' + e.control.content.value, size=25))
                self.more_list_find_product.content.controls.append(TextButton(content=Text('', size=25)))
        elif int(e.control.content.value) == 1:
            keys = list(self.res.keys())[:50]
            self.more_list_find_product.content.controls.append(TextButton(content=Text('', size=25)))
            self.more_list_find_product.content.controls.append(
                Text('Страница товаров ' + e.control.content.value, size=25))
            self.more_list_find_product.content.controls.append(
                TextButton(content=Text(str(int(e.control.content.value) + 1), size=25), on_click=self.click_page))
        else:
                keys = list(self.res.keys())[int(e.control.content.value) * 50  - 50:(int(e.control.content.value)+1) * 50  - 50]
                self.more_list_find_product.content.controls.append(TextButton(content=Text(str(int(e.control.content.value) - 1), size=25), on_click=self.click_page))
                self.more_list_find_product.content.controls.append(Text('Страница товаров ' + e.control.content.value, size=25))
                self.more_list_find_product.content.controls.append(TextButton(content=Text(str(int(e.control.content.value) + 1), size=25), on_click=self.click_page))
        for i in keys:

            # if len(res) > 70:
            #     if res[i]['name'] == stop_res['name']:
            #         break
            if self.res[i]['name_shop'] == 'bristol':
                shop_name = Row(controls=[Image(src='..\\resources\\icons_shops\\bristol.jpg', width=25, height=25),
                                          Text('Бристоль', color='#1d1e33', size=20)])
            elif self.res[i]['name_shop'] == 'КБ':
                shop_name = Row(controls=[Image(src='..\\resources\\icons_shops\\kb.png', width=25, height=25),
                              Text('Красное и белое', color='#1d1e33', size=20)])
            else:
                shop_name = [
                    Row(controls=[Image(src='..\\resources\\icons_shops\\bristol.jpg', width=25, height=25),
                                  Text('Пятёрочка', color='#1d1e33', size=20)]),
                    Row(controls=[Image(src='..\\resources\\icons_shops\\kb.png', width=25, height=25),
                                  Text('Красное и белое', color='#1d1e33', size=20)])]
            self.product_add_bool = Container()
            for product in self.value_page.list_korzina:
                if product.name.content.content.value == self.res[i]['name']:
                    self.product_add_bool = Tooltip(message='Товар уже добавлен!',
                            content=Container(Icon(icons.CHECK_BOX, color='green', size=42)),
                            bgcolor='#2E4374', text_style=ft.TextStyle(size=15, color=ft.colors.WHITE),
                            wait_duration=200, border=border.all(1, 'gray'))
                    break

            r = Container(
                content=Row(controls=[
                    Container(Image(src=self.res[i]['pic_url'], width=210, height=200),
                              border_radius=ft.border_radius.all(10), width=200, height=190, bgcolor=colors.WHITE,
                              padding=padding.all(5)),
                    Container(width=1),
                    Column(controls=[
                        Container(height=self.page.window_height * 0.0139),
                        Container(content=Tooltip(message='Наличие товара в магазине', content=Row(controls=
                        [shop_name],
                            alignment=MainAxisAlignment.CENTER), bgcolor='#667FBA',
                                                  text_style=ft.TextStyle(size=15, color=ft.colors.WHITE),
                                                  wait_duration=200, border=border.all(1, 'gray')), width=500),

                        Container(content=
                                  Tooltip(message='Описание товара', content=
                                  Text(value=self.res[i]['name'],
                                       size=24, color='#1d1e33', max_lines=3, text_align='CENTER'),
                                          bgcolor='#667FBA', text_style=ft.TextStyle(size=15, color=ft.colors.WHITE),
                                          wait_duration=200, border=border.all(1, 'gray')),
                                  width=500),
                        Container(),
                        # Container(content=Tooltip(message='Информация о товаре', content=
                        # Text(value='Италия, 0.75 л., Абруццо, 13%', size=20, color='#53377a', text_align='CENTER'),
                        #                           bgcolor='#667FBA',
                        #                           text_style=ft.TextStyle(size=15, color=ft.colors.WHITE),
                        #                           wait_duration=200, border=border.all(1, 'gray')),
                        #           width=500),
                        Container(content=Tooltip(message='Цена', content=
                        Text(value=str(self.res[i]['price'])+' ₽', size=24, color='#1d1e33', text_align='CENTER',
                             weight=FontWeight.BOLD), bgcolor='#667FBA',
                                                  text_style=ft.TextStyle(size=15, color=ft.colors.WHITE),
                                                  wait_duration=200, border=border.all(1, 'gray')),
                                  width=500),

                    ], alignment=MainAxisAlignment.SPACE_BETWEEN),
                    Container(width=15),
                    Container(
                    Column(controls=[
                    Container(alignment=alignment.top_center, content=Tooltip(message='Среднее количество товара в магазинах\nМаксимальное количество: '+str(sum(self.res[i]['count'])),
                                                                              content=Text('~'+str(sum(self.res[i]['count']) // len(self.res[i]['count'])), size=22,
                                                                                           color='black',
                                                                                           weight='bold'),
                                                                              bgcolor='#667FBA',
                                                                              text_style=ft.TextStyle(size=15,
                                                                                                      color=ft.colors.WHITE),
                                                                              wait_duration=200), padding=5),
                    self.product_add_bool,
                    Tooltip(message='Добавить товар!',content=Container(Icon(icons.PLUS_ONE, color='red', size=42)),
                                bgcolor='#667FBA', text_style=ft.TextStyle(size=15, color=ft.colors.WHITE),
                                wait_duration=200, border=border.all(1, 'gray')),
                        ], alignment=MainAxisAlignment.SPACE_BETWEEN), padding=padding.only(bottom=5)
                    )

                ]),
                # on_click=self.element_click, bgcolor='#667FBA', height=220, border_radius=10)
                on_click=self.element_click, bgcolor=colors.WHITE, height=220, border_radius=10)
            self.list_find_product.content.controls.append(r)
        self.page.update()


    def generate_product_list(self, e):
        self.res = find_products.search_products(e)
        if self.res != None:
            self.count_product_find.value = f'Найдено {len(self.res)} {self.right_padej(len(self.res))}!'
        if len(self.res) % 50 == 0:
                self.current_pages_find = int((len(self.res) / 50))
        else:
                self.current_pages_find = int((len(self.res) / 50))+1

        self.res = self.sort_res(self.res)
        self.more_list_find_product.content.controls.clear()
        if len(self.res) > 50:
            self.more_list_find_product.bgcolor = '#7366bd'
            self.more_list_find_product.border_radius = 10
            self.more_list_find_product.content.controls.append(TextButton(content=Text('', size=25)))
            self.more_list_find_product.content.controls.append(Text('Страница товаров 1', size=25))
            self.more_list_find_product.content.controls.append(TextButton(content=Text('2', size=25), on_click=self.click_page))

        keys = list(self.res.keys())[:50]
        # if len(res) > 70:
        #     stop_res = res[70]
        for i in keys:

            # if len(res) > 70:
            #     if res[i]['name'] == stop_res['name']:
            #         break
            if self.res[i]['name_shop'] == 'bristol':
                shop_name = Row(controls=[Image(src='..\\resources\\icons_shops\\bristol.jpg', width=25, height=25),
                                          Text('Бристоль', color='#1d1e33', size=20)])
            elif self.res[i]['name_shop'] == 'КБ':
                shop_name = Row(controls=[Image(src='..\\resources\\icons_shops\\kb.png', width=25, height=25),
                              Text('Красное и белое', color='#1d1e33', size=20)])
            else:
                shop_name = [
                    Row(controls=[Image(src='..\\resources\\icons_shops\\bristol.jpg', width=25, height=25),
                                  Text('Пятёрочка', color='#1d1e33', size=20)]),
                    Row(controls=[Image(src='..\\resources\\icons_shops\\kb.png', width=25, height=25),
                                  Text('Красное и белое', color='#1d1e33', size=20)])]
            self.product_add_bool = Container()
            for product in self.value_page.list_korzina:
                if product.name.content.content.value == self.res[i]['name']:
                    self.product_add_bool = Tooltip(message='Товар уже добавлен!',
                            content=Container(Icon(icons.CHECK_BOX, color='green', size=42)),
                            bgcolor='#2E4374', text_style=ft.TextStyle(size=15, color=ft.colors.WHITE),
                            wait_duration=200, border=border.all(1, 'gray'))
                    break

            r = Container(
                content=Row(controls=[
                    Container(Image(src=self.res[i]['pic_url'], width=210, height=200),
                              border_radius=ft.border_radius.all(10), width=200, height=190, bgcolor=colors.WHITE,
                              padding=padding.all(5)),
                    Container(width=1),
                    Column(controls=[
                        Container(height=self.page.window_height * 0.0139),
                        Container(content=Tooltip(message='Наличие товара в магазине', content=Row(controls=
                        [shop_name],
                            alignment=MainAxisAlignment.CENTER), bgcolor='#667FBA',
                                                  text_style=ft.TextStyle(size=15, color=ft.colors.WHITE),
                                                  wait_duration=200, border=border.all(1, 'gray')), width=500),

                        Container(content=
                                  Tooltip(message='Описание товара', content=
                                  Text(value=self.res[i]['name'],
                                       size=24, color='#1d1e33', max_lines=3, text_align='CENTER'),
                                          bgcolor='#667FBA', text_style=ft.TextStyle(size=15, color=ft.colors.WHITE),
                                          wait_duration=200, border=border.all(1, 'gray')),
                                  width=500),
                        Container(),
                        # Container(content=Tooltip(message='Информация о товаре', content=
                        # Text(value='Италия, 0.75 л., Абруццо, 13%', size=20, color='#53377a', text_align='CENTER'),
                        #                           bgcolor='#667FBA',
                        #                           text_style=ft.TextStyle(size=15, color=ft.colors.WHITE),
                        #                           wait_duration=200, border=border.all(1, 'gray')),
                        #           width=500),
                        Container(content=Tooltip(message='Цена', content=
                        Text(value=str(self.res[i]['price'])+' ₽', size=24, color='#1d1e33', text_align='CENTER',
                             weight=FontWeight.BOLD), bgcolor='#667FBA',
                                                  text_style=ft.TextStyle(size=15, color=ft.colors.WHITE),
                                                  wait_duration=200, border=border.all(1, 'gray')),
                                  width=500),

                    ], alignment=MainAxisAlignment.SPACE_BETWEEN),
                    Container(width=15),
                    Container(
                    Column(controls=[
                    Container(alignment=alignment.top_center, content=Tooltip(message='Среднее количество товара в магазинах\nМаксимальное количество: '+str(sum(self.res[i]['count'])),
                                                                              content=Text('~'+str(sum(self.res[i]['count']) // len(self.res[i]['count'])), size=22,
                                                                                           color='black',
                                                                                           weight='bold'),
                                                                              bgcolor='#667FBA',
                                                                              text_style=ft.TextStyle(size=15,
                                                                                                      color=ft.colors.WHITE),
                                                                              wait_duration=200), padding=5),
                    self.product_add_bool,
                    Tooltip(message='Добавить товар!',content=Container(Icon(icons.PLUS_ONE, color='red', size=42)),
                                bgcolor='#667FBA', text_style=ft.TextStyle(size=15, color=ft.colors.WHITE),
                                wait_duration=200, border=border.all(1, 'gray')),
                        ], alignment=MainAxisAlignment.SPACE_BETWEEN), padding=padding.only(bottom=5)
                    )

                ]),
                # on_click=self.element_click, bgcolor='#667FBA', height=220, border_radius=10)
                on_click=self.element_click, bgcolor=colors.WHITE, height=220, border_radius=10)
            self.list_find_product.content.controls.append(r)

    def dropdown_changed(self, e):
        self.sort_list = e.control.value
        self.list_find_product.bgcolor = '#2E4374'
        self.list_find_product.height = self.page.window_height * 0.440
        self.list_find_product.content.controls.clear()
        self.list_find_product.content.controls.append(Container(height=1))
        if self.find_label.value != '':
            self.generate_product_list(self.find_label.value)
        self.page.update()


    def finder_app(self):
        self.create_appbar()
        self.list_find_product = Container(content=Column(
            height=self.page.window_height * 0.440,
            scroll='ALWAYS',
            controls=[
            ]

        )
        )
        self.more_list_find_product = Container(content=Row(controls=[Text('', size=25)], alignment=MainAxisAlignment.SPACE_BETWEEN))
        self.count_product_find = Text(value='', size=22, weight=ft.FontWeight.BOLD)
        self.block_bottom_finder = Row(controls=[self.count_product_find,
                                                 # Row(controls=[Text('Сортировать по: ', size=22, weight=ft.FontWeight.BOLD), Dropdown(value='Названию',width=400, on_change=self.dropdown_changed, text_size= 22,
                                                 Row(controls=[Dropdown(value='Названию', label="Сортировать по:",
                                                                        # bgcolor='#7B67BB',
                                                                        bgcolor='#667FBA',
                                                                        focused_bgcolor='#667FBA',
                                                                        filled=True,
                                                                        label_style=TextStyle(size=self.page.window_height * 0.0225, color='white',
                                                                                              weight='bold'), width=400,
                                                                        text_style=TextStyle(size=self.page.window_height * 0.0185, color='white',
                                                                                              weight='bold'),
                                                                        on_change=self.dropdown_changed,
                                                                        border_color='gray', border_width=1.5,
                                                                        border_radius=10, options=[
                                                         ft.dropdown.Option("Названию"),
                                                         ft.dropdown.Option("Минимальной цене"),
                                                         ft.dropdown.Option("Максимальной цене"),
                                                         ft.dropdown.Option("Магазин Бристоль"),
                                                         ft.dropdown.Option("Магазин КБ")])])],
                                       alignment=MainAxisAlignment.SPACE_BETWEEN)
        self.find_label = TextField(
            prefix_icon=ft.icons.SEARCH,
            hint_text='Введите название продукта: ', hint_style=TextStyle(color='#6B6767'), text_size=self.page.window_height * 0.0225, height=self.page.window_height * 0.06,
            on_submit=self.find_product, border=border.all(2, '#2E4374'),
            # bgcolor='#ADC4CE', text_style=TextStyle(color='black'))
            bgcolor=colors.WHITE, text_style=TextStyle(color='black', weight='bold'))
        page_1 = Container(
            width=1000,
            height=self.page.window_height * 0.87,
            border_radius=35,
            bgcolor='#2E4374',
            alignment=alignment.center,
            padding=padding.only(left=80, top=self.page.window_height*0.037, right=80),

            content=Column(
                alignment=MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    Column( controls=[
                    Container(height=self.page.window_height*0.009),
                    Text('Добрый день, давайте выберем товары необходимые вам: ', size=self.page.window_height * 0.021, weight='bold'),
                    Container(height=self.page.window_height*0.009),
                    self.find_label,
                    self.block_bottom_finder,
                    self.more_list_find_product,
                    self.list_find_product,]
            ),
                    Row(
                        controls=[
                            TextButton(content=Row(controls=[
                                Text(value='Назад', size=self.page.window_height * 0.024),
                                Icon(icons.ARROW_LEFT, size=self.page.window_height * 0.1056)
                            ]), on_click=self.find_to_back),
                            TextButton(content=Row(controls=[
                                Icon(icons.ARROW_RIGHT, size=self.page.window_height * 0.1056),
                                Text(value='В корзину', size=self.page.window_height * 0.024)
                            ]), on_click=self.korzina_click),
                        ], alignment=MainAxisAlignment.SPACE_BETWEEN
                    )

                ]
            )
        )

        self.page.add(page_1)


class AppMain:

    def change_window(self, e):
        self.page.controls.pop()
        self.start_view = Container(
            width=1000,
            height=(self.page.window_height * 0.85),
            # height=(768*0.85),
            border_radius=35,
            bgcolor='#2E4374',
            padding=padding.only(left=80, top=40, right=80),
            content=Column(controls=[
                Container(height=self.page.window_height * 0.1815),
                Container(height=self.page.window_height * 0.1388),
                Container(content=self.TextHeaderWelcome, alignment=alignment.center),
                Container(height=self.page.window_height * 0.2472),
                Container(content=Row(controls=
                [
                    Container(width=100),
                    TextButton(content=Row(controls=[
                        Icon(icons.ARROW_RIGHT, size=self.page.window_height * 0.1056),
                        Text(value='Вперёд!', size=self.page.window_height * 0.024)

                    ]), on_click=self.to_next)
                ], alignment=MainAxisAlignment.SPACE_BETWEEN))

            ], alignment=alignment.center
            )
        )
        self.page.add(self.start_view)
        self.page.update()

    def __init__(self, page, value_page):
        self.page = page
        # self.page.on_resize = self.change_window
        self.value_page = value_page
        # self.page.horizontal_alignment = 'center'
        # self.page.vertical_alignment = 'center'
        self.TextHeaderWelcome = Text('Привет, пришли за выгодными покупками?', style="headlineLarge",
                                      text_align='center')
        self.create_appbar()
        self.start_view = Container(
            width=1000,
            height=(self.page.window_height * 0.87),
            border_radius=35,
            bgcolor='#2E4374',
            padding=padding.only(left=80, top=40, right=80),
            content=Column(controls=[
                Column(controls=[
                    Container(height=self.page.window_height * 0.1815),
                    Container(height=self.page.window_height * 0.1388),
                    Container(content=self.TextHeaderWelcome, alignment=alignment.center),
                    ]),
                Container(content=Row(controls=
                [
                    Container(width=100),
                    TextButton(content=Row(controls=[
                        Icon(icons.ARROW_RIGHT, size=self.page.window_height* 0.1056),
                        Text(value='Вперёд!', size=self.page.window_height*0.024)

                    ]), on_click=self.to_next)
                ], alignment=MainAxisAlignment.SPACE_BETWEEN))

            ], alignment=MainAxisAlignment.SPACE_BETWEEN
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
