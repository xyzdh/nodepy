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
file = open("bind.py", "r",encoding='UTF-8')  
source = file.read()  
# visitor = ReWriteName()
exam = ast.parse(source)
print(ast.dump(exam))  
# root = visitor.visit(root)  
# ast.fix_missing_locations(root)  
   
# code_object = compile(root, "<string>", "exec")  
# exec code_object