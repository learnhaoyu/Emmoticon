import json
import re
f=open("items","r")
items=json.loads(f.read())
target=[]
for item in items:
    if (re.search("表情",item["type"])!=None):
        target.append(item["name"])
print(items)