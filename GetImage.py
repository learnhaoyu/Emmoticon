import aiohttp
import asyncio
from bs4 import BeautifulSoup
from defaultconfig import headers
import re
import logging
import os
import aiofiles
from time import time
import json
from GetEmmoticonFromUser import GetUserinfo
baseurl="https://steamcommunity-a.akamaihd.net/economy/image/"
# def get(soup,emname):#re get download url
#     for s in soup.findAll('a'):
#         if s.get('class') == ['market_listing_row_link']:
#             for childs in s:
#                 for child in childs:
#                     try:
#                         if ((child['class']) == ['market_listing_item_img']):
#                             timg = child['src']
#                         if (child['class'] == ['market_listing_item_name_block']):
#                             if (child.span.string.lower() == emname.lower()):
#                                 emmoticonbool = child.find_all('span')[1].string
#                                 if (re.search(r'emoticon', emmoticonbool, re.I)):
#                                     return timg;
#                     except:
#                         logging.info("解析网页失败,没有找到表情")
async def download(session ,url,k):#download image
    print(k+'strat download')
    url=baseurl+url
    async with session.get(url,verify_ssl=False) as resp:
           with open('downloadimg/' +k.replace(":","")+'.png', 'wb') as fd:
                while True:
                    chunk = await resp.content.read(1024)
                    if not chunk:
                        break
                    fd.write(chunk)
    print(k + 'finish download')


#初始化
async def init(loop,target):

    task = []
    a=os.getcwd() + r'/downloadimg'
    if (os.path.exists(os.getcwd() + r'/downloadimg')):
        pass
    else:
        os.mkdir('downloadimg')
    async with aiohttp.ClientSession(loop=loop) as session:
        for k in target:
            task.append(asyncio.ensure_future(download(session,target[k],k)))
        # for furture in task:
        #     furture.add_done_callback(download)
        if(task.__len__()!=0):
            await asyncio.wait(task)


def file_name(file_dir,targets):
    if(os.path.exists(file_dir)):
        for root, dirs, files in os.walk(file_dir):
            for files_name in files:
                files_name=":"+files_name[0:len(files_name)-4]+':'
                if(files_name in targets):
                    del targets[files_name]
            # print(root) #当前目录路径
            # print(dirs) #当前路径下所有子目录
            # print(files) #当前路径下所有非目录子文件

#获取用户信息
start = time()

GetUserinfo()
#获取表情
f=open("items","r")
items=json.loads(f.read())
targets={}
for item in items:
    if (re.search("表情",item["type"])!=None):
        targets[item["name"]] = item["icon_url"]


file_name(os.getcwd() + r'/downloadimg',targets)

print(targets)

loop=asyncio.get_event_loop()
task = init(loop, targets)
try:
    loop.run_until_complete(task)
except SystemExit:
    print("caught SystemExit!")
    task.exception()
    raise
finally:
    loop.close()

loop.close()
stop = time()
print("下载耗费秒："+str(stop-start))