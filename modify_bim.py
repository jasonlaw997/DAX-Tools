# -*- coding: UTF-8 -*-
import json


def get_bim_measures(path):
    with open(path, 'r',encoding='utf-8') as f:
        data = json.load(f,strict=False)
    t=data["model"]["tables"]
    measures_exp_dict={}
    for i in t:
        for k,v in i.items():
            if k=="measures":
                for m in v:
                    try:
                        if isinstance(m["expression"], list):
                            measures_exp_dict.update({m["name"] : " ".join(m["expression"])})
                        else:
                            measures_exp_dict.update ({m["name"] : m["expression"]})
                    except:
                        None
    # print(measures_exp_dict)
    return measures_exp_dict

def modfiy_bim(measure_dict_formatted,path):
    with open(path, 'r',encoding='utf-8') as f:
        data = json.load(f,strict=False)
    t = data["model"]["tables"]
    for i in t:
        for k, v in i.items():
            if k == "measures":
                for m in v:
                    for name,exp in measure_dict_formatted.items():
                        if m["name"]==name:

                            m["expression"]=exp
    with open(path,'w',encoding='utf-8') as f:
        json.dump(data,f,ensure_ascii=False ,indent=4)

if __name__ == "__main__":
    path="Model.bim"
    # modfiy_bim()

    # with open('model33.bim','w',encoding='utf-8') as f:
    #     json.dump(r,f,ensure_ascii=False ,indent=4)
    # with open('model33.txt','w',encoding='utf-8') as f:
    #     json.dump(r,f,ensure_ascii=False, indent=4)

