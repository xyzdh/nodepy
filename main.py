from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.button import Button
class NonePy(App):
    """NonePy start"""
    def build(self):
        return Button(text = "Hello World")

if __name__ == '__main__':
    NonePy().run()
