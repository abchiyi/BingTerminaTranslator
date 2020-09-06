# TODO 无效的安装脚本
$loc = (Get-Location ).Path
$prg = "C:\Program Files\BinTerminalTranslator"
# $loc = Split-Path -Parent $MyInvocation.MyCommand.Definition

# Start-Process powershell.exe -Verb runas -ArgumentList '-NoExit','-Command','&{cd (Get-Location).path }'
# $file_dir = 'C:\Program Files\sspp'
# Write-Output $prgram_file


# Copy-Item $prgram_file $file_dir
# Start-Process -FilePath powershell.exe -Verb runas -ArgumentList "-noprofile -command "

# $env:Path += ';hello'
# [System.Environment]::SetEnvironmentVariable("path", $env:Path, "User")
