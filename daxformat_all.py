import sys
import math
import datetime
import time, threading
import  requests
import clr
import logging
from pathlib import Path
from time import  sleep
from functools import wraps
from queue import Queue

global System, DataTable, TOM, ADOMD
from dearpygui import *
from multiprocessing import Process, Queue, Lock
import multiprocessing


logger = logging.getLogger(__name__)
logger.info("Loading .Net assemblies...")
clr.AddReference("System")
clr.AddReference("System.Data")
root = Path(r"C:\Windows\Microsoft.NET\assembly\GAC_MSIL")
amo_path = str(
            max((root / "Microsoft.AnalysisServices.Tabular").iterdir())
            / "Microsoft.AnalysisServices.Tabular.dll"
        )
adomd_path = str(
            max((root / "Microsoft.AnalysisServices.AdomdClient").iterdir())
            / "Microsoft.AnalysisServices.AdomdClient.dll"
        )
clr.AddReference(amo_path)
clr.AddReference(adomd_path)
import System
from System.Data import DataTable
import Microsoft.AnalysisServices.Tabular as TOM
import Microsoft.AnalysisServices.AdomdClient as ADOMD
from Microsoft.AnalysisServices.Tabular import Measure

global databaseid_value,localhost_value



def gui(databaseid_value,localhost_value):
    set_main_window_title('DAX Format')
    set_style_window_title_align(10, 10)
    set_main_window_size(530, 650)
    add_text("input databaseid and localhost")
    add_text("You can via Dax studio to  copy that")
    add_input_text("databaseid",default_value=databaseid_value)
    add_input_text("localhost",default_value=localhost_value)
    add_button("Start", callback="start_callback",width=80,height=40)
    add_text("msgmess:")
    start_dearpygui()
def start_callback(sender, data):
    global databaseid_value, localhost_value
    print(get_value("databaseid"))
    print(get_value("localhost"))
    databaseid_value=get_value("databaseid")
    localhost_value = get_value("localhost")
    rename_main()


def tomserver():

    conn = "Provider=MSOLAP;Data Source="+localhost_value+";Initial Catalog='';"
    # print(conn)
    TOMServer = TOM.Server()
    TOMServer.Connect(conn)

    for item in TOMServer.Databases:
        print("Compatibility Level: {0} \nDatabase: {1} \nCreated: {2}".
              format(item.Name,item.CompatibilityLevel,item.CreatedTimestamp))

    databaseid=databaseid_value
    PowerBIDatabase = TOMServer.Databases[databaseid]
    return PowerBIDatabase



def get_measures(PowerBIDatabase):
    measures_list = []
    for table in PowerBIDatabase.Model.Tables:
        CurrentTable = PowerBIDatabase.Model.Tables.Find(table.Name)
        for measure in CurrentTable.Measures:
            measures_list.append({"Name":measure.Name,"Expression": measure.Expression})
    return measures_list


def get_formatted_dax(Measure_list,q):
    if len(Measure_list)>0:
        for Measure in Measure_list:
            i=0
            while i<4:
                try:
                    x = {'Dax': Measure["Name"]+"="+Measure["Expression"], 'ListSeparator': ',', 'DecimalSeparator': '.', 'MaxLineLenght': 0}
                    url = 'https://daxtest02.azurewebsites.net/api/daxformatter/daxtokenformat/'
                    r = requests.post(url, data=x,timeout=15)
                    dax_dict = r.json()
                    d1 = dax_dict["formatted"]
                    if len(d1)==0:
                        print("DAX公式错误")
                        break
                    result = ""
                    for i, v in enumerate(d1):
                        if i > 0:
                            result = result + '\r\n'
                            for x in v:
                                result = result + x["string"]

                    q.put({"Name":Measure["Name"],"Expression":result})
                    break
                except Exception as e:
                    i=i+1
                    print("第{0}次超时/网络错误".format(i))



def formatted_all_measures(PowerBIDatabase,formatted_mesures):
    # refresh_dict = {"full": TOM.RefreshType.Full}
    # print(formatted_mesures)
    for table in PowerBIDatabase.Model.Tables:
        CurrentTable = PowerBIDatabase.Model.Tables.Find(table.Name)
        for measure in CurrentTable.Measures:
            for d in formatted_mesures:
                if measure.Name == d["Name"]:
                    # print(d["Name"],d["Expression"])
                    measure.Expression = d["Expression"]
    #     CurrentTable.RequestRefresh(refresh_dict["full"])
    # PowerBIDatabase.Model.RequestRefresh(refresh_dict["full"])
    PowerBIDatabase.Model.SaveChanges()
    print("All Dax has been formatted")


def multithreading_get_format_dax(measures_list,q):
    if len(measures_list)<20:
        thread_num=len(measures_list)
    else:
        thread_num = 20
    step = math.ceil(len(measures_list) / thread_num)
    thread_list = []
    for i in range(0,thread_num):
        t = threading.Thread(target=get_formatted_dax, args=(measures_list[i*step:(i+1)*step],q,))
        # print(i*step,(i+1)*step)
        thread_list.append(t)
    for i,t,in enumerate(thread_list):
        t.start()
    for i,t,in enumerate(thread_list):
        t.join()

def rename_main():
    PowerBIDatabase=tomserver()
    q = Queue()
    start_time = time.time()
    measure_list=get_measures(PowerBIDatabase)
    print("total measures:{}".format(len(measure_list)))
    multithreading_get_format_dax(measure_list, q)
    formatted_mesures = []
    while True:
        if not (q.empty()):
            formatted_mesures.append(q.get())
        else:
            break

    end_time = time.time()
    formatted_all_measures(PowerBIDatabase,formatted_mesures)
    time_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    msg="time:{0}   total measures:{1} ---- take {2} seconds".format(time_str,len(formatted_mesures),round(end_time - start_time,3))
    print(" {} measures has been formatted".format(len(formatted_mesures)))
    print("cost time：", end_time - start_time)
    # print(msg)
    add_text(msg)


if __name__ == '__main__':
    try:
        databaseid_value = sys.argv[2]
        localhost_value = sys.argv[1]
    except:
        databaseid_value = ""
        localhost_value = ""
    gui(databaseid_value,localhost_value)
