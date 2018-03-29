import init#保留HEAD,必须导入


'''
目前 仅 motion pos 及 控件显示效果 以 左上角 为坐标原点。
控件 实际 pos 还是 左下角 为 坐标原点 因此 导致 motion pos 不能 和 控件 相匹配
next
    需要 保证 匹配
'''



from nodepy.layout import Layout
from kivy.app import App
from kivy.uix.button import Button
from kivy.graphics import Color, Rectangle
from kivy.core.window import Window
class test(App):

    def move(self,instance,pos):
        # self.button.pos_hint_y += 0.01
        # print (self.smallLayout.pos,self.smallLayout.size,self.smallLayout.right,self.smallLayout.top)
        print (Window.height,type(Window.size))
        pass

    def build(self):
        self.rootNode = Layout()
        self.smallLayout = Layout(size_hint = [0.2,0.2],pos_hint = [0.1,0.1])
        with self.smallLayout.canvas.before:
            Color(0, 1, 0, 1)
            self.rect = Rectangle(size=self.smallLayout.size,pos=self.smallLayout.pos)

        self.button = Button(size_hint = [0.2,0.2],pos_hint = [0.1,0.1])
        self.smallLayout.add_widget(self.button)
        self.smallLayout.bind(on_touch_down = self.move)
        self.rootNode.add_widget(self.smallLayout)


        def update_rect(instance, value):
            self.rect.pos = instance.pos
            self.rect.size = instance.size
        # listen to size and position changes
        self.smallLayout.bind(pos=update_rect, size=update_rect)
        return self.rootNode

if __name__ == "__main__":
    test().run()
