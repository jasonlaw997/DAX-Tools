import requests
from bs4 import BeautifulSoup
from bs4 import element
import time
from concurrent.futures import ThreadPoolExecutor
from queue import Queue

def get_cate_funs(url):
    response = requests.get(url)
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
    # print(funs_dict)
    return funs_dict

def get_funs_detail(cate_fun,fun_name,url,q1):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "lxml")
    syntax=soup.find_all("div",class_="notation")[0].string.  replace(r'&lt;',"<").replace("&gt;",">")
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
        # print(5555555555,rv_p[-1].string)
        # print("Syntax:"+syntax+'\n'+"Return Values:"+'\n'+"("+rd_list[0]+")  "+rd_list[1]+"\n"+rv_p_s)
        r=("Syntax:"+syntax+'\n'+"Return Values:"+'\n'+"("+rd_list[0]+")  "+rd_list[1]+"\n"+rv_p_s)
    except:
        r = ("Syntax:" + syntax )
    # print(fun_name, url)
    q1.put({fun_name:r})
    # return {fun_name:r}

if __name__=='__main__':
    start_time=time.time()
    q=Queue()
    threadPool=ThreadPoolExecutor(max_workers=15,thread_name_prefix="get_funs_detail")
    gui_folding_table_dict={}
    gui_funs_detail_dict={}
    gui_cate_funs_list=[]
    url='https://dax.guide/'
    r=get_cate_funs(url)
    # print(r)
    for k,v in r.items():
        for i in v:
            # print(k,v,i)
            for k1,v1 in i.items():
                # print(k1,v1)
                gui_cate_funs_list.append(k1)
                # r=get_funs_detail(k1,v1)
                future=threadPool.submit(get_funs_detail,k,k1,v1,q)
                # gui_funs_detail_dict.update(r)
        gui_folding_table_dict.update({k:gui_cate_funs_list})

    threadPool.shutdown(wait=True)
    while not q.empty():
        gui_funs_detail_dict.update(q.get())
    print(gui_funs_detail_dict)
    print(gui_folding_table_dict)
    end_time=time.time()
    print(999,len(gui_funs_detail_dict))

    print('totally cost', end_time - start_time)