import sys
from os.path import dirname,abspath

#将 当前目录 添加 到 sys.path,便于 其他文件 相互 访问
sys.path.append(dirname(abspath(__file__)))

from kivy.core.window import WindowBase


def update_childsize(self, childs=None):
    w, h = self.size
    if childs is None:
        childs = self.children
    for w in childs:
        shw, shh = w.size_hint
        w.size = shw * w, shh * h



        x_hint,y_hint = w.pos_hint
        w.x = x_hint * w
        w.y = (1-shh-y_hint) * h




WindowBase.update_childsize = update_childsize

import widget_patch

import motionevent_patch
'''
以上保留
'''
import module.load



# kivy.core.window   ------------update_childsize