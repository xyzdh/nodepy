import init#每个测试例 都要 import init

# import moudle2.load
from nodepy.will import WillbeCover,WillbeCover2
def run(self):
    print("I'm a pathch")

def run2(self,**kwargs):
    print("I'm a pathch too~~~~~~~~")

##测试 用 新方法 覆盖 类 的 原始方法
WillbeCover.run = run

WillbeCover2.run2 = run2

print(WillbeCover2.myattr)

##把 类 的 属性 删掉
delattr(WillbeCover2, 'myattr')

from nodepy import test2
