import requests
import aiohttp
import asyncio
from bs4 import BeautifulSoup
from defaultconfig import headers
import re
import logging
import os
import aiofiles
from time import time

def get(soup,emname):#re get download url
    for s in soup.findAll('a'):
        if s.get('class') == ['market_listing_row_link']:
            for childs in s:
                for child in childs:
                    try:
                        if ((child['class']) == ['market_listing_item_img']):
                            timg = child['src']
                        if (child['class'] == ['market_listing_item_name_block']):
                            if (child.span.string.lower() == emname.lower()):
                                emmoticonbool = child.find_all('span')[1].string
                                if (re.search(r'emoticon', emmoticonbool, re.I)):
                                    return timg;
                    except:
                        logging.info("解析网页失败,没有找到表情")
async def downloads(session,url):#download image
    for key in url:
        print(key+'strat download')
        async with session.get(url[key],verify_ssl=False) as resp:
               with open('downloadimg/' +key.replace(":","")+'.png', 'wb') as fd:
                while True:
                    chunk = await resp.content.read(1024)
                    print("downloadingfrom"+url[key])
                    if not chunk:
                        break
                    fd.write(chunk)

class Getimage:
    def __init__(self,Emoticon,session):
        self.url={}
        if(type(Emoticon)==list):
            for s in Emoticon:
                self.url[s]=('http://steamcommunity.com/market/search?descriptions=1&q=%s'% s)
        else:
            self.url[Emoticon] = ('http://steamcommunity.com/market/search?descriptions=1&q=%s' % Emoticon)
        self.session=session
    async def geti(self):
        temp={}
        for k in self.url:
            async with self.session.get(self.url[k],proxy="http://127.0.0.1:1087",headers=headers,verify_ssl=False)as resp:
                soup=BeautifulSoup(await resp.text(),'lxml')
                self.imgurl=get(soup,k)
                print(self.imgurl)
                if(self.imgurl==None):
                    logging.warning("没有找到'%s'"%k)
                else:
                    temp[k]=self.imgurl
        if temp:
            #await asyncio.wait(asyncio.ensure_future(download(self.session,temp)))
            await downloads(self.session,temp)






async def init(loop,target):

    task = []
    a=os.getcwd() + r'/downloadimg'
    if (os.path.exists(os.getcwd() + r'/downloadimg')):
        pass
    else:
        os.mkdir('downloadimg')
    async with aiohttp.ClientSession(loop=loop) as session:
        for k in target:
            task.append(asyncio.ensure_future(Getimage(k,session).geti()))
        # for furture in task:
        #     furture.add_done_callback(download)
        if(task.__len__()!=0):
            await asyncio.wait(task)


def file_name(file_dir,target):
    if(os.path.exists(file_dir)):
        for root, dirs, files in os.walk(file_dir):
            for files_name in files:
                files_name=":"+files_name[0:len(files_name)-4]+':'
                if(files_name in target):
                    del target[files_name]
            # print(root) #当前目录路径
            # print(dirs) #当前路径下所有子目录
            # print(files) #当前路径下所有非目录子文件


target = {":16bitheart:":"", ":8bitheart:":""}
file_name(os.getcwd() + r'/downloadimg',target)

print(target)
start = time()
loop=asyncio.get_event_loop()
loop.run_until_complete(init(loop,target))
loop.close()
stop = time()
print(str(stop-start) + "秒")