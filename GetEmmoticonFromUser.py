from defaultconfig import userid,headers,storehouseurl
import aiohttp
import asyncio
from bs4 import BeautifulSoup
import re
import logging
import os
import aiofiles
from time import time
import json
import copy
header = copy.deepcopy(headers)
header["Referer"] = "https://steamcommunity.com/profiles/"+userid+"/inventory/"

async def fetch(session, url):
   async with session.get(url,proxy="http://127.0.0.1:1087",headers=headers,verify_ssl=False) as response:
       return await response.text()

async def main():
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

def callback(future):
    items=future.result()
    f=open("items",'w')
    f.write(json.dumps(items))



loop = asyncio.get_event_loop()

task = asyncio.ensure_future(main())
task.add_done_callback(callback)
loop.run_until_complete(task)
loop.close()
