# BinTerminaTranslator

## 介绍

该项目设计为内建内建在终端内的快速翻译工具

## 翻译实现依赖项目
[Gitee bing-translation-for-python][1] | [Github bing-translation-for-python][1]

## 安装

    pip install bing_translator

## 如何使用

安装配置完毕后，命令行中输入即可执行翻译到指定的语言。
直接键入'bing'以查看帮助信息。下面是一个使用示例

    bing zh-Hans hello

### 选项 -l --list_all_lgtg
输入你所使用的语言的语言的语言码，例如'en'作为第一个参数，结尾附上'-l'开关
程序将以你的语言来展示指出的语言

    bin en -l

该选项用于展示所有支持的语言及其语言码用法如下,该选项支持i8n,将自动转换码表语言至指定语言。但目前不支持存储，每次调用时需要等候转换

### 选项 -h --help

展示帮助选项

### 选项 -c --copy
复制翻译后的文本到剪贴板

### 选项 -d --debug
故障排查模式，没啥用

<!-- Doc网站 -->

<!-- TODO bing-translation-for-python 项目地址 -->
<!-- Gitee -->
[1]:https://gitee.com/abchiyi/bing_translation_for_python

<!-- Github -->
[1]:https:......
