$prg = $HOME + '\.bin_terminal_translator'
$loc = (Get-Location).Path

Copy-Item $loc\* $prg -Recurse -Force
if ($env:Path -cnotmatch ($prg -replace '\\', '\\') ) {
    [System.Environment]::SetEnvironmentVariable(
        "path", $env:Path + ';' + $prg, "User"
    )
}
