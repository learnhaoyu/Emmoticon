import sys
import aiohttp
import asyncio
import re
import os
from time import time
import json
from GetUserImage.DefaultConfig import *
from GetUserImage.GetUserInfo.GetEmmoticonFromUser import GetDownLoadUserInfofuture

baseurl="https://steamcommunity-a.akamaihd.net/economy/image/"

async def download(session ,url,k):#download image
    print(k+'strat download')
    url=baseurl+url
    async with session.get(url) as resp:
           with open('..\\downloadimg\\' +k.replace(":","")+'.png', 'wb') as fd:
                while True:
                    chunk = await resp.content.read(1024)
                    if not chunk:
                        break
                    fd.write(chunk)
    print(k + 'finish download')



async def init(loop,target):

    task = []
    a=r'..\downloadimg'
    if (os.path.exists(r'..\downloadimg')):
        pass
    else:
        os.mkdir('..\downloadimg')
    async with aiohttp.ClientSession(loop=loop) as session:
        for k in target:
            task.append(asyncio.ensure_future(download(session,target[k],k)))
        # for furture in task:
        #     furture.add_done_callback(download)
        if(task.__len__()!=0):
            await asyncio.wait(task)


def Delrepetition(file_dir):
    f = open("items", "r")
    items = json.loads(f.read())
    targets = {}
    for item in items:
        if (re.search("表情", item["type"]) != None):
            targets[item["name"]] = item["icon_url"]
    if(os.path.exists(file_dir)):
        for root, dirs, files in os.walk(file_dir):
            for files_name in files:
                files_name=":"+files_name[0:len(files_name)-4]+':'
                if(files_name in targets):
                    del targets[files_name]

    return targets
            # print(root) #当前目录路径
            # print(dirs) #当前路径下所有子目录
            # print(files) #当前路径下所有非目录子文件

loop=asyncio.get_event_loop()
#Get user info
if(updateuserinfo):
    loop.run_until_complete(GetDownLoadUserInfofuture())
#Deleterepetition
targets=Delrepetition(r'..\downloadimg')
print(targets)

start = time()
try:
    loop.run_until_complete(asyncio.ensure_future(init(loop, targets)))
except SystemExit:
    print("caught SystemExit!")
    raise
finally:
    loop.close()


stop = time()
print(str(stop-start) + "秒")