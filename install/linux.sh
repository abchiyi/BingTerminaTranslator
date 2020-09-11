#!/usr/bin/env bash

prg_path=~/bin_terminal_translator/
python_path=$(which python)
if (($?!=0));then
    python_path=$(which python3)
fi

if (($?!=0)); then
    echo "未找到'python'运行环境,请确保您的计算机中正确配置了'python'环境"
    exit 1
fi

$python_path -m pip -V
if (($?!=0)); then
    echo 没有pip包管理器,请为 $python_path 下的python安装pip包管理器
    exit 1
fi
$python_path -m pip install -r $prg_path'install/packegs_of_linux'

mv $prg_path'bin.py' $prg_path'co.py'

echo '#!'$(which bash) > $prg_path/bin.sh
echo $python_path $prg_path'co.py $*' >> $prg_path'bin.sh'
chmod 700 $prg_path'bin.sh'
exit 0
