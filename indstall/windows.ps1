# 安装位置
$prg = $HOME + '\bin_terminal_translator'
# 当前资源位置
$loc = (Get-Location).Path
# 复制到指定目录
Write-Output "复制文件... 请勿关闭"
Copy-Item $loc $prg -Recurse
# 添加环境变量
[System.Environment]::SetEnvironmentVariable("path", $env:Path + ';' + $prg + '\', "User")
