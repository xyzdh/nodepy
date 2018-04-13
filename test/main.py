import inspect
import sys
print(inspect.stack(3))#保证 3 可以获取 到 下一行,当前行在中间，然后 总共 获取 三行源码
print(11111)
print (sys._getframe(0).f_code.co_name)
print(4)
print(inspect.getframeinfo(inspect.currentframe()))
import linecache
# print(linecache.cache[filename])
t =  list(linecache.cache[filename])
t[2][-1] = 'print(23333333333)\n'
linecache.cache[filename] = t
print(linecache.cache[filename])
print(666)