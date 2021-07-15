import requests
import asyncio
import httpx


class WxNotify:
    def __init__(self, corpid, corpsecret, agentid):
        self.corpid = corpid
        self.corpsecret = corpsecret
        self.agentid = agentid
        self.access_token = self.__get_access_token(corpid, corpsecret)
        self.session = None

    def __get_access_token(self, corpid, corpsecret):
        url = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken'
        params = {
            'corpid': corpid,
            'corpsecret': corpsecret
        }
        resp = requests.get(url, params=params)
        resp.raise_for_status()
        resp_json = resp.json()
        if 'access_token' in resp_json.keys():
            return resp_json['access_token']
        else:
            raise Exception('Please check if corpid and corpsecret are correct \n' + resp.text)

    async def send(self, text):
        url = 'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=' + self.access_token
        payload = {
            "touser": "@all",
            "msgtype": "text",
            "agentid": self.agentid,
            "text": {
                "content": text
            },
            "safe": 0,
            "enable_id_trans": 0,
            "enable_duplicate_check": 0,
            "duplicate_check_interval": 1800
        }
        async with httpx.AsyncClient() as session:
            async with session.post(url, json=payload) as resp:
                data = await resp.read()
        return data


if __name__ == "__main__":
    CORPID = 'ww90015c31704f9f3c'
    CORPSECRET = 'CH2i2nQAVxue969khtHSn9lbDIltCqdhnDa3bQvSK-I'
    AgentId = '1000002'
    wn = WxNotify(corpid=CORPID, corpsecret=CORPSECRET, agentid=AgentId)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(wn.send("异步测试"))
