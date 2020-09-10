# BinTerminaTranslator

## 介绍

该项目设计为内建内建在终端内的快速翻译工具
语言支持建立在必应翻译接口上

---

### 下载

[各版本下载[gitee]][1]

---

### 安装教程

#### ![Gitee](/media/SVG/windows.svg "Windwos") <font color='blue'>Windwos 安装配置</font>

###### 脚本安装

下载最新的Windows发行版，该版本以打包运行环境无需配置运行环境。解压并右键执行“indtall.ps1”脚本即可。
异或者克隆最新仓库，执行“packeg_for_windws.ps1”来打包最新的版本，当然你需要确保运行环境正常，打包完毕将在桌面生成安装包，其版本号将沿用最新版本号


###### 手动安装

!!!**源码运行仅支持Python3.6或更高版本**!!!

首先你需要确保安装 python3.6 或更高版本，python系统变量名为“python”

    $prg = $HOME + '\bin_terminal_translator'
    git clone https://gitee.com/abchiyi/BinTerminaTranslator $prg
    cd $prg

现在安装所需的运行库

    python -m pip install -r .\packges

现在你已经有了一个能够执行的环境了，只需将其配置到系统环境即可

    cp .\bin.py .\co.py
    del .\bin.py
    echo "python $prg\co.py `$args" > .\bin.ps1

最后将目录添加至用户环境变量

    [System.Environment]::SetEnvironmentVariable("path", $env:Path + ';' + $prg + '\', "User")

###### 至此 Windows 下安装结束

---

#### ![linux](/media/SVG/linux.svg "Linux") <font color='Yellow'>Linux安装配置</font>

暂时么得

##### 手动安装

暂时么得，也许你可以参考下Windows的安装方法是🤔

###### 源码安装

暂时么得，也许你可以参考下Windows的安装方法是🤔

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

![tgt loading](/media/gif/tgt_loading_zh.gif "转换至码表解释至目标语言")

[1]:https://gitee.com/abchiyi/BinTerminaTranslator/releases

---

20/9/6 by Meme
