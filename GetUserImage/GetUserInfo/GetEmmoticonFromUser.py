import sys
import aiohttp
import asyncio
import json
import copy
import os
from GetUserImage.DefaultConfig import userid,headers,storehouseurl

header = copy.deepcopy(headers)
header["Referer"] = "https://steamcommunity.com/profiles/"+userid+"/inventory/"

async def fetch(session, url):
   async with session.get(url,proxy="http://127.0.0.1:1080",headers=headers) as response:
       return await response.text()

async def DownLoadUserInfo():
    global storehouseurl

    totalcount =- 1
    count = 0
    storehouseurl = storehouseurl
    item=[]
    async with aiohttp.ClientSession() as session:
        while count != totalcount:
            html = await fetch(session, storehouseurl)
            html = json.loads(html)
            item +=html["descriptions"]
            totalcount=html["total_inventory_count"]
            count += len(html["assets"])
            last_assetid=html["assets"][len(html["assets"])-1]["assetid"]
            if(count < totalcount):
                storehouseurl = storehouseurl+"&start_assetid="+last_assetid
    return item

def DownLoadUserInfocallback(future):
    items=future.result()
    f=open("items",'w')
    f.write(json.dumps(items))
def GetDownLoadUserInfofuture():
    DownLoadUserInfofuture = asyncio.ensure_future(DownLoadUserInfo())
    DownLoadUserInfofuture.add_done_callback(DownLoadUserInfocallback)
    return DownLoadUserInfofuture

