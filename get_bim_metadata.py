import json
import copy

def get_bim_data(path):
    with open(path, 'r',encoding='utf-8') as f:
        data = json.load(f,strict=False)
    t=data["model"]["tables"]
    table_list=[]
    column_dict={}
    table_column_list=[]
    column_list=[]
    measures_list=[]
    measures_exp_dict = {}
    for i in t:
        for k,v in i.items():
            if k=="measures":
                for m in v:
                    # print(m)
                    try:
                        measures_list.append("["+m["name"]+"]")
                    except:
                        None

                    try:

                        if isinstance(m["expression"], list):
                            measures_exp_dict.update({m["name"] : " ".join(m["expression"])})
                        else:
                            measures_exp_dict.update ({m["name"] : m["expression"]})
                    except:
                        None
            if k=="name":
                # table_list.append(v)
                table_list.append("'"+v+"'")
            if  k=="name" or k=="columns":
                if k == "name":
                    table_name=v
                    table_column_list.append("'"+v+"'")
                try:
                    for c in v:
                        # table_column_list.append(table_name+"["+c["name"]+"]")
                        table_column_list.append("'"+table_name+"'"+"["+c["name"]+"]")
                except:
                    None
            if  k=="name" or k=="columns":
                # if k == "name":
                #
                #     table_name=v
                #     table_column_list.append("'"+v+"'")
                try:
                    for c in v:
                        column_list.append("["+c["name"]+"]")

                    column_dict.update({"'"+table_name+"'":column_list})
                    column_dict=copy.deepcopy(column_dict)
                    column_list.clear()
                except:
                    None
    meta_dict={"table_list":table_list,
               "table_column_list":table_column_list,
               "column_dict":column_dict,
               "measures_list":measures_list,
               "measures_exp_dict":measures_exp_dict
               }
    # print(meta_dict)
    return meta_dict

if __name__ == "__main__":
    # path="Model_epos.bim"
    path = "Model.bim"
    r=get_bim_data(path)
    print(r)
    r1 = r["measures_exp_dict"]['度量值 3']
    print(r1)
    # print("度量值数量:", len(r1))
    # print("".join(r1))