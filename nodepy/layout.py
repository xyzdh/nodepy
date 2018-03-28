#-*- coding: utf-8 -*-
'''
基本 布局 类（相对布局）.nodepy的 特点 就是 “相对pos，相对size”。
相对布局 的 好处 在于 自适应 窗口(window)尺寸。
坐标系 使用 右手坐标系，坐标原点(0,0) 为 左上角
对于 位置(pos) 及 尺寸(size) 均使用 相对值(百分比)
pos_hint = [x,y] 及 size_hint = [w,h] #值 范围 为(0.0,1.0)
eg:
    rootNode = Layout()
    rootNode.add_widget(Button(pos_hint = [0.1,0.2],size_hint = [0.2,0.3]))

'''




__all__ = ('Layout', )

from kivy.clock import Clock
from kivy.uix.widget import Widget

class Layout(Widget):

    _trigger_layout = None

    def __init__(self, **kwargs):
        if self._trigger_layout is None:
            self._trigger_layout = Clock.create_trigger(self.do_layout, -1)
        fbind = self.fbind
        update = self._trigger_layout
        fbind('children', update)
        fbind('pos', update)
        fbind('pos_hint', update)
        fbind('size_hint', update)
        fbind('size', update)
        super(Layout, self).__init__(**kwargs)

    def do_layout(self, *largs, **kwargs):
        # optimize layout by preventing looking at the same attribute in a loop
        w, h = self.size
        x, y = self.pos

        for c in self.children:
            #size
            shw, shh = c.size_hint
            c.size = shw * w, shh * h

            x_hint,y_hint = c.pos_hint
            c.x = x + x_hint * w
            c.y = y + (1-shh-y_hint) * h# 打了 window_patch 后，貌似 不需要 1- 了,减不减 都一样？？？(1-shh-y_hint)
        # print (c.pos,'SSS')


    def add_widget(self, widget, index=0):
        fbind = widget.fbind
        fbind('pos_hint', self._trigger_layout)
        fbind('size_hint', self._trigger_layout)
        return super(Layout, self).add_widget(widget, index)

    def remove_widget(self, widget):
        funbind = widget.funbind
        fbind('pos_hint', self._trigger_layout)
        fbind('size_hint', self._trigger_layout)
        return super(Layout, self).remove_widget(widget)