'''var = Bind()
当 对象 的 值 改变时，作出 反应。
When the value of Object is changed,do something.'''

'''
在 同一行 的 多次 变化 只会 callback一次,因此 尽量 避免 一行 多次使用。
最好的写法是一行 只 处理一项。
eg:
    test = Bind()
    def call(value,old_value):
        print(old_value,'---old')
    def condition(value,old_value):
        if isinstance(value,int) and value > 6:
            print('will not trigger call,value == ',value)
            return False
        return True

    test.bind(call,condition)

    test(6) # test() == 6 #None ---old
    test(7) # test() == 7

    test([1,2,3])# test() == 123 #6 ---old
    test()[1] = 6 # test() == [1,6,3] #[1, 2, 3] ---old

    test.unbind(call) # unbind Callback & its Condition 

    test('nothing will print')

    print(test())
'''

from types import FunctionType, MethodType
from ast import parse, walk, Name
from copy import deepcopy
from sys import _getframe
from codecs import open


class Bind():
    __slots__ = {'__value', 'cache', '__old_value',
                 '__callback', '__condition', '__cache', '_temp'}

    def __init__(self, value=None, cache=True):
        self.__value = value
        self.cache = cache #设置 是否 缓存 调用行 的 相关内容
        self.__old_value = None
        self.__callback = []
        self.__condition = []
        self.__cache = {}
        self._temp = None

    def __value_change_call(self, value):
        if value == self.__old_value:
            return

        v = {'value': value, 'old_value': self.__old_value}
        for index, condition in enumerate(self.__condition):
            run_call = (condition is None or condition(**v))

            if run_call:
                self.__callback[index](**v)

        self.__old_value = deepcopy(value)

    def __call__(self, *args):
        num = len(args)
        if num == 1:
            self.__value = args[0]
            self.__value_change_call(self.__value)
            return
        elif num > 0:
            raise TypeError(
                "takes 1 positional arguments but %d were given" % len(args))

        frame = _getframe()
        filename = frame.f_back.f_code.co_filename
        lineno = frame.f_back.f_lineno
        self._temp = deepcopy(self.__value)

        try:
            if not self.cache:
                raise
            source, var = self.__cache[filename][lineno]
        except:
            if not self.__cache.get(filename):
                self.__cache[filename] = {}

            _local = frame.f_back.f_locals
            _global = frame.f_back.f_globals
            var = {}

            with open(filename, "r", encoding='UTF-8') as file:
                source = file.readlines()[lineno - 1]
                source = source.replace("\r\n", "").replace("\n", "")

                if source[-1] != ':':  # 说明不是 if/while/for…… 之类
                    source = source.replace(' ', "").replace("\t", "")
                    nodes = parse(source)
                    # 首先 找出 所有 ) 右括号 的 位置,用于 模糊定位 函数位置
                    r_p = []  # Right parenthesis
                    for index, value in enumerate(source):
                        if value == ')':
                            r_p.append(index)

                    for node in walk(nodes):
                        if isinstance(node, Name):
                            _id = node.id

                            if var.get(_id):  # 不重复处理相同的name
                                continue

                            try:
                                var[_id] = _local[_id]
                            except:
                                try:
                                    var[_id] = _global[_id]
                                except:  # __builtins__
                                    if _id == 'print':
                                        return self._temp

                            start, add_len = 0, 0
                            while 1:
                                start = source.find(_id, start)
                                if start == -1:
                                    break
                                for index, pos in enumerate(r_p[:]):
                                    if pos < start:
                                        continue
                                    end = pos - 1
                                    ext = source[start + len(_id):end]
                                    try:
                                        if isinstance(eval('var[_id]' + ext), Bind):
                                            if source[end] == '(':
                                                source = source[
                                                    :end] + "._Bind__value" + source[end + 2:]
                                                we = source[
                                                    :end] + "._Bind__value" + source[end + 2:]
                                                r_p.remove(pos)
                                                for i in range(index, len(r_p)):
                                                    r_p[i] += 13 - 2
                                    except:
                                        pass
                                start += len(_id)

            if self.cache:
                self.__cache[filename][lineno] = [source, var]

        exec(source, {}, var)

        self.__value_change_call(self.__value)

        return self._temp

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

