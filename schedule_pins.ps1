# 🛠️ Pinterest Bot Daily Scheduler
# This script creates a Windows Task to run the pin_bot every day at 9:00 AM.

$Action = New-ScheduledTaskAction -Execute "C:\Projects\the-index\run_pin_bot.bat"
$Trigger = New-ScheduledTaskTrigger -Daily -At 9am
$Principal = New-ScheduledTaskPrincipal -UserId "$env:USERDOMAIN\$env:USERNAME" -LogonType Interactive
$Settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable

Register-ScheduledTask -TaskName "PinterestDailyPost" -Action $Action -Trigger $Trigger -Principal $Principal -Settings $Settings -Force

Write-Host "SUCCESS: Pinterest Daily Post task created successfully!" -ForegroundColor Green
Write-Host "Schedule: It will run every day at 9:00 AM."
