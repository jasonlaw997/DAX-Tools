English | [中文](README_zh-CN.md)

DAX Tools
=======================================================

![](https://img.shields.io/badge/Dependencies-python-brightgreen)
![](https://img.shields.io/badge/Package-pywin32%2Cpythonnet%2Cdearpygui-blue)
![](https://img.shields.io/badge/Version-v1.0.0-orange)
# Background
Solve the problem that the **Tabular Editor** does not have smart input prompts

![](image/g1.gif)

# Installation

1. Download two files
**dax_tools.exe** and **DAX_Tools.pbitool.json**
2. Change the exe location of **DAX_Tools.pbitool.json**:   "C:\\Users\\XXX\\Desktop\\DAX_Tools\\dist\\dax_tools.exe"
Replace it with the file location of **dax_tools.exe** on your computer, and then put **DAX_Tools.pbitool.json** in the json folder of PowerBI's external tools, which is generally displayed as follows:  
(This step is no different from adding other external tools)
```
C:\Program Files (x86)\Common Files\Microsoft Shared\Power BI Desktop\External Tools
```
Restart PowerBI and you will see

![](https://github.com/jasonlaw997/DAX-Tools/blob/main/image/ig0.png)
---

# First Start
### pbix:
When opening **DAX Tools** in a external tool, the Login window will be displayed.  
**DAX Tools** will automatically enter the internal parameters of pbix [**databaseid**, **localhost**], then Click "Login".  
Open **Tabular Editor**, mouse click on **Tabular Editor**, press **F12**, at this time **DAX Tools** will be bound to **Tabular Editor**.  
(Actually, pbix, Tabular Editor, and DAX Tools are bound to each other)  

![](https://github.com/jasonlaw997/DAX-Tools/blob/main/image/im2.png)
---



### Visual Studio:
Need **Dax Studio** to get [**databaseid**, **localhost**], fill in two input boxes, Login, click Tabular Editor with the mouse, press **F12**  lock Tabular Editor


## bim file
Click the button [select bim], select xxx.bim, click **Tabular Editor**, press **F12** lock **Tabular Editor**



#  The main function

Input prompt  
Input prompt    
Input prompt      


# Other functions
1. All measure format (fast)
2. Show irrelevant columns
3. Display metrics including [filter, var, if, switch]  
4. Function prompt, and jump to the web page
5. Functions commonly used function shortcuts
6. Links between model design and various solutions displayed on the front end
7. pbix related websites

# Detailed tutorial

![](https://github.com/jasonlaw997/DAX-Tools/blob/main/image/ig3.jpg)
---
Please remember the four input signs in the picture above (input start symbol)

## 1. "`" Backquote 
Input function

## 2. "[" Brackets 
Input measure

## 3. "'" Apostrophe
Input table

## 4. "/" Slash
Enter a number, such as a Measure [p12m], you need to enter [p/1/2/m]


## 5. Function prompt ctrl+c+c
Double-click any function in the Tabular Editor edit box, there will be function usage tips, and you can click the button to jump to [dax.dax.guide](https://dax.guide/) or [Microsoft DAX function document-Chinese] (https://docs.microsoft.com/zh-cn/dax/)

## 6. The most important space key
#### a. Space key to clear any input  
#### b. Switch the focus of the windows   application window from DAX Tools back to Tabular Editor  
#### c. Press the space key in the Tabular Editor edit box to synchronize the newly created Measure to DAX Tools, even if you have not saved the Tabular Editor changes to pbix

## 7. Other reminders

### Button [Input:Yes]
If you need to enter four input starting symbols **` ['/**
Or need to pause DAX Tools input Need to click the button [Input:Yes]

![](image/im_input.png)

### Button [Top]
Window on top

### Press Enter
When creating a new measure on the Tabular Editor, after renaming, enter will trigger an action to synchronize the new measure to DAX Tools (one of the functions of the space bar)



# Question
##### 1. Why is there no change on pbix after the full file measurement is formatted?
**Answer:** Modify any measurement on pbix at will, for example, add a space, then enter, the temporary database created by pbix will be refreshed, and the previous formatting and modification actions will also be refreshed; you can also create a new one on pbix A metric or refresh any table (preferably a very small table)
  
# Contributors

![](https://github.com/jasonlaw997/DAX-Tools/blob/main/image/1.png)
![](https://github.com/jasonlaw997/DAX-Tools/blob/main/image/ba1.png)
![](https://github.com/jasonlaw997/DAX-Tools/blob/main/image/2.png)
![](https://github.com/jasonlaw997/DAX-Tools/blob/main/image/3.png)