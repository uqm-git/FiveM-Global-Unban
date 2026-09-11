import os
import shutil
import subprocess
import sys
import ctypes
             
os.system("")

RED = "\033[91m"
RESET = "\033[0m"

BANNER = r"""
                                     █    ██  ███▄    █  ▄▄▄▄    ▄▄▄       ███▄    █ 
                                     ██  ▓██▒ ██ ▀█   █ ▓█████▄ ▒████▄     ██ ▀█   █ 
                                    ▓██  ▒██░▓██  ▀█ ██▒▒██▒ ▄██▒██  ▀█▄  ▓██  ▀█ ██▒
                                    ▓▓█  ░██░▓██▒  ▐▌██▒▒██░█▀  ░██▄▄▄▄██ ▓██▒  ▐▌██▒
                                    ▒▒█████▓ ▒██░   ▓██░░▓█  ▀█▓ ▓█   ▓██▒▒██░   ▓██░
                                    ░▒▓▒ ▒ ▒ ░ ▒░   ▒ ▒ ░▒▓███▀▒ ▒▒   ▓▒█░░ ▒░   ▒ ▒ 
                                    ░░▒░ ░ ░ ░ ░░   ░ ▒░▒░▒   ░   ▒   ▒▒ ░░ ░░   ░ ▒░
                                     ░░░ ░ ░    ░   ░ ░  ░    ░   ░   ▒      ░   ░ ░ 
                                       ░              ░  ░            ░  ░         ░ 
                                                              ░
"""

def log(msg):
    print(f"[{RED}-{RESET}] {msg}")

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except Exception:
        return False

def run(cmd):
    subprocess.run(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def clean_fivem():
    local_app_data = os.environ.get("LocalAppData", "")
    fivem_app_data = os.path.join(local_app_data, "FiveM", "FiveM.app")
    digital_entitlements = os.path.join(local_app_data, "DigitalEntitlements")

    data_folder = os.path.join(fivem_app_data, "data")
    if os.path.exists(data_folder):
        log(f"Deleting {data_folder}...")
        shutil.rmtree(data_folder, ignore_errors=True)
    else:
        log(f"Folder {data_folder} does not exist.")

    if os.path.exists(digital_entitlements):
        log(f"Cleaning contents of {digital_entitlements}...")
        for entry in os.listdir(digital_entitlements):
            path = os.path.join(digital_entitlements, entry)
            try:
                if os.path.isdir(path):
                    shutil.rmtree(path, ignore_errors=True)
                else:
                    os.remove(path)
            except Exception:
                pass
    else:
        log(f"Folder {digital_entitlements} does not exist.")

    log("Taking ownership of the temp directory...")
    run('takeown /A /R /D Y /F C:\\windows\\temp')

    if not os.path.exists("C:\\windows\\temp"):
        log("Creating temp directory...")
        os.makedirs("C:\\windows\\temp", exist_ok=True)

    log("Deleting log files...")
    log_patterns = [
        ("C:\\windows\\logs\\cbs", "*.log"),
        ("C:\\Windows\\Logs\\MoSetup", "*.log"),
        ("C:\\Windows\\Panther", "*.log"),
        ("C:\\Windows\\inf", "*.log"),
        ("C:\\Windows\\logs", "*.log"),
        ("C:\\Windows\\SoftwareDistribution", "*.log"),
        ("C:\\Windows\\Microsoft.NET", "*.log"),
        (os.path.join(local_app_data, "Microsoft", "Windows", "WebCache"), "*.log"),
        (os.path.join(local_app_data, "Microsoft", "Windows", "SettingSync"), "*.log"),
    ]
    for folder, pattern in log_patterns:
        if os.path.exists(folder):
            for root, _, files in os.walk(folder):
                for f in files:
                    if pattern == "*" or f.lower().endswith(pattern.replace("*", "")):
                        try:
                            os.remove(os.path.join(root, f))
                        except Exception:
                            pass

    log("Removing directories...")
    dirs_to_remove = [
        os.path.join(local_app_data, "Microsoft", "Windows", "INetCache"),
        os.path.join(fivem_app_data, "cache"),
        os.path.join(local_app_data, "FiveM.app", "logs"),
        os.path.join(local_app_data, "FiveM.app", "crashes"),
    ]
    for d in dirs_to_remove:
        shutil.rmtree(d, ignore_errors=True)

    log("Stopping Xbox services...")
    for svc in ["XblAuthManager", "XblGameSave", "XboxNetApiSvc", "XboxGipSvc"]:
        run(f"sc stop {svc}")

    log("Deleting Xbox services...")
    for svc in ["XblAuthManager", "XblGameSave", "XboxNetApiSvc", "XboxGipSvc"]:
        run(f"sc delete {svc}")

    log("Cleaning the registry...")
    reg_keys = [
        r"HKLM\SYSTEM\CurrentControlSet\Services\xbgm",
        r"HKEY_LOCAL_MACHINE\SOFTWARE\INextUUID",
        r"HKEY_CURRENT_USER\SOFTWARE\Microsoft\Windows\CurrentVersion\Run",
        r"HKEY_CURRENT_USER\SOFTWARE\CitizenFX",
        r"HKEY_CURRENT_USER\SOFTWARE\Valve",
        r"HKEY_CURRENT_USER\SOFTWARE\nk",
    ]
    for key in reg_keys:
        run(f'reg delete "{key}" /f')

    log("Disabling tasks...")
    run('schtasks /Change /TN "Microsoft\\XblGameSave\\XblGameSaveTask" /disable')
    run('schtasks /Change /TN "Microsoft\\XblGameSave\\XblGameSaveTaskLogon" /disable')

    log("Setting GameDVR policy...")
    run('reg add "HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows\\GameDVR" /v AllowGameDVR /t REG_DWORD /d 0 /f')

    log("Cleanup complete!")
    input("Press Enter to exit...")


def menu():
    while True:
        os.system("cls")
        print(f"{RED}{BANNER}{RESET}")
        print("1. Clean FiveM")
        print("2. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            log("Cleaning FiveM...")
            clean_fivem()
        elif choice == "2":
            sys.exit(0)
        else:
            log("Invalid option. Please try again.")
            input("Press Enter to continue...")


def main():
    if not is_admin():
        log("This script requires administrative privileges. Please run it as an administrator.")
        input("Press Enter to exit...")
        sys.exit(1)
    menu()


if __name__ == "__main__":
    main()