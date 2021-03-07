a="度量值 3 = CALCULATE(SUM('Sheet13'[sales]),ALL(Sheet13))"
a="度量值 = var x=CALCULATE(var x1= SUM('Sheet13'[sales]) return x1,ALL(Sheet13),FILTER(CALCULATETABLE('Sheet13',ALL('Sheet13'[banner])),'Sheet13'[banner]='A')) return x"
count=0
d1={}
heap=[]
p_dict={}
for i,p in enumerate(a):
    # print(i,p)
    if p=='(':
        heap.append((i,p))
        print("压入：", heap,"层级：",count)
        count=count+1
    elif p==')':
        x_pop=heap.pop()
        count = count -1
        x = [x_pop, (i, p)]
        xx = [(x_pop[0], i-1)]
        print("一对x：",x,"层级：",count)
        print("一对xx：",xx,"层级：",count)
        if  count not in d1:
            d1.update({count:xx})
            print(99,{count:xx})
        elif count in d1:
            xxx=d1[count]+xx
            d1.update({count:xxx})
    elif p==',':
        print("逗号：",i,p,count)
        if not count in p_dict:
            p_dict.update({count:[i]})
        else:
            pp=p_dict[count]+[i]
            p_dict.update({count:pp})
print("逗号字典",p_dict)
print("括号字典",d1)

blank="    "
final_dict={}
for k,v in d1.items():
    for k1,v1 in p_dict.items():
        for i in v1:
            for vv in v:
                # print(777,i,vv)
                if i >=vv[0] and i<=vv[1] and (k+1)==k1 and (vv[1]-vv[0])>=50:
                    print(888,k,vv,i)
                    print(999,{vv[0]:(k+1)*blank+"n"},{vv[1]:k*blank+"n"},{i:(k+1)*blank+"n"})
                    final_dict.update({vv[0]:(k+1)*blank})
                    final_dict.update({vv[1]:k*blank})
                    final_dict.update({i:(k+1)*blank})

print("final dict:",final_dict)
str_list=list(a)
index_list=[k for k in final_dict]
index_list.sort()
print("index list:",index_list)

ff=0
for i,v in  enumerate(index_list):
    print(66666,i,v,final_dict[v])
    index=(v+1)+i
    str_list.insert(index,"\r\n"+final_dict[v])
    final_dax=''.join(str_list)
print(final_dax,index)
# print(final_dax[:40]+"XXX    \r\n    1"+final_dax[50:])
vr_list=[]
for i,s in enumerate(final_dax):
    var_x=final_dax[i:i+3]
    return_x=final_dax[i:i+6]
    if var_x.upper()=='VAR' or return_x.upper()=="RETURN":
        print(i,i+3,var_x)
        vr_list.append((i,i+3))
    elif  return_x.upper()=="RETURN":
        print(i,i+6,return_x)
        vr_list.append((i,i+6))

print(len(final_dax))
print(vr_list)
vr_list1=[x[0] for x in vr_list]
vr_list2=[x[1] for x in vr_list]
print(vr_list1)

str_list=list(final_dax)

vr_list1.sort()
print("index list2:",vr_list2)


for f,i in enumerate( vr_list2):
    print(f,i)
    index = i + f+1
    str_list.insert(index,"\r\n")
    final_dax1=''.join(str_list)
    print(final_dax1,index)
