$prg = $HOME + '\.bin_terminal_translator'
$loc = (Get-Location).Path
Copy-Item $loc\* $prg -Recurse -Force
[System.Environment]::SetEnvironmentVariable("path", $env:Path + ';' + $prg + '\', "User")
