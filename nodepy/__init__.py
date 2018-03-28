import sys
from os.path import dirname,abspath

#将 当前目录 添加 到 sys.path,便于 其他文件 相互 访问
sys.path.append(dirname(abspath(__file__)))

import window_patch

import widget_patch

import motionevent_patch
'''
以上保留
'''
import module.load



# kivy.core.window   ------------update_childsize