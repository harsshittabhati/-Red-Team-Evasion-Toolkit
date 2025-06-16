<#
.SYNOPSIS
    Encodes a PowerShell script into Base64 for execution via -EncodedCommand.
#>

param (
    [Parameter(Mandatory=$true)]
    [string]$InputFile,

    [Parameter(Mandatory=$true)]
    [string]$OutputFile
)

if (-Not (Test-Path $InputFile)) {
    Write-Error "Input file does not exist."
    exit 1
}

$content = Get-Content $InputFile -Raw
$bytes = [System.Text.Encoding]::Unicode.GetBytes($content)
$encoded = [Convert]::ToBase64String($bytes)

$encoded | Out-File $OutputFile -Encoding ASCII
Write-Host "Base64-encoded script saved to $OutputFile"
