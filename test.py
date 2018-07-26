import asyncio
import aiohttp
async def download():#download image
    print("test"+'strat download')
    url=("https://steamcommunity-a.akamaihd.net/economy/image/-9a81dlWLwJ2UUGcVs_nsVtzdOEdtWwKGZZLQHTxH5rd9eDAjcFyv45SR"
          "YAFMIcKL_PArgVSL403ulRUWEndVKv7gZeFAA07dwcDteOmL1Ez0qScIDkQ6I-0wdGOkvKiN-rQlDgIuZEg3uuYooih3BqkpRSfqSIqdA")
    async with aiohttp.ClientSession() as session:
        async with session.get(url,verify_ssl=False) as resp:
               with open('downloadimg/' +"test".replace(":","")+'.png', 'wb') as fd:
                    while True:
                        chunk = await resp.content.read(1024)
                        if not chunk:
                            break
                        fd.write(chunk)
async def geti(self):
    if self.url != None:
        await asyncio.wait(asyncio.ensure_future(download(self.session, self.url, self.k)))

loop = asyncio.get_event_loop()
task = asyncio.ensure_future(download())

loop.run_until_complete(task)
loop.close()
# import sys
# from PyQt5.QtWidgets import QApplication, QWidget
# app = QApplication(sys.argv)
# w = QWidget()
# w.resize(250, 150)
# w.move(300, 300)
# w.setWindowTitle('Simple')
# w.show()
#
# sys.exit(app.exec_())