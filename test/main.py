import init#每个测试例 都要 import init

#测试 打过motionevent_patch后，touch_pos 的 坐标系原点 是否 变为 左上角
from kivy.app import App
from kivy.uix.label import Label
from nodepy.layout import Layout
class testLabel(Label):
    def on_touch_down(self,touch):
        self.text = str(touch.pos)

class test(App):

    def ttt(self,instance,pos):
        print(self.rootNode.size,self.rootNode.pos,self.rootNode.size_hint,self.rootNode.pos_hint) 
    def build(self):
        self.rootNode = Layout()
        print(self.rootNode.size) 
        self.rootNode.bind(on_touch_down = self.ttt)
        return self.rootNode

if __name__ == "__main__":
    test().run()
