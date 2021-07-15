import asyncio
from random import random
import httpx

CORPID = 'ww90015c31704f9f3c'
CORPSECRET = 'CH2i2nQAVxue969khtHSn9lbDIltCqdhnDa3bQvSK-I'
AgentId = '1000002'
HOST = 'j05.space'
proxies={"all://":"http://127.0.0.1:8888"}

headers = {
    "Host": HOST,
    "Connection": "keep-alive",
    "Accept": "application/json, text/plain, */*",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36",
    "Content-Type": "application/json;charset=UTF-8",
    "Origin": "https://{}".format(HOST),
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Dest": "empty",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
}


async def login(client):
    data = {"email": "skywardcn", "passwd": "831113/*-"}
    url = "https://{}/signin?c={}".format(HOST, random())
    resp = await client.post(url=url, json=data)
    messages = resp.json()
    messages = messages.get("msg")
    print( messages)


async def checkin(client: httpx.AsyncClient):
    url = "https://{}/user/checkin?c={}".format(HOST, random())
    resp = await client.post(url)
    messages = resp.json()
    messages = messages.get("msg")
    return messages


async def create_tasks():
    async with httpx.AsyncClient(
        headers=headers, 
        verify=False,
        # proxies=proxies
        ) as client:
        await login(client)
        return await checkin(client)


def app():
    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(create_tasks())
    print(result)


def main_handler(event, context):
    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(create_tasks())
    return result


if __name__ == '__main__':
    app()
