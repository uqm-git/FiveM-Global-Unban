# 🧹 UNBAN — FiveM Spoofer

A Python tool for cleaning FiveM and Windows artifacts commonly associated with hardware/account bans. It removes caches, logs, registry entries, Xbox services, and resets GameDVR policies.
In order to get unbaned, you have to login into a new Rockstar Account.


> ⚠️ **Disclaimer:** This tool is intended for educational and research purposes only. Using it may violate the Terms of Service of FiveM, Rockstar Games, and Microsoft. Use at your own risk.
>
> The author does **not guarantee** that using this software will remove, prevent, bypass, or otherwise affect any account, hardware, platform, or service restriction.
>
> You are solely responsible for determining whether running this software is permitted under the Terms of Service, license agreements, or other rules applicable to your accounts, software, hardware, and jurisdiction.
>
> **Use of this software is entirely at your own risk.**
> 
---

## 📋 Features

- Deletes the `data` folder inside `FiveM.app`
- Clears the `DigitalEntitlements` folder
- Removes Windows and application log files
- Deletes FiveM cache, log, and crash folders
- Stops and deletes Xbox services (`XblAuthManager`, `XblGameSave`, `XboxNetApiSvc`, `XboxGipSvc`)
- Cleans related registry keys
- Disables Xbox-related scheduled tasks
- Disables the GameDVR policy
- Clean menu with colored status output


## ⚙️ Requirements

- **Windows 10 / 11**
- **Python 3.8+**
- **Administrator privileges** (required for registry and service operations)


## 📁 What Gets Cleaned?

- Area                                      Action
- `%LocalAppData%\FiveM\FiveM.app\data`       Delete folder
- `%LocalAppData%\DigitalEntitlements  `      Delete contents
- `%LocalAppData%\FiveM.app\cache, logs, crashes`  Delete folders
- `%LocalAppData%\Microsoft\Windows\INetCache`     Delete folder
- Windows log directories (cbs, MoSetup, Panther, inf, …)  Delete *.log
- Xbox services (XblAuthManager, XblGameSave, XboxNetApiSvc, XboxGipSvc)  Stop & delete
- Registry keys (CitizenFX, Valve, INextUUID, xbgm, …)  Delete
- Scheduled tasks (XblGameSaveTask, XblGameSaveTaskLogon)  Disable
- GameDVR policy                             Disable

## Please leave a ⭐ if you like it
