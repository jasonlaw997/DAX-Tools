# Background
Solve the problem that the **Tabular Editor** does not have smart input prompts

![](image/g1.gif)

# Installation

1. Download two files
**dax_tools.exe** and **DAX_Tools.pbitool.json**
2. Change the exe location of **DAX_Tools.pbitool.json**:   <font color=#FF0000>"C:\\Users\\XXX\\Desktop\\DAX_Tools\\dist\\dax_tools.exe"</font>
Replace it with the file location of **dax_tools.exe** on your computer, and then put **DAX_Tools.pbitool.json** in the json folder of PowerBI's external tools, which is generally displayed as follows:  
(This step is no different from adding other external tools)
```
C:\Program Files (x86)\Common Files\Microsoft Shared\Power BI Desktop\External Tools
```


Restart PowerBI and you will see
![](image\ig1.png)


# First Start
### pbix:
When opening **DAX Tools** in a external tool, the Login window will be displayed.  
**DAX Tools** will automatically enter the internal parameters of pbix [**databaseid**, **localhost**], then Click "Login".  
Open **Tabular Editor**, mouse click on **Tabular Editor**, press <font color=#FF0000>**F12**</font>, at this time **DAX Tools** will be bound to **Tabular Editor**.  
(Actually, pbix, Tabular Editor, and DAX Tools are bound to each other)

![](image/im2.png)


### Visual Studio:
Need **Dax Studio** to get [**databaseid**, **localhost**], fill in two input boxes, Login, click Tabular Editor with the mouse, press <font color=#FF0000>**F12** </font> lock Tabular Editor


## bim file
Click the button [select bim], select xxx.bim, click **Tabular Editor**, press <font color=#FF0000>**F12** </font>lock **Tabular Editor**



#  The main function
<font color=#FF0000>
Input prompt

Input prompt    
Input prompt    
 </font>

# Other functions
1. All measure format (fast)
2. Show irrelevant columns
3. Display metrics including <font color=#FF0000>[filter, var, if, switch]</font>  
4. Function prompt, and jump to the web page
5. Functions commonly used function shortcuts
6. Links between model design and various solutions displayed on the front end
7. pbix related websites

# Detailed tutorial

![](image\ig3.jpg)

Please remember the four input signs in the picture above (input start symbol)

## 1. "`" Backquote 
<font color=#FF0000>Input function</font>

## 2. "[" Brackets 
<font color=#FF0000>Input metric</font>

## 3. "'" Apostrophe
<font color=#FF0000>Input table</font>

## 4. "/" Slash
<font color=#FF0000>Enter a number</font>, such as a Measure [p12m], you need to enter [p/1/2/m]


## 5. Function prompt ctrl+c+c
Double-click any function in the Tabular Editor edit box, there will be function usage tips, and you can click the button to jump to [dax.dax.guide](https://dax.guide/) or [Microsoft DAX function document-Chinese] (https://docs.microsoft.com/zh-cn/dax/)

## 6. The most important space key
#### a. Space key to clear any input  
#### b. Switch the focus of the windows   application window from DAX Tools back to Tabular Editor  
#### c. Press the space key in the Tabular Editor edit box to synchronize the newly created Measure to DAX Tools, even if you have not saved the Tabular Editor changes to pbix

## 7. Other reminders

### Button [Input:Yes]
If you need to enter four input starting symbols **` ['/**
Or need to pause DAX Tools input
Need to click the button [Input:Yes]
![](image/im_input.png)

### Button [Top]
Window on top

### Press Enter
When creating a new measure on the Tabular Editor, after renaming, enter will trigger an action to synchronize the new measure to DAX Tools (one of the functions of the space bar)



# Question
##### 1. Why is there no change on pbix after the full file measurement is formatted?
**Answer:** Modify any measurement on pbix at will, for example, add a space, then enter, the temporary database created by pbix will be refreshed, and the previous formatting and modification actions will also be refreshed; you can also create a new one on pbix A metric or refresh any table (preferably a very small table)