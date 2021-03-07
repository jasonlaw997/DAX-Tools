import requests
from bs4 import BeautifulSoup
from bs4 import element
import time
from concurrent.futures import ThreadPoolExecutor
from queue import Queue
import random
import  urllib3.contrib.pyopenssl
import os
import json
from queue import Queue
import re
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

def get_cate_funs(url):
    UserAgent = random.choice(user_agent_list)
    header = {'User-Agent': UserAgent}
    response = requests.get(url,headers=header,timeout=200)
    soup = BeautifulSoup(response.text, "lxml")
    r=(soup.find_all('li',class_="parent-item"))[0]
    rr=r.find_all("ul",class_="expandable")[0]
    funs_dict = {}
    funs_cate_list = []
    rrr=rr.find_all("li",class_="parent-item")
    for  i ,x in  enumerate(rrr):
        if type(x)==element.Tag:
            rrrr=x.find_all("li")
            for ii,s in enumerate( rrrr ):
                # print(i,x.a.string,s.a.string,s.a.get("href"))
                funs_cate_list.append({s.a.string:s.a.get("href")})
            funs_dict.update({x.a.string:funs_cate_list})
            funs_cate_list=[]
    print(funs_dict)
    return funs_dict

def get_funs_detail(session,fun_name,url,q):
    UserAgent = random.choice(user_agent_list)
    header = {'User-Agent': UserAgent} #, 'Connection': 'close'}
    response = session.get(url,timeout=20,headers=header, verify=False)
    print(fun_name)
    soup = BeautifulSoup(response.text, "lxml")
    syntax=soup.find_all("div",class_="notation")[0].string.  replace(r'&lt;',"<").replace("&gt;",">")

    def str_insert(str_origin, pos, str_add):
        str_list = list(str_origin)  # 字符串转list
        str_list.insert(pos, str_add)  # 在指定位置插入字符串
        str_out = ''.join(str_list)  # 空字符连接
        # print(str_out)
        return str_out

    syn_text=syntax.replace(" ", "")
    # print(len(syn_text))
    if len(syn_text)>32:     #处理函数syntax的换行显示问题
        span_list=[]
        for aa in re.finditer('<', syn_text):
            span_list.append(aa.span()[0])
        iii = 0
        for ii in span_list:
            syn_text = str_insert(syn_text, ii + iii, "\n")
            iii = iii + 1
        syntax = "\n  " + syn_text[:-1] + "\n)"
    else:
        syntax = "\n  " + syn_text
    try:
        rv=soup.find_all("section",id="returns")[0]

        rv_div=rv.find_all("div")[0]
        rd_list=[]
        for string in rv_div.strings:
            rd_list.append(string)
        rv_p=rv.find_all("p")
        if rv_p[-1].string==None:
            rv_p_s=""
        else:
            rv_p_s=rv_p[-1].string
            str_len = int(len(rv_p_s) / 2)
            index=0
            for i in range(int(str_len) - 1):
                str_len=str_len+i
                if rv_p_s[str_len] == " ":
                    index=str_len
                    break
            rv_p_s_text=rv_p_s[:index]+"\n "+rv_p_s[index:]
        r=("Syntax:"+syntax+'\n \n'+"Return Values:"+'\n'+"("+rd_list[0]+")  "+rd_list[1]+"\n"+rv_p_s_text)
    except:
        r = ("Syntax:" + syntax )
    # print(syntax)
    q.put({fun_name:r})
    # return {fun_name:r}

def thread_get_funs_json(q):
    pwd_path = os.getcwd()
    funs_json_name = "funs_data.json"
    funs_json_path = pwd_path + "\\" + funs_json_name

    if os.path.exists(funs_json_path):
        with open(funs_json_path, 'rb') as f:
            funs_json_data = json.load(f,strict=False)
    else:
        q_thread=Queue()
        threadPool=ThreadPoolExecutor(max_workers=15)
        gui_folding_table_dict={}
        gui_funs_detail_dict={}
        gui_cate_funs_list=[]
        gui_all_funs_list=[]
        url='https://dax.guide/'
        r=get_cate_funs(url)
        urllib3.contrib.pyopenssl.inject_into_urllib3()
        requests.packages.urllib3.disable_warnings()
        requests.adapters.DEFAULT_RETRIES = 5
        session = requests.session()
        # session.keep_alive = False
        # print(r)
        for k,v in r.items():
            for i in v:
                # print(111,k,v)
                # time.sleep(5)
                for fun_name,fun_url in i.items():
                    # print(222,fun_name,fun_url)
                    # time.sleep(3)
                    gui_cate_funs_list.append(fun_name)
                    gui_all_funs_list.append({fun_name:fun_url})
                    threadPool.submit(get_funs_detail,session,fun_name,fun_url,q_thread)
            gui_folding_table_dict.update({k:gui_cate_funs_list})
            gui_cate_funs_list=[]

        time.sleep(10)
        threadPool.shutdown(wait=True)
        while not q_thread.empty():
            gui_funs_detail_dict.update(q_thread.get())
        # print(gui_funs_detail_dict)
        # print(gui_folding_table_dict)
        funs_json_data=[gui_funs_detail_dict,gui_folding_table_dict,gui_all_funs_list]
        with open(funs_json_path, 'w', encoding='utf-8') as f:
            json.dump(funs_json_data, f, ensure_ascii=False, indent=4)
    # print(funs_json_data)
    q.put(funs_json_data)
    print(funs_json_data)
    return funs_json_data


if __name__ =='__main__':

    ##复制print结果到funs_data_list.py
    q=Queue()
    start_time=time.time()
    thread_get_funs_json(q)
    end_time=time.time()
    x=end_time-start_time
    print("cost time:{:.0f} min {:.2f} s".format( x//60,x%60))