# BinTerminaTranslator

## 介绍

该项目设计为内建内建在终端内的快速翻译工具
语言支持建立在必应翻译接口上

[文档-Document][4] | [下载发行版][1]



## 如何使用

安装配置完毕后，命令行中输入即可执行翻译到指定的语言。

    bin 语言码 [文本] [选项]

### 选项 -l --list_all_lgtg
其中若text参数未提供则会以剪贴板最进的文本作为参数。
其中语言码为必需参数，输入以下代码查看语言码表，当前语言码为中文简体。
在查看时，其中的文本将自动被转换为中文简体以方便阅读。

    bin zh-Hans -l

该选项用于展示所有支持的语言及其语言码用法如下,该选项支持i8n,将自动转换码表语言至指定语言。但目前不支持存储，每次调用时需要等候转换

![tgt loading](/media/gif/tgt_loading_zh.gif "转换至码表解释至目标语言")

### 选项 -h --help

展示帮助选项

### 选项 -c --copy
复制翻译后的文本到剪贴板

### 选项 -d --debug
故障排查模式，没啥用

### 选项 -s --split
指定将输入文本的字符替换为空格，以避免对翻译引擎的干扰接受多个参数，选项后所有给出的参数都将被作为排除文本

## 在本地配置项目

### 下载源码
我建议你使用Windwos，在它上面配置项目相对简单。

你需要[Python][2]3.5及以上版本，一个[Git][3]管理器,你可以点击以上链接快速下载。

在终端中cd到你想保存文件的位置，执行下面的指令，然后它将保存在这里

    git clone https://gitee.com/abchiyi/BinTerminaTranslator

### 配置本地运行环境
当你的python安装好后你将有个pip管理器使用它来下载所有依赖包

项目所用到的包都记录在packges文件中,在终端中打开项目文件夹

    pip install -r ./packges

现在基本上都配置好了，你可以随心所欲地修改它了

<!-- 发行版链接 -->
[1]:https://gitee.com/abchiyi/BinTerminaTranslator/releases
<!-- python -->
[2]:https://www.python.org/downloads/windows/
<!-- git -->
[3]:https://git-scm.com/downloads
<!-- Doc网站 -->
<!-- TODO 待添加文档网站 -->
[4]:https:......
