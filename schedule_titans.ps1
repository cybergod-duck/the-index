$Principal = New-ScheduledTaskPrincipal -UserId "$env:USERDOMAIN\$env:USERNAME" -LogonType Interactive
$Settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable

$ScriptPath = "C:\Users\ovjup\Dropbox\VNR  Projects\the-index"

# 1. 📌 Pinterest Titan (Runs at 9:00 AM)
$ActionPin = New-ScheduledTaskAction -Execute "python" -Argument "$ScriptPath\solo_titan.py" -WorkingDirectory $ScriptPath
$TriggerPin = New-ScheduledTaskTrigger -Daily -At 9am
Register-ScheduledTask -TaskName "TrafficTitan_Pinterest" -Action $ActionPin -Trigger $TriggerPin -Principal $Principal -Settings $Settings -Force
Write-Host "✅ Pinterest Titan scheduled for 9:00 AM" -ForegroundColor Cyan

# 2. 👾 Reddit Titan (Runs at 12:00 PM)
$ActionReddit = New-ScheduledTaskAction -Execute "python" -Argument "$ScriptPath\reddit_titan.py" -WorkingDirectory $ScriptPath
$TriggerReddit = New-ScheduledTaskTrigger -Daily -At 12pm
Register-ScheduledTask -TaskName "TrafficTitan_Reddit" -Action $ActionReddit -Trigger $TriggerReddit -Principal $Principal -Settings $Settings -Force
Write-Host "✅ Reddit Titan scheduled for 12:00 PM" -ForegroundColor Cyan


Write-Host "`n🚀 ALL TRAFFIC ENGINES ARE NOW ARMED AND FULLY AUTOMATED!" -ForegroundColor Green
