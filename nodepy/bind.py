'''var = Bind()
当 对象 的 值 改变时，作出 反应。
When the value of Object is changed,do something.
只对 list/dict/class 一层 作出反应.
不会 对 list的方法作出反应(eg:test.remove(2))
'''
'''
test = Bind()

def call(value,old_value):
    print(old_value,'---old')
def condition(value,old_value):
    if isinstance(value,int) and value > 6:
        print('will not trigger call,value == ',value)
        return False
    return True
#绑定 动作 及 条件
test.bind(call,condition)

#普通 赋值
test(6) # test() == 6 #None ---old
test(7) # test() == 7

test([1,2,3])# test() == 7 #7 ---old
# 给子项赋值，可以 检测 到 变动(仅限一层)
test[1] = 6 #test() == [1,6,3]
#打印 值
print(test) # == print(test()) # [1,6,3]
#将 值 传递给 其他对象.失去 检测变动 的 功能
t = test() # t == [1,6,3]
t[0] = 8
####################
class Temp():
    www = 'Hello'

test(Temp())
print(test.www) #Hello
test.www = 'World'#检测到 变动

#解绑。动作与条件 是 一起的
test.unbind(call) # unbind Callback & its Condition 

test('nothing will print')

# print(test)
'''

from types import FunctionType, MethodType
from ast import parse, walk, Name
from copy import deepcopy
from re import finditer
from sys import _getframe
from codecs import open


class Bind():

    def __init__(self, value=None, cache=True):
        self.__value = value
        self.__old_value = None
        self.__callback = []
        self.__condition = []

    def __setattr__(self,name,value):
        if not name.startswith('_Bind__'):
            exec("self._Bind__value."+name+'=value')
            self.__value_change_call()
            return
        self.__dict__[name] = value

    def __getattr__(self, name):

        return eval("self._Bind__value."+name)

    def __setitem__(self, name, value):
        self.__dict__['_Bind__value'][name] = value
        self.__value_change_call()
        
    def __getitem__(self, name):
        return self.__value[name]

    def __value_change_call(self):
        value = self.__value
        old_value = self.__old_value

        if value == old_value:
            return

        v = {'value': value, 'old_value': old_value}
        for index, condition in enumerate(self.__condition):
            run_call = (condition is None or condition(**v))

            if run_call:
                self.__callback[index](**v)

        self.__dict__['_Bind__old_value'] = deepcopy(value)

    def __call__(self, *args):
        num = len(args)
        if num == 0:
            return self.__value

        if num == 1:
            self.__dict__['_Bind__value'] = args[0]
            self.__value_change_call()
            return

        if num > 0:
            raise TypeError(
                "takes 1 positional arguments but %d were given" % len(args))

    def __str__(self):
        return str(self.__value)

    __repr__ = __str__

    def __check(self, obj):
        # 只 允许 '函数' 和 '方法'
        if type(obj) in [FunctionType, MethodType]:
            return True

    def bind(self, call, ifs=None):
        if not self.__check(call):
            raise TypeError("can not call")
        if ifs != None and not self.__check(ifs):
            raise TypeError("can not call")
        if call not in self.__callback:  # 相同 的 call 只会 绑定一次
            self.__callback.append(call)
            self.__condition.append(ifs)

    def unbind(self, call):
        if not self.__check(call):
            raise TypeError("can not call")
        try:
            index = self.__callback.index(call)
            del self.__callback[index]
            del self.__condition[index]
        except ValueError:
            raise 'unbind fail.The call is not a Bind callback'


test = Bind()

def call(value,old_value):
    print(old_value,'---old')
def condition(value,old_value):
    if isinstance(value,int) and value > 6:
        print('will not trigger call,value == ',value)
        return False
    return True
#绑定 动作 及 条件
test.bind(call,condition)

#普通 赋值
test(6) # test() == 6 #None ---old
test(7) # test() == 7

test([1,2,3])# test() == 7 #7 ---old
test.remove(2)
print(test)