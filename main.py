import asyncio
import re
from random import *
from urllib.error import HTTPError

import requests
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from urllib.request import urlopen, Request
from bs4 import *


TIKTOK_LINK_REG_EXP = r"((https?:\/\/)?((\w|\d)+\.)?tiktok\.(\w|\d)+\/(\w|\d)*)"
FOXES_DIR_LINK = "https://wohlsoft.ru/images/foxybot/foxes/"


def http_get(url: str):
    request = Request(url)
    try:
        with urlopen(request) as response:
            data = response.read()
            return {
                "data": data,
                "status": response.status,
                "url": response.url
            }
    except HTTPError as error:
        return {
            "status": error.code,
        }


def get_foxes():
    data = http_get(FOXES_DIR_LINK)["data"]
    parsed_html = BeautifulSoup(data)
    links = []
    for link in parsed_html.body.find_all('td', attrs={'class':'indexcolname'})[1:]:
        links.append(FOXES_DIR_LINK + link.a.get("href"))
    return links


bot = Bot(token='7852413770:AAGvS6GCvcbadVS6OsxvXIuwKGW98HjNZA8')
dp = Dispatcher()


@dp.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer('привет')


@dp.message(Command('foxpic'))
async def foxpic(message: types.Message):
    await bot.send_photo(chat_id=message.chat.id,
                         photo=choice(get_foxes()))


@dp.message(Command('1or2'))
async def fiffif(message: Message):
    fif = str(randint(1, 2))
    await message.answer(fif)


# @dp.message(Command(re.compile(TIKTOK_LINK_REG_EXP)))
@dp.message(Command("dl"))
async def tiktok_download(message: Message):
    api = f"https://tiktok-info.p.rapidapi.com/dl/"
    link = re.findall(TIKTOK_LINK_REG_EXP, message.text)[0]
    link = link[0].split("?")[0]
    params = { "link": link }
    headers = {
      'x-rapidapi-host': "tiktok-info.p.rapidapi.com",
      'x-rapidapi-key': "f5685dd303mshcd2f836809b2d10p1ee22fjsn00548f3e2e9f"
    }
    video_link = requests.get(api, params=params, headers=headers) #.json()['videoLinks']['download']
    print(video_link)
    try:
        print(video_link.json())
    except:
        pass
    # await bot.send_video(message.chat.id, video_link)


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Бот выключен')

