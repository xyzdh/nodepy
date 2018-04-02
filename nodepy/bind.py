'''
condition条件函数,只支持 参数 _value,_old_value
for example:
    def first_condition(_value,_old_value):
        if _value > _old_value:
            return True
or example:
    def first_condition():
        if 2 > 1:
            return True                
'''

from types import FunctionType,MethodType
from copy import deepcopy
class A4():
    pass
class Bind():
    __old_value = None
    __callback = []
    __condition = []
    def __init__(self,value=None):
        self.__value = value

    def aa(self):
        pass
    def __value_change_call(self,value):
        if value == self.__old_value:
            return
        old_value = deepcopy(self.__old_value)
        self.__old_value = deepcopy(value)
        for index,condition in enumerate(self.__condition):
            try:
                run_call = (condition is None or condition(value,old_value))
            except:
                run_call = (condition is None or condition())

            if run_call:
                try:
                    self.__callback[index](value,old_value)
                except:
                    self.__callback[index]()
    def __call__(self, *args):
        if args ==():
            return self.__value
            
        if len(args)==1:
            self.__value=args[0]
            self.__value_change_call(self.__value)
            return
            
        raise TypeError("takes 1 positional arguments but %d were given"%len(args))
        
    def __check(self,obj):
        # 只 允许 '函数' 和 '方法'
        if type(obj) in [FunctionType,MethodType]:
            return True
    def bind(self,call,ifs=None):
        if not self.__check(call):
            raise TypeError("can not call")
        if ifs != None and not self.__check(ifs):
            raise TypeError("can not call")
        self.__callback.append(call)        
        self.__condition.append(ifs) 
        
# a = Bind(6)

# a(56)
# print(a())
# if callable(Bind):
#      print(5555)
# if A4:
#     print (A4())
# 在类实例使用()符号时，就会调用__call__方法
if __name__ == '__main__':
    class TEST():
        def __init__(self):
            self.var = Bind()
            self.var.bind(self.call_with_value)# use args,but only can be  _value, _old_value
            self.var.bind(self.call_no_value,self.condition)# use condition

        def call_with_value(self,_value,_old_value):
            print("--------\n","I'm a Method and use args-value\n",_value,"\n",_old_value)

        def call_no_value(self):
            print("--------\n","I'm a Method and no args-value")

        def condition(self,_value,_old_value):
            if _old_value != None:
                return True 

    # test = TEST()
    # test.var("will not call <self.call_no_value>")

    # test.var("will call <self.call_no_value>")

    # ##########
    test = Bind([666,2333])
    def callme(_value,_old_value):
        print('hi,hi',_value,_old_value)
    test.bind(callme)
    # # print (test())
    test()[0] = 'WWWWWW'#这种 赋值 检测不到，555
    print(test()[0],222222)

    # test(66)#只能 检测到 从 ()里 赋值
    # print(test(),333333)

    # if type(callme) == FunctionType:
    #     print(666)