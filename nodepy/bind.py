'''
当 对象 的 值 改变时，作出 反应。
del 只支持 一层。
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
test(6) # test() == 6 => None ---old
test(7) # == 7, but will not call

test([1,2,3]) # == [1,2,3] => 7 ---old

test[0] = [5,6] # == [[5, 6], 2, 3]  => [1, 2, 3] ---old
test[0][1] = 0 # == [[5, 0], 2, 3]  => [[5, 6], 2, 3] ---old
#只能 删除 一层,eg：del test[0]
# del test[0][1] # will raise erro
# #打印 值
print(test,'\n______') # == print(test()) => [1,6,3]

class Temp():
    www = 'Hello'

test(Temp())
test.www = 'World' # will call

print(test.www) # => Hello

# #解绑。动作与条件 是 一起的
test.unbind(call) # unbind Callback & its Condition 

test('nothing will print')

print(test)
'''
from types import FunctionType, MethodType
from ast import parse, walk, Name
from copy import deepcopy
from re import finditer
from sys import _getframe
from codecs import open

__all__ = ('Bind')


Cache = {}  # filename:{lineno:[source,namespace]}
CheckChange = []
Status = 0  # 0入口,'deepcopy'提前运行一遍 获取 值变动,>0实际运行

class Bind():

    def __init__(self, value=None):
        self.__value = value
        self.__deep_value = deepcopy(value)
        self.__old_value = deepcopy(value)
        self.__callback = []
        self.__condition = []

    def __setattr__(self, name, value):
        # 这种 只能 处理 一层，很直接
        if not name.startswith('_Bind__'):
            exec("self._Bind__value." + name + '=value')
            self.__dict__['_Bind__deep_value'] = deepcopy(self.__value)
            self.__value_change_call()
            return
        self.__dict__[name] = value

    def pre(self, frame):#提前运行一遍 获取 值变动
        global Status,Cache,CheckChange

        filename = frame.f_back.f_code.co_filename
        lineno = frame.f_back.f_lineno

        try:#查看 有无 缓存
            source, namespace = Cache[filename][lineno]
        except:
            if not Cache.get(filename):
                Cache[filename] = {}

            _local = frame.f_back.f_locals
            _global = frame.f_back.f_globals
            namespace = {}

            with open(filename, "r", encoding='UTF-8') as file:
                source = file.readlines()[lineno - 1]
                source = "".join(source.split())  # 去除空格,换行符,制表符

                if source[-1] != ':':  # 说明不是 if/while/for…… 之类
                    nodes = parse(source)

                    for node in walk(nodes):
                        if isinstance(node, Name):
                            _id = node.id

                            if namespace.get(_id):  # 不重复处理相同的name
                                continue
                            try:
                                namespace[_id] = _local[_id]
                            except:
                                try:
                                    namespace[_id] = _global[_id]
                                except:
                                    if _id == 'print':                            
                                        return
                                    raise Exception("keyword not support,except 'print'")
            Cache[filename] = source, namespace

        Status = 'prerun'#模拟运行状态，使用 deepcopy 
        exec(source, {}, namespace)
        Status = len(CheckChange)-1#辅助 恢复 为 0,减去的1 为 首项(特殊)
        for run in CheckChange: 
            run()
        CheckChange = []

    def __getattr__(self, name):
        global Status
        # 这种 才是 处理 普通取值 及 深层赋值的

        if Status is 0:# 0无状态
            self.pre(_getframe()) 
            return eval("self._Bind__value." + name)

        if Status=='prerun':
            CheckChange.append(self.__value_change_call)
            self.__dict__['_Bind__deep_value'] = deepcopy(self.__value)
            return eval("self._Bind__deep_value." + name)# 仅使用值

        #实际运行
        Status -= 1
        return eval("self._Bind__value." + name)
    
    def __setitem__(self, name, value):
        # 这种 只能 处理 一层，很直接
        self.__value[name] = value
        self.__dict__['_Bind__deep_value'] = deepcopy(self.__value)
        self.__value_change_call()

    def __getitem__(self, name):
        global Status
        if Status is 0:# 0无状态
            self.pre(_getframe()) 
            return self.__value[name]

        if Status=='prerun':
            CheckChange.append(self.__value_change_call)
            self.__dict__['_Bind__deep_value'] = deepcopy(self.__value)
            return self.__deep_value[name] # 仅使用值

        #实际运行
        Status -= 1
        return self.__value[name]
    
    def __delattr__(self,name):
        exec("del self._Bind__value." + name)
        self.__dict__['_Bind__deep_value'] = deepcopy(self.__value)
        self.__value_change_call()  

    def __delitem__(self,name):
        del self.__value[name]
        self.__dict__['_Bind__deep_value'] = deepcopy(self.__value)
        self.__value_change_call() 

    def __value_change_call(self):
        value = self.__deep_value
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
            self.__dict__['_Bind__deep_value'] = deepcopy(self.__value)
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



def call(value, old_value):
    print(old_value, '---old')

def condition(value, old_value):
    if isinstance(value, int) and value > 6:
        print('will not trigger call,value == ', value)
        return False
    return True

