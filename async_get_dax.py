import  requests
from get_metadata import *
from get_bim_metadata import *
from queue import Queue
from concurrent.futures import ThreadPoolExecutor
import time
import os
import  urllib3.contrib.pyopenssl

import asyncio

import aiohttp

def get_formatted_dax(name,exp,q):
        # print(name,exp)
        # print(111111,name,exp)
        x = {'Dax': name + "=" + exp, 'ListSeparator': ',', 'DecimalSeparator': '.', 'MaxLineLenght': 0}
        urllib3.contrib.pyopenssl.inject_into_urllib3()
        requests.packages.urllib3.disable_warnings()
        requests.adapters.DEFAULT_RETRIES = 5
        header = {
             'Connection': 'close',
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:68.0) Gecko/20100101 Firefox/68.0"
        }

        url = 'https://daxtest02.azurewebsites.net/api/daxformatter/daxtokenformat/'
        session = requests.session()
        session.keep_alive = False
        r = session.post(url, data=x,timeout=100,headers=header, verify=False)

        dax_dict = r.json()
        # print(2222222,dax_dict)
        d1 = dax_dict["formatted"]
        result = ""
        for i, v in enumerate(d1):
            if i > 0:
                result = result + '\r\n'
                for x in v:
                    result = result + x["string"]
        q.put({name:result})



async def fetch(session, name,exp):
    x = {'Dax': name + "=" + exp, 'ListSeparator': ',', 'DecimalSeparator': '.', 'MaxLineLenght': 0}
    # print(x)
    url='https://daxtest02.azurewebsites.net/api/daxformatter/daxtokenformat/'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}
    try:
        async with session.post(url, data=x, headers=headers, verify_ssl=False) as resp:
            return await resp.json()
    except Exception:
        # print()
        print(f"{name}, error happened:",Exception)


async def fetch_all(measures_exp_dict):
    connector = aiohttp.TCPConnector(limit=60)
    async with aiohttp.ClientSession(connector=connector) as session:
        session.keep_alive = False
        datas = await asyncio.gather(*[fetch(session, name, exp) for name, exp in measures_exp_dict.items()], return_exceptions=True)
        # return_exceptions=True 可知从哪个url抛出的异常
        # for ind, data in enumerate(urls):
        #     id_, url = data
        #     if isinstance(datas[ind], Exception):
        #         print(f"{id_}, {url}: ERROR")
        print(datas)
        print(len(datas))
        return datas





if __name__ == '__main__':
    start_time = time.time()
    try:
        databaseid_value = sys.argv[2]
        localhost_value = sys.argv[1]
    except:
        # databaseid_value = ""
        # localhost_value = ""
        databaseid_value = "980b24b4-c2d8-4ce0-9da6-44aa4bae3f4e"
        localhost_value = "localhost:56211"

    # r=get_meta_data(databaseid_value,localhost_value)

    path = "Model_epos.bim"
    r = get_bim_data(path)
    measures_exp_dict=r["measures_exp_dict"]
    print("度量值数量:",len(measures_exp_dict))
    q=Queue()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(fetch_all(measures_exp_dict))
    loop.close()
    end_time = time.time()
    print('totally cost', end_time - start_time, str((end_time - start_time) / 60) + "min")
