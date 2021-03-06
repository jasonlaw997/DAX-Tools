
[English](README.md) | 中文

DAX Tools
=======================================================

![](https://img.shields.io/badge/Dependencies-python-brightgreen)
![](https://img.shields.io/badge/Package-pywin32%2Cpythonnet%2Cdearpygui-blue)
![](https://img.shields.io/badge/Version-v1.0.0-orange)

# 背景
解决 **Tabular Editor** 没有智能输入提示的问题  

![](image/g1.gif)

# 安装

1.下载两个文件
**dax_tools.exe** 以及 **DAX_Tools.pbitool.json**  
2.将**DAX_Tools.pbitool.json**的的exe位置："C:\\Users\\XXX\\Desktop\\DAX_Tools\\dist\\dax_tools.exe"
替换为你电脑上**dax_tools.exe** 的文件位置，然后将**DAX_Tools.pbitool.json**放到PowerBI的第三方工具json文件夹，一般如下显示：  
（此步骤与添加其他第三方工具无差别）  
```
C:\Program Files (x86)\Common Files\Microsoft Shared\Power BI Desktop\External Tools
```

重启PowerBI你将看到  

![](https://github.com/jasonlaw997/DAX-Tools/blob/main/image/ig0.png)
---


# 初次使用
### pbix:
在第三方工具打开 **DAX ToolsDAX Tools** 上会显示Login窗口；  
**DAX Tools** 会自动输入pbix的内部参数 [**databaseid**，**localhost**] 点击"Login"；  
打开**Tabular Editor**，鼠标点击一下 **Tabular Editor**，按下**F12**，此时 **DAX Tools** 将绑定 **Tabular Editor**。  
（实际上pbix，Tabular Editor，DAX Tools三方相互绑定了）  

![](https://github.com/jasonlaw997/DAX-Tools/blob/main/image/im2.png)


### Visual Studio:
需要**Dax Studio**获取[**databaseid**，**localhost**] 填进去两个输入框，Login，鼠标点击Tabular Editor ，**F12**锁定Tabular Editor


## bim file
点击按钮 [select bim]，选择xxx.bim，鼠标点击**Tabular Editor** ，**F12**锁定**Tabular Editor**


#  主要功能

输入提示    
输入提示  
输入提示


# 其他功能
1.全文件度量格式化（快）  
2.显示无关列  
3.显示包含 [filter，var ，if，switch] 的度量  
4.函数提示，并跳转网页  
5.函数常用函数快捷键  
6.模型设计与前端显示的各种解决方案的链接  
7.pbix相关网站  

# 详细使用教程
![](https://github.com/jasonlaw997/DAX-Tools/blob/main/image/ig3.jpg)
---

请记住上图的四个输入标志（输入起手符号）

## 1. "`" 反单引号 (backquote)
输入函数

## 2. "[" 括号 (bracket)
输入度量

## 3. "'" 英文单引号 (Apostrophe)
输入表

## 4. "/" 斜杠 (Slash)
输入数字，例如一个Measure [p12m]，需要输入[p/1/2/m]


## 5. 函数提示 ctrl+c+c
双击 Tabular Editor 编辑框的任意函数，将会有函数用法提示，以及可以点击按钮跳转到 [dax.dax.guide](https://dax.guide/) 或者是[微软DAX函数文档-中文](https://docs.microsoft.com/zh-cn/dax/)

## 6. 最重要的空格键(space)
#### a. 空格键清空任何输入 
#### b. 将windows的应用窗口焦点从 DAX Tools 切换回 Tabular Editor  
#### c. 在 Tabular Editor 编辑框按下空格键，将新建的Measure同步到 DAX Tools，即使你未将 Tabular Editor 的修改保存到 pbix  

## 7. 其他提醒

### 按钮 [Input:Yes]
如果需要输入四个输入起手符号  **` [ ' /**  
或者需要暂停DAX Tools输入  
需要点击按钮 [Input:Yes]  
![](image/im_input.png)

### 按钮[Top]
窗口置顶

### 按键Enter
在Tabular Editor上新建Measure时，重命名后，enter将会触发动作，将新建Measure同步到DAX Tools (space空格键的功能之一)



# 其他问题
##### 1.为什么全文件度量格式化后，pbix上没有任何变化？  
**答：** 在pbix上的任意度量随意修改一下，例如加一个空格，然后enter，pbix创建的临时数据库将会被刷新，前面格式化修改的动作也将刷新；亦可在pbix上新建一个度量或者刷新任意表（最好是很小的表） 

# Contributors

![](https://github.com/jasonlaw997/DAX-Tools/blob/main/image/1.png)
![](https://github.com/jasonlaw997/DAX-Tools/blob/main/image/ba1.png)
![](https://github.com/jasonlaw997/DAX-Tools/blob/main/image/2.png)
![](https://github.com/jasonlaw997/DAX-Tools/blob/main/image/3.png)