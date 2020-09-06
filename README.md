# BinTerminaTranslator

## 介绍

该项目设计为内建内建在终端内的快速翻译工具
语言支持建立在必应翻译接口上

---

### 下载

[各版本下载[gitee]][1]

---

### 安装教程

#### ![Gi](/media/SVG/windows.svg "Windwos") <font color='blue'>Windwos 安装配置</font>

###### 脚本安装

解压压缩包到独立文件夹内，执行内部的install.ps1脚本即可

###### 源码安装 !!!**源码运行仅支持Python3.6或更高版本**!!!

安装时你可以选定是否需要打包为 .exe 程序。
首先确定运行环境,开启任意终端,切换到源码目录。执行该命令安装所需支持包

    python -m pip install -r .\packges

打包执行文件。如不需要打包为 .exe 即可[点击此处]跳转至下一节

    pyinstaller.exe -D .\bin.py

复制配置文件

    Copy-Item .\ini\* .\dist\bin\ini\

复制文件至用户目录下,依次执行以下命令

    1. $prg = $HOME + '\bin_terminal_translator'
    2. $loc = (Get-Location).Path
    3. Copy-Item $loc $prg -Recurse

最后将目录添加至用户环境变量

    [System.Environment]::SetEnvironmentVariable("path", $env:Path + ';' + $prg + '\', "User")

###### 至此 Windows 下的源码安装到此结束

---

#### ![linux](/media/SVG/linux.svg "Linux") <font color='Yellow'>Linux安装配置</font>

暂时么得

##### 手动安装

暂时么得，也许你可以参考下Windows的安装方法

###### 源码安装

暂时么得，也许你可以参考下Windows的安装方法

###### 至此 Linux 下的源码安装到此结束

---
#### 使用说明
安装配置完毕后在打开任意终端输入

    bin tgt_lang [text] [-options]
即可执行翻译到指定的语言，其中若text参数未提供则会以剪贴板最后一条为参数

##### 选项 -h --help

展示帮助选项

##### 选项 -c --copy
复制翻译后的文本到剪贴板

##### 选项 -d --debug
故障排查模式，没啥用

##### 选项 -s --split
指定将输入文本的字符替换为空格，以避免对翻译引擎的干扰接受多个参数，选项后所有给出的参数都将被作为排除文本

##### 选项 -l --list_all_lgtg
该选项用于展示所有支持的语言及其语言码用法如下,该选项支持i8n,将自动转换码表语言至指定语言。但目前不支持存储，每次调用时需要等候转换
    bin zh-Hans -l

<video src="/media/vedio/tgt_loading_zh.mp4" width="1920px" height="1080px" controls="controls"></video>

---

[1]:https://gitee.com/abchiyi/BinTerminaTranslator/releases

20/9/6 by Meme
