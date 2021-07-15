import asyncio
from random import random
import logging
from logging import handlers
import platform
import httpx

logger = logging.getLogger("ASP")
fh = handlers.RotatingFileHandler("./history.log", encoding="utf-8", maxBytes=1024)
console = logging.StreamHandler()
output_fmt = logging.Formatter("[%(levelname)s %(asctime)s]：%(message)s")
logger.level = logging.INFO
fh.setFormatter(output_fmt)
console.setFormatter(output_fmt)
logger.addHandler(fh)
logger.addHandler(console)

CORPID = 'ww90015c31704f9f3c'
CORPSECRET = 'CH2i2nQAVxue969khtHSn9lbDIltCqdhnDa3bQvSK-I'
AgentId = '1000002'
HOST = 'oo.ax'

headers = {
    "Host": HOST,
    "Connection": "keep-alive",
    "Accept": "application/json, text/plain, */*",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36",
    "Content-Type": "application/json;charset=UTF-8",
    "Origin": F"https://{HOST}",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Dest": "empty",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
}


async def login(client: httpx.AsyncClient):
    data = {"email": "skywardcn", "passwd": "831113/*-"}
    url = f"https://{HOST}/signin?c={random()}"
    logger.info(url)
    resp = await client.post(url=url, json=data)
    messages = resp.json()
    messages = messages.get("msg")
    logger.info(messages)


async def checkin(client: httpx.AsyncClient):
    url = f"https://{HOST}/user/checkin?c={random()}"
    resp = await client.post(url)
    messages = resp.json()
    messages = messages.get("msg")
    return messages


async def create_tasks():
    proxies = {
        "all://": "http://127.0.0.1:8888"
    }
    async with httpx.AsyncClient(headers=headers, proxies=proxies, verify=False) as client:
        await login(client)
        return await checkin(client)


def app():
    logger.info("任务启动")
    asyncio.run(create_tasks())


if __name__ == '__main__':
    app()
