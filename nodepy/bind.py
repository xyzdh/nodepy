#糟糕的实现，无法 对 深层的 变化 引起 的 整体 变化 作出相应。弃用
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
from re import finditer
from sys import _getframe
from codecs import open


class Bind():

    def __init__(self, value=None, cache=True):
        self.__dict__ = {'_Bind__value': value, '_Bind__old_value': None,
                         '_Bind__callback': [], '_Bind__condition': [], '_Bind__cache': {}}
        self.__setattr__ = self.__setitem__

    def __getattr__(self, name):
        print(46546,name,88888888)
        return eval("self.__dict__['_Bind__value']."+name)

    def __getitem__(self, name):
        return self.__dict__['_Bind__value'][name]
        # eval('self.__value['+name+']')

    def __setitem__(self, name, value):

        frame = _getframe()
        filename = frame.f_back.f_code.co_filename
        lineno = frame.f_back.f_lineno

        _local = frame.f_back.f_locals
        _global = frame.f_back.f_globals
        var = {}
    
        with open(filename, "r", encoding='UTF-8') as file:
            source = file.readlines()[lineno - 1]
            source = "".join(source.split())#去除空格,换行符,制表符

            if source[-1] != ':':  # 说明不是 if/while/for…… 之类
                nodes = parse(source)

                for node in walk(nodes):
                    if isinstance(node, Name):
                        _id = node.id

                        if var.get(_id):  # 不重复处理相同的name
                            continue

                        try:
                            var[_id] = _local[_id]
                        except:
                            var[_id] = _global[_id]


                        exclude = []#剔除 字符串
                        for w in ['"(.+?)"',"'(.+?)'"]:
                            exclude += [[m.start(),m.end()] for m in finditer(w, source)]

                        start,length =  0,len(_id)
                        inside = lambda x,y:y[0]<=x<=y[1]
                        while 1:
                            start = source.find(_id, start)
                            if start == -1:
                                break

                            t = start+length
                            if all([not inside(start, r) for r in exclude]):
                                    source = source[:t]+".__dict__['_Bind__value']"+source[t:]
                            start = t
        print(source,2222222)
        exec(source, {}, var)
        # self.__dict__['_Bind__value'][name] = value
        self.__value_change_call()

    # __setattr__ = __setitem__
    # # def __delitem__(self,key):
    # def __delitem__(self,key):
    #     print(key,6546546)
    def __value_change_call(self):
        value = self.__dict__['_Bind__value']
        old_value = self.__dict__['_Bind__old_value']
        if value == old_value:
            return

        v = {'value': value, 'old_value': old_value}
        for index, condition in enumerate(self.__dict__['_Bind__condition']):
            run_call = (condition is None or condition(**v))

            if run_call:
                self.__dict__['_Bind__callback'][index](**v)

        self.__dict__['_Bind__old_value'] = deepcopy(value)

    def __call__(self, *args):
        # print(self.__dict__)
        num = len(args)
        if num == 0:
            return self.__dict__['_Bind__value']  

        if num == 1:
            # print('22222222')
            self.__dict__['_Bind__value'] = args[0]
            self.__value_change_call()
            return

        if num > 0:
            raise TypeError(
                "takes 1 positional arguments but %d were given" % len(args))

    def __str__(self):
        return str(self.__dict__['_Bind__value'])

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
        if call not in self.__dict__['_Bind__callback']:  # 相同 的 call 只会 绑定一次
            self.__dict__['_Bind__callback'].append(call)
            self.__dict__['_Bind__condition'].append(ifs)

    def unbind(self, call):
        if not self.__check(call):
            raise TypeError("can not call")
        try:
            index = self.__dict__['_Bind__callback'].index(call)
            del self.__dict__['_Bind__callback'][index]
            del self.__dict__['_Bind__condition'][index]
        except ValueError:
            raise 'unbind fail.The call is not a Bind callback'

test = Bind()


def call(value, old_value):
    print(old_value, '---old')


def condition(value, old_value):
    if isinstance(value, int) and value > 6:
        print('will not trigger call,value == ', value)
        return False
    return True

test.bind(call,condition)

test([1, [2,3]])  # test() == 6 #None ---old
test[1] = 6
print(test) 

# class AA():
#     wow = 6
# test(AA)
# test.wow = 7
# print(test.wow)

# print(test[-1])
# test[1] = 3
# print(test)
# c = [12,3]
# # del test[1],c[1]
# # print(test,c)
# test[1] = [5,6]
# test[1][0] = 8
# print(test)
# if test == [1,3]:
#     print(56465)
# test(7) # test() == 7

# test([1,2,3])# test() == 123 #6 ---old
# test()[1] = 6 # test() == [1,6,3] #[1, 2, 3] ---old

# test.unbind(call) # unbind Callback & its Condition

# test('nothing will print')

# print(test())
# print(test._Bind__value)
