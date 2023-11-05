import subprocess
import psutil
import time
import re

LOW_BATTERRY_PERCENT=50


# Define PowerShell scripts.
change_theme_to_dark = (
"&{"
"$themePath = 'HKCU:Software\\Microsoft\\Windows\\CurrentVersion\\Themes\\Personalize';"
"Set-ItemProperty -Path $themePath -Name ColorPrevalence -Value 0;"
"Stop-Process -f -ProcessName explorer"
"}"
)

change_theme_to_red = (
    "&{"
    "$themePath = 'HKCU:Software\\Microsoft\\Windows\\CurrentVersion\\Themes\\Personalize';"
    "Set-ItemProperty -Path $themePath -Name ColorPrevalence -Value 1;"
    "Stop-Process -f -ProcessName explorer"
    "}"
)

get_theme_cmd = (
"&{"
"$themePath = 'HKCU:Software\\Microsoft\\Windows\\CurrentVersion\\Themes\\Personalize';"
"Get-ItemProperty -Path $themePath -Name ColorPrevalence ;"
"}"
)


# Function to get the bar theme.
def get_theme_color():
    theme_obj=subprocess.check_output(["powershell", "-Command", get_theme_cmd])
    theme_is_red=re.search('ColorPrevalence : 1',str(theme_obj))!=None 
    if theme_is_red:
        return "red"
    return "dark"


# Function to change the bar theme.
def change_bar_theme(theme):
    if theme == "red":
        subprocess.run(["powershell", "-Command", change_theme_to_red])
    else:
        subprocess.run(["powershell", "-Command", change_theme_to_dark])


# Function to handle low battery event.
def low_battery_alert():
    while True:
        battery_status = psutil.sensors_battery()
        theme_color=get_theme_color()
        if battery_status.percent < LOW_BATTERRY_PERCENT and not battery_status.power_plugged:      
            if(theme_color == "dark"):
                change_bar_theme("red")        
                print("Changing theme to red.")
        else:
            if(theme_color == "red"):
                change_bar_theme('dark')
                print("Changing theme to dark.")
        time.sleep(5)


low_battery_alert()