import ast
# file = open("code.py", "r")  
# source = file.read()  
# visitor = ReWriteName()  
# root = ast.parse(source)  
# root = visitor.visit(root)  
# ast.fix_missing_locations(root)  
   
# code_object = compile(root, "<string>", "exec")  
# exec code_object
from codecs import open
file = open("temp", "r",encoding='UTF-8')  
source = file.read()  
# # visitor = ReWriteName()
# for index,value in enumerate(source):
#     if value == '"':
import re
source = "".join(source.split())#去除空格,换行符,制表符
print(source)
print(re.findall("'(.+?)'", source))
exclude = []
for w in ['"(.+?)"',"'(.+?)'"]:
    exclude += [[m.start(),m.end()] for m in re.finditer(w, source)]
print(exclude,46565)

_id = 'test'
length =  len(_id)
start = 0
inside = lambda x,y:y[0]<=x<=y[1]
while 1:
    start = source.find(_id, start)
    if start == -1:
        break

    if all([not inside(start, r) for r in exclude]):
            t = start+length
            source = source[:t]+".__dict__['_Bind__value']"+source[t:]
    start += len(_id)
print(source,2222222)
# source = "a = var['kkl']"
# exam = ast.parse(source)
# print(ast.dump(exam))  
# root = visitor.visit(root)  
# ast.fix_missing_locations(root)  
   
# code_object = compile(root, "<string>", "exec")  
# exec code_object
# a = 'sdsa'
# a = a.replace('s', 's()')
# print(a)
# a = [1,2,3]
# for _ in a:
#     print(_+4)
