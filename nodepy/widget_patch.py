from kivy.properties import NumericProperty, ReferenceListProperty

from kivy.uix.widget import Widget

Widget.pos_hint_x = NumericProperty(0, allownone=True)

Widget.pos_hint_y = NumericProperty(0, allownone=True)

Widget.pos_hint = ReferenceListProperty(Widget.pos_hint_x, Widget.pos_hint_y)

'''
目前 montionevent 产生 的 pos 已 使用 右手坐标系(left-top)
然而 内部 逻辑 的 坐标系 仍是 左手坐标系 (left-bottom)，
因此，
    计算 碰撞 点时 需要 将 点坐标 转到 左手坐标系(left-bottom)
在 外部 使用 时 还是 将 坐标系 视为 右手坐标系
'''
from kivy.core.window import Window
def collide_point(self, x, y):
    return self.x <= x <= self.right and self.y <= Window.height-y <= self.top

Widget.collide_point = collide_point