GetProcess | Where-Object { $_.MainWindowTitle -ne "" } | Select-Object Name, MainWindowTitle | Format-Table -AutoSize
