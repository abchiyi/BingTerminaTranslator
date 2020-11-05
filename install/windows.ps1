#!code UTF-16LE CRLF
$prg = $HOME + '\.bin_terminal_translator\'
$loc = (Get-Location).Path

Write-Output 创建目录
mkdir $prg
Write-Output 写入文件...
Copy-Item $loc\* $prg -Recurse -Force

# 设定主目录变量，以暴露bin文件
Write-Output 检查环境变量 BTT_HOME
if ( -not $env:BTR_HOME){
    Write-Output 写入
    [System.Environment]::SetEnvironmentVariable(
        "BTT_HOME",
        $prg,
        "User"
    )
    Write-Output 成功
}

# 该环境变量包含了 主目录和脚本目录
$new_path = ';%BTT_HOME%;%BTT_HOME%\scripts'



Write-Output 检查path环境变量
# 做匹验证 在path中不包含时为真
if ($env:path -cnotmatch $new_path){
    Write-Output 写入
    [System.Environment]::SetEnvironmentVariable(
        'path',
        $env:path+$new_path,
        "User"
    )
    Write-Output 成功
}


Write-Output 安装完成
