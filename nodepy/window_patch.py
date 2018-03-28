from kivy.core.window import WindowBase


def update_childsize(self, childs=None):
    width, height = self.size
    if childs is None:
        childs = self.children
    for w in childs:
        # size
        shw, shh = w.size_hint
        w.size = shw * width, shh * height
        # pos
        x_hint,y_hint = w.pos_hint
        w.x = x_hint * width
        # print (1-shh-y_hint)
        w.y = y_hint * height #在 控件 添加 到 layout中 时 (1-shh-y_hint) 或 y_hint 效果无区别
        print (w.pos,888)




WindowBase.update_childsize = update_childsize
