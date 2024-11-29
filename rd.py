from kivymd.app import MDApp
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.textfield import MDTextField
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle
import random
import os

class BorderedButton(MDBoxLayout):
    def __init__(self, text, on_release, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 5
        self.button = MDRaisedButton(
            text=text,
            size_hint_y=None,
            height=50,

            text_color=(1, 1, 1, 1),  # Цвет текста по умолчанию (белый)
            elevation=0,
            on_release=on_release
            
        )
        self.add_widget(self.button)

        with self.canvas.before:
            Color(0, 0, 0, 0)
            self.rect = Rectangle(size=self.size, pos=self.pos)

        self.bind(size=self.update_rect, pos=self.update_rect)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

class ThemeGeneratorApp(MDApp):
    def build(self):
        self.theme_cls.theme_style_switch_animation = True
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Gray"

        self.themes1 = self.read_themes_from_file('block1.txt')
        self.themes2 = self.read_themes_from_file('block2.txt')
        self.themes3 = self.read_themes_from_file('block3.txt')

        layout = MDBoxLayout(orientation='vertical', padding=20, spacing=10)

        self.theme_count_input = MDTextField(
            hint_text='Введите количество тем',
            multiline=False,
            size_hint_y=None,
            height=40,
            background_color=(1, 1, 1, 1),  # Цвет фона поля ввода (белый)
            foreground_color=(0, 0, 0, 1)  # Цвет текста в поле ввода (черный)
        )

        btn_all = BorderedButton('Выдать темы из 3 блоков', self.generate_all_themes)
        btn_block1 = BorderedButton('Выдать темы из блока 1', self.generate_block1_themes)
        btn_block2 = BorderedButton('Выдать темы из блока 2', self.generate_block2_themes)
        btn_block3 = BorderedButton('Выдать темы из блока 3', self.generate_block3_themes)
        btn_exit = BorderedButton('Выход', self.stop)
        btn_switch_theme = BorderedButton('Сменить цветовую схему', self.switch_theme_style)

        self.label = MDLabel(text='', size_hint_y=None, height=200, theme_text_color="Primary")

        scroll_view = MDScrollView(size_hint=(1, None), size=(400, 200))
        scroll_view.add_widget(self.label)

        layout.add_widget(self.theme_count_input)
        layout.add_widget(btn_all)
        layout.add_widget(btn_block1)
        layout.add_widget(btn_block2)
        layout.add_widget(btn_block3)
        layout.add_widget(btn_switch_theme)
        layout.add_widget(btn_exit)
        layout.add_widget(scroll_view)

        return layout

    def on_button_press(self, button):
        if self.theme_cls.theme_style == "Dark":
            button.button.md_bg_color = (0, 0.5, 1, 1)
            button.button.text_color = (1, 1, 1, 1)
        else:
            button.button.md_bg_color = (0.8, 0.8, 0.8, 1)
            button.button.text_color = (0, 0, 0, 1)

    def on_button_release(self, button):
        Clock.schedule_once(lambda dt: self.reset_button_color(button), 0.5)

    def reset_button_color(self, button):
        if self.theme_cls.theme_style == "Dark":
            button.button.md_bg_color = (0.1, 0.8, 0.8, 1)
            button.button.text_color = (0, 0.55, 1, 0)
        else:
            button.button.md_bg_color = (0.8, 0.8, 0.8, 1)
            button.button.text_color = (0, 0, 0, 1)  # Цвет текста по умолчанию (черный)

    def read_themes_from_file(self, filename):
        if not os.path.exists(filename):
            return []
        with open(filename, 'r', encoding='utf-8') as file:
            return [line.strip() for line in file.readlines()]

    def get_random_themes(self, themes, count):
        return random.sample(themes, min(count, len(themes)))

    def save_themes_to_file(self, themes):
        with open('generated_themes.txt', 'w', encoding='utf-8') as file:
            for theme in themes:
                file.write(theme + '\n')
        self.label.text += "\nТемы сохранены в файл 'generated_themes.txt'."

    def generate_all_themes(self, instance):
        try:
            if not self.theme_count_input.text.strip():
                self.label.text = "Введите количество тем!"
                return
            total_count = int(self.theme_count_input.text)
            selected_themes = self.get_random_themes(self.themes1, total_count) + \
                              self.get_random_themes(self.themes2, total_count) + \
                              self.get_random_themes(self.themes3, total_count)
            self.label.text = "\n".join(selected_themes)
            self.save_themes_to_file(selected_themes)
        except ValueError:
            self.label.text = "Введите корректное число!"

    def generate_block1_themes(self, instance):
        self.generate_themes(self.themes1)

    def generate_block2_themes(self, instance):
        self.generate_themes(self.themes2)

    def generate_block3_themes(self, instance):
        self.generate_themes(self.themes3)

    def generate_themes(self, themes):
        try:
            if not self.theme_count_input.text.strip():
                self.label.text = "Введите количество тем!"
                return
            count = int(self.theme_count_input.text)
            selected_themes = self.get_random_themes(themes, count)
            self.label.text = "\n".join(selected_themes)
        except ValueError:
            self.label.text = "Введите корректное число!"

    def switch_theme_style(self, *args):
        if self.theme_cls.theme_style == "Dark":
            self.theme_cls.theme_style = "Light"
            self.theme_cls.primary_palette = "Gray"
            self.update_button_styles((0.5, 0.5, 0.5, 1), (0, 0, 0, 1), (1, 1, 1, 1))
        else:
            self.theme_cls.theme_style = "Dark"
            self.theme_cls.primary_palette = "Orange"
            self.update_button_styles((0, 0, 0, 0), (0, 1, 0, 1), (0, 1, 0, 1))
        self.label.text = "Текущая цветовая схема: {}".format("Темная" if self.theme_cls.theme_style == "Dark" else "Светлая")

    def update_button_styles(self, bg_color, line_color, text_color):
        for child in self.root.children:
            if isinstance(child, BorderedButton):
                child.button.md_bg_color = bg_color
                child.button.text_color = text_color

if __name__ == '__main__':
    ThemeGeneratorApp().run()
