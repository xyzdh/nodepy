import init#每个测试例 都要 import init

#测试 打过motionevent_patch后，touch_pos 的 坐标系原点 是否 变为 左上角
from kivy.app import App
from kivy.uix.label import Label

class testLabel(Label):
    def on_touch_down(self,touch):
        self.text = str(touch.pos)

class test(App):

    def build(self):
        rootNode = testLabel(text = "Hello World")
        return rootNode

if __name__ == "__main__":
    test().run()
