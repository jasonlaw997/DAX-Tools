import requests
from get_metadata import *
from modify_bim import *
from queue import Queue
from concurrent.futures import ThreadPoolExecutor ,wait,ALL_COMPLETED
import time
import random
import urllib3.contrib.pyopenssl



def get_formatted_dax(session,name,exp,q,timeout):
        x = {'dax': name + "=" + exp, 'ListSeparator': ',', 'DecimalSeparator': '.', 'maxLineLength':'1'}
        user_agent_list = [
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95',
            'Safari/537.36 OPR/26.0.1656.60',
            'Opera/8.0 (Windows NT 5.1; U; en)',
            'Mozilla/5.0 (Windows NT 5.1; U; en; rv:1.8.1) Gecko/20061208 Firefox/2.0.0 Opera 9.50',
            'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0',
            'Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 '
            '(maverick) Firefox/3.6.10',
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
            'Chrome/39.0.2171.71 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 '
            '(KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
        ]
        UserAgent = random.choice(user_agent_list)
        header = {'User-Agent': UserAgent,'Connection': 'close'}
        url = 'https://daxtest02.azurewebsites.net/api/daxformatter/daxtokenformat/'

        req = session.post(url, data=x,timeout=timeout,headers=header, verify=False)
        dax_dict = req.json()

        d1 = dax_dict["formatted"]

        result = ""
        for i, v in enumerate(d1):
            if i > 0:
                result = result + '\r\n'
                for x in v:
                    result = result + x["string"]
                    # print(result)
        r1={name:result}
        q.put(r1)

        return r1


def thread_get_formatted_dax(measure_dict,q,max_workers):
    if len(measure_dict)>30:
        sl=10
        timeout=16
    else:
        sl=3
        timeout=10

    measure_dict_formatted={}
    urllib3.contrib.pyopenssl.inject_into_urllib3()
    requests.packages.urllib3.disable_warnings()
    requests.adapters.DEFAULT_RETRIES = 5
    session = requests.session()
    session.keep_alive = False
    threadPool = ThreadPoolExecutor(max_workers=max_workers)
    for name,exp in measure_dict.items():
        threadPool.submit(get_formatted_dax,session,name,exp,q,timeout)

    time.sleep(sl)
    threadPool.shutdown(wait=True)
    while not q.empty():
        measure_dict_formatted.update(q.get())
    return measure_dict_formatted



def bim_all_formatted_dax(path, q):
    measures_exp_dict = get_bim_measures(path)
    r1 = {k: measures_exp_dict[k] for i, k in enumerate(measures_exp_dict) if i < 200}
    result = thread_get_formatted_dax(r1, q, 20)
    # dax_request_retry_dict = {}
    # for x in r1:
    #     if x not in result:
    #         dax_request_retry_dict.update({x: r1[x]})
    # if dax_request_retry_dict:                           #第二次开始获取之前多线程不生效的dax格式化
    #     if len(dax_request_retry_dict) > 10:
    #         max_workers = 10
    #     else:
    #         max_workers = len(dax_request_retry_dict)
    #     r = thread_get_formatted_dax(dax_request_retry_dict, q, max_workers)
    #     result.update(r)

    modfiy_bim(result, path)

def db_all_formatted_dax(databaseid,localhost,q):
    PowerBIDatabase=tomserver(databaseid,localhost)
    all_dict=get_meta_data(databaseid,localhost)
    measures_exp_dict=all_dict["measures_exp_dict"]
    r1 = {k: measures_exp_dict[k] for i, k in enumerate(measures_exp_dict) if i < 200}
    result = thread_get_formatted_dax(r1, q, 20)
    # dax_request_retry_dict = {}
    # for x in r1:
    #     if x not in result:
    #         dax_request_retry_dict.update({x: r1[x]})
    # if dax_request_retry_dict:                          #第二次开始获取之前多线程不生效的dax格式化
    #     if len(dax_request_retry_dict) > 10:
    #         max_workers = 10
    #     else:
    #         max_workers = len(dax_request_retry_dict)
    #     r = thread_get_formatted_dax(dax_request_retry_dict, q, max_workers)
    #     result.update(r)

    measure_dict_formatted=result
    for table in PowerBIDatabase.Model.Tables:
        CurrentTable = PowerBIDatabase.Model.Tables.Find(table.Name)
        for measure in CurrentTable.Measures:
            for k,v in measure_dict_formatted.items():
                if measure.Name == k:
                    measure.Expression = v
    PowerBIDatabase.Model.SaveChanges()


def gui_format_dax(flag,databaseid,localhost,path,q):
    if flag=="bim":
        bim_all_formatted_dax(path,q)
    elif flag=="pbix":
        db_all_formatted_dax(databaseid,localhost,q)

if __name__ == '__main__':
    start_time=time.time()
    try:
        databaseid_value = sys.argv[2]
        localhost_value = sys.argv[1]
    except:
        # databaseid_value = ""
        # localhost_value = ""
        databaseid_value = "496190c8-b617-43d2-ba58-d842f22944e6"
        localhost_value = "localhost:63999"

    # r=get_meta_data(databaseid_value,localhost_value)
    q=Queue()
    path = "Model.bim"
    # bim_all_formatted_dax(path,q)
    # db_all_formatted_dax(databaseid_value,localhost_value)
    flag="pbix"
    gui_format_dax(flag,databaseid_value,localhost_value,path,q)
    end_time=time.time()
    x=end_time-start_time
    print("cost time:{:.0f} min {:.2f} s".format(x // 60, x % 60))
