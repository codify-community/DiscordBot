from discordbot import main as dc_main
from tgbot import main as tg_main
from threading import Thread

import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)

if __name__ == '__main__':
    tg = Thread(target=tg_main)
    tg.start()
    dc_main()
    del tg
    

