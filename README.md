# BinTerminaTranslator

## 介绍

该项目设计为内建内建在终端内的快速翻译工具
语言支持建立在必应翻译接口上

---

## 下载

[各版本下载[gitee]][1]

---

## 安装教程

### ![Gitee](/media/SVG/windows.svg "Windwos") <font color='blue'>Windwos 安装配置</font>

#### 快速安装

下载最新的Windows[发行版][1]，解压并右键执行“install.ps1”脚本安装

#### 手动安装

首先你需要确保已安装 [python][2]3.5 或更高版本 以及 [Git][3]

请务必保证所有语句在同一命令窗口中执行，如有中断请删除所有文件从头再来

所有文件将被放置到你的'$HOME'目录下

    $prg = $HOME + '\.bin_terminal_translator'
    git clone https://gitee.com/abchiyi/BinTerminaTranslator $prg;cd $prg

现在安装所需的运行库

    python -m pip install -r .\install\packges_of_windows

执行打包程序



配置到系统环境变量


    [System.Environment]::SetEnvironmentVariable("path", $env:Path + ';' + $prg + '\', "User")

###### 至此 Windows 下安装结束

---

#### ![linux](/media/SVG/linux.svg "Linux") <font color='Yellow'>Linux安装配置</font>

    prg=~/.bin_terminal_translator
    git clone https://gitee.com/abchiyi/BinTerminaTranslator $prg;cd $prg
    bash ./install/linux.sh

##### zsh

    echo 'alias bin="~/.bin_terminal_translator/bin.sh"' >> ~/.zshrc
    touch  ~/.zshrc

##### bashrc

    echo 'alias bin="~/.bin_terminal_translator/bin.sh"' >> ~/.bashrc
    touch  ~/.bashrc

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

<!-- 发行版链接 -->
[1]:https://gitee.com/abchiyi/BinTerminaTranslator/releases
<!-- python -->
[2]:https://www.python.org/downloads/windows/
<!-- git -->
[3]:https://git-scm.com/downloads
