# 打包程序
pyinstaller.exe -D .\bin.py
# 源文件
$loc = (Get-Location).Path + '\dist\bin\.'
# 输出路径
$packge_name = $HOME + '\Desktop\Windows-x64-' + (git tag)[-1] + '.7z'
# 复制配置文件
mkdir .\dist\bin\ini\
Copy-Item .\ini\* .\dist\bin\ini\
Copy-Item .\install\windows.ps1 .\dist\bin\install.ps1
# 压缩
& 'C:\Program Files\7-Zip\7z.exe' a -t7z -r $packge_name $loc
# 清理k
Remove-Item .\build -Recurse
Remove-Item .\dist -Recurse
Remove-Item .\bin.spec
