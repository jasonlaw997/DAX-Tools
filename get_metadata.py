import sys
import clr   # from pythonnet
import logging
from pathlib import Path

global System, DataTable, TOM, ADOMD
import  json
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

# global databaseid_value,localhost_value


def tomserver(databaseid_value,localhost_value):
    conn = "Provider=MSOLAP;Data Source="+localhost_value+";Initial Catalog='';"
    # print(conn)
    TOMServer = TOM.Server()
    TOMServer.Connect(conn)
    # for item in TOMServer.Databases:
    #     print("Compatibility Level: {0} \nDatabase: {1} \nCreated: {2}".
    #           format(item.Name,item.CompatibilityLevel,item.CreatedTimestamp))
    PowerBIDatabase = TOMServer.Databases[databaseid_value]
    return PowerBIDatabase

def get_meta_data(databaseid_value,localhost_value):
    PowerBIDatabase=tomserver(databaseid_value, localhost_value)
    table_list=[]
    table_column_list=[]
    column_dict={}
    measures_list = []
    measures_list_format = []
    measures_exp_dict = {}
    for table in PowerBIDatabase.Model.Tables:
        column_list = []
        # table_list.append(table.Name)    #因为空格问题，表名必须包含单引号
        table_list.append("'"+table.Name+"'")
        table_column_list.append("'"+table.Name+"'")
        CurrentTable = PowerBIDatabase.Model.Tables.Find(table.Name)
        for column in CurrentTable.Columns:
            if "RowNumber-" not in column.Name:
                column_list.append('['+column.Name+']')
                # table_column_list.append(table.Name+'['+column.Name+']')
                table_column_list.append("'"+table.Name+"'"+'['+column.Name+']')
                column_dict.update({"'"+table.Name+"'":column_list})
        for measure in CurrentTable.Measures:
            measures_list.append('['+measure.Name+']')
            measures_list_format.append(measure.Name+"="+ measure.Expression)

            measures_exp_dict.update({measure.Name:measure.Expression})
    meta_dict={'table_list':table_list,
               'table_column_list':table_column_list,
               'column_dict':column_dict,
               'measures_list':measures_list,
               # "measures_list_format": measures_list_format,
               "measures_exp_dict":measures_exp_dict
               }
    # print(meta_dict)
    return meta_dict



if __name__ == '__main__':

    try:
        databaseid_value = sys.argv[2]
        localhost_value = sys.argv[1]
    except:
        # databaseid_value = ""
        # localhost_value = ""
        databaseid_value = "1b5a341d-a8be-4977-8cab-8e633d75480e"
        localhost_value = "localhost:51771"

    # pbidt=tomserver(databaseid_value,localhost_value)


    r=get_meta_data(databaseid_value,localhost_value)
    print(r)
    r1=r["measures_exp_dict"]
    print(len(r1))
