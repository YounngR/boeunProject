# -*- coding: utf-8 -*-
content = None
with open("db.json",'rb') as f:
    content = f.read()
print(content)    
with open("db.json",'wb') as f:
    f.write(content)
