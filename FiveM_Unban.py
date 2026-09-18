import ctypes
import os
import re
import shutil
import subprocess
import sys
import time
from datetime import datetime

if os.name == "nt":
    os.system("")


class C:
    RESET   = "\033[0m"
    BOLD    = "\033[1m"
    DIM     = "\033[2m"
    RED     = "\033[91m"
    GREEN   = "\033[92m"
    YELLOW  = "\033[93m"
    BLUE    = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN    = "\033[96m"
    WHITE   = "\033[97m"
    GRAY    = "\033[90m"

    TEAL     = "\033[38;5;43m"
    TEAL_LT  = "\033[38;5;80m"
    MINT     = "\033[38;5;121m"
    LIME     = "\033[38;5;155m"
    AMBER    = "\033[38;5;214m"
    CORAL    = "\033[38;5;203m"
    ROSE     = "\033[38;5;211m"
    INDIGO   = "\033[38;5;105m"
    SKY      = "\033[38;5;117m"
    STEEL    = "\033[38;5;67m"
    SLATE    = "\033[38;5;60m"
    COAL     = "\033[38;5;236m"

    HIDE = "\033[?25l"
    SHOW = "\033[?25h"


SYM_DOT   = "•"
SYM_OK    = "✓"
SYM_FAIL  = "✗"
SYM_ARROW = "›"
SYM_BOLT  = "⌁"
SYM_LOCK  = "⚿"
SYM_WARN  = "⚠"

GITHUB = "github.com/uqm-git"

DOTS = ["·  ", "·· ", "···", " ··", "  ·", "   "]


ANSI_RE = re.compile(r"\x1b\[[0-9;?]*[a-zA-Z]")


def vlen(s):
    return len(ANSI_RE.sub("", s))


def pad(s, width):
    return s + " " * max(0, width - vlen(s))


def term_width():
    try:
        w = shutil.get_terminal_size().columns
    except Exception:
        w = 80
    return max(80, min(w - 2, 120))


def clear():
    os.system("cls" if os.name == "nt" else "clear")


def hide():
    sys.stdout.write(C.HIDE)
    sys.stdout.flush()


def show():
    sys.stdout.write(C.SHOW)
    sys.stdout.flush()


def typewriter(text, color=C.SKY, delay=0.008, prefix="  "):
    hide()
    sys.stdout.write(prefix)
    for ch in text:
        sys.stdout.write(C.BOLD + color + ch + C.RESET)
        sys.stdout.flush()
        time.sleep(delay)
    sys.stdout.write("\n")
    show()


def marquee(text, color=C.TEAL_LT, duration=1.0):
    w = term_width() - 6
    padded = "  " + text + "  " * 6
    end = time.time() + duration
    i = 0
    hide()
    while time.time() < end:
        segment = (padded * 3)[i:i + w]
        sys.stdout.write(f"\r  {C.BOLD}{color}{segment}{C.RESET}")
        sys.stdout.flush()
        time.sleep(0.04)
        i += 1
    sys.stdout.write("\r" + " " * (w + 6) + "\r")
    show()


LOGO = [
    "  ███████╗██╗██╗   ██╗███████╗███╗   ███╗",
    "  ██╔════╝██║██║   ██║██╔════╝████╗ ████║",
    "  █████╗  ██║██║   ██║█████╗  ██╔████╔██║",
    "  ██╔══╝  ██║╚██╗ ██╔╝██╔══╝  ██║╚██╔╝██║",
    "  ██║     ██║ ╚████╔╝ ███████╗██║ ╚═╝ ██║",
    "  ╚═╝     ╚═╝  ╚═══╝  ╚══════╝╚═╝     ╚═╝",
    "          C L E A N E R   ·   v 3",
]

LOGO_COLORS = [C.STEEL, C.SKY, C.TEAL_LT, C.MINT,
               C.TEAL_LT, C.SKY, C.AMBER]


def animate_logo():
    for i, line in enumerate(LOGO):
        col = LOGO_COLORS[i % len(LOGO_COLORS)]
        print("  " + C.BOLD + col + line + C.RESET)
        time.sleep(0.05)


def boot():
    w = term_width()
    clear()
    print()


    print("  " + C.COAL + "─" * (w - 4) + C.RESET)
    print()

    animate_logo()

    print()
    marquee(f"{SYM_BOLT}  N E O N  ·  D A S H B O A R D  ·  E D I T I O N  {SYM_BOLT}",
            C.TEAL_LT, duration=0.9)

    print()
    print("  " + C.COAL + "─" * (w - 4) + C.RESET)
    time.sleep(0.1)
    print()


def is_admin():
    try:
        return bool(ctypes.windll.shell32.IsUserAnAdmin())
    except Exception:
        return False


def require_admin():
    if not is_admin():
        w = term_width()
        print()
        print(C.CORAL + "  ┌" + "─" * (w - 4) + "┐" + C.RESET)
        print(C.CORAL + "  │ " + C.BOLD + C.CORAL
              + f"{SYM_LOCK}  ADMIN PRIVILEGES REQUIRED"
              + C.RESET
              + " " * (w - 34)
              + C.CORAL + "│" + C.RESET)
        print(C.CORAL + "  │ " + C.WHITE
              + "Restart this tool as Administrator."
              + C.RESET
              + " " * (w - 42)
              + C.CORAL + "│" + C.RESET)
        print(C.CORAL + "  └" + "─" * (w - 4) + "┘" + C.RESET)
        print()
        input(f"  {C.GRAY}ENTER to exit…{C.RESET}")
        sys.exit(1)


def run(cmd):
    return subprocess.run(cmd, shell=True,
                          stdout=subprocess.DEVNULL,
                          stderr=subprocess.DEVNULL).returncode


def status_lines(inner_w):
    local = os.environ.get("LocalAppData", "")
    fivem = os.path.join(local, "FiveM", "FiveM.app")
    ent = os.path.join(local, "DigitalEntitlements")
    fivem_ok = os.path.exists(fivem)
    ent_ok = os.path.exists(ent)

    try:
        total, used, free = shutil.disk_usage("C:\\")
        free_gb = free / (1024 ** 3)
        total_gb = total / (1024 ** 3)
        pct = int(used / total * 100)
        bar_w = max(10, inner_w - 8)
        filled = int(pct / 100 * bar_w)
        disk_bar = "█" * filled + "░" * (bar_w - filled)
    except Exception:
        free_gb, total_gb, pct, disk_bar = 0, 0, 0, "░" * 18

    user = os.environ.get("USERNAME", "?")

    rows = [
        f"{C.SLATE}SYSTEM{C.RESET}",
        f"{C.TEAL_LT}{SYM_DOT}{C.RESET} "
        f"{C.SLATE}User  {C.RESET}{C.WHITE}{user}{C.RESET}",
        "",
        f"{C.SLATE}DISK  C:{C.RESET}",
        f"{C.SKY}{disk_bar}{C.RESET}  {C.WHITE}{pct}%{C.RESET}",
        f"{C.GRAY}{free_gb:0.1f} / {total_gb:0.1f} GB free{C.RESET}",
        "",
        f"{C.SLATE}FIVEM{C.RESET}",
        (f"{C.MINT}{SYM_OK}{C.RESET} app_data"
         if fivem_ok else f"{C.GRAY}○{C.RESET} app_data"),
        (f"{C.MINT}{SYM_OK}{C.RESET} entitlements"
         if ent_ok else f"{C.GRAY}○{C.RESET} entitlements"),
    ]
    return rows


def dashboard():
    clear()
    w = term_width()

    left_title = (f"{C.BOLD}{C.SKY}FIVEM Spoofer{C.RESET} "
                  f"{C.SLATE}·{C.RESET} "
                  f"{C.TEAL_LT}DASHBOARD{C.RESET}")
    ts = datetime.now().strftime("%a %d.%m · %H:%M:%S")
    head_visible = "FIVEM Spoofer · DASHBOARD"
    space = (w - 4) - len(head_visible) - len(ts)
    print()
    print("  " + left_title + " " * max(1, space) + f"{C.GRAY}{ts}{C.RESET}")
    print("  " + C.COAL + "─" * (w - 4) + C.RESET)
    print()

    total_w = w - 4
    gap = 3
    left_w = int(total_w * 0.58)
    right_w = total_w - left_w - gap

    menu_items = [
        ("1", "Remove CFX Ban",
         "does not remove hardware bans", C.CORAL),
        ("2", "Exit",
         "close the dashboard", C.SLATE),
    ]

    L = []
    L.append(C.STEEL + "┌" + "─" * (left_w - 2) + "┐" + C.RESET)
    title = " A C T I O N S "
    rem = (left_w - 2) - len(title)
    ll = rem // 2
    lr = rem - ll
    L.append(C.STEEL + "├" + "─" * ll + C.RESET
             + C.BOLD + C.SKY + title + C.RESET
             + C.STEEL + "─" * lr + "┤" + C.RESET)

    for key, name, desc, col in menu_items:
        badge = f"[{key}]"
        inner = f"  {C.BOLD}{col}{badge}{C.RESET} {C.BOLD}{C.WHITE}{name}{C.RESET}"
        L.append(C.STEEL + "│" + C.RESET + pad(inner, left_w - 2)
                 + C.STEEL + "│" + C.RESET)
        inner2 = f"       {C.GRAY}{desc}{C.RESET}"
        L.append(C.STEEL + "│" + C.RESET + pad(inner2, left_w - 2)
                 + C.STEEL + "│" + C.RESET)
        L.append(C.STEEL + "│" + C.RESET
                 + " " * (left_w - 2) + C.STEEL + "│" + C.RESET)

    L.pop()
    L.append(C.STEEL + "└" + "─" * (left_w - 2) + "┘" + C.RESET)

    R = []
    R.append(C.STEEL + "┌" + "─" * (right_w - 2) + "┐" + C.RESET)
    title_r = " S T A T U S "
    rem = (right_w - 2) - len(title_r)
    rl = rem // 2
    rr = rem - rl
    R.append(C.STEEL + "├" + "─" * rl + C.RESET
             + C.BOLD + C.TEAL_LT + title_r + C.RESET
             + C.STEEL + "─" * rr + "┤" + C.RESET)

    for line in status_lines(right_w - 2):
        R.append(C.STEEL + "│" + C.RESET + pad(" " + line, right_w - 2)
                 + C.STEEL + "│" + C.RESET)

    while len(R) < len(L) - 1:
        R.append(C.STEEL + "│" + C.RESET
                 + " " * (right_w - 2) + C.STEEL + "│" + C.RESET)

    R.append(C.STEEL + "└" + "─" * (right_w - 2) + "┘" + C.RESET)

    rows = max(len(L), len(R))
    L += [" " * left_w] * (rows - len(L))
    R += [" " * right_w] * (rows - len(R))

    for l, r in zip(L, R):
        print("  " + pad(l, left_w) + " " * gap + r)

    print()
    print("  " + C.COAL + "─" * (w - 4) + C.RESET)
    foot_left = f"{C.GRAY}⌥ {C.SKY}{GITHUB}{C.RESET}"
    foot_right = f"{C.SLATE}v3.0 · neon{C.RESET}"
    print("  " + pad(foot_left, (w - 4) - vlen(foot_right)) + foot_right)
    print()


class Task:
    def __init__(self, name, fn, tag="clean"):
        self.name = name
        self.fn = fn
        self.done = False
        self.tag = tag


def make_tasks():
    local = os.environ.get("LocalAppData", "")
    fivem = os.path.join(local, "FiveM", "FiveM.app")
    ent = os.path.join(local, "DigitalEntitlements")

    def rm_data():
        p = os.path.join(fivem, "data")
        if os.path.exists(p):
            shutil.rmtree(p, ignore_errors=True)

    def clean_ent():
        if not os.path.exists(ent):
            return
        for e in os.listdir(ent):
            p = os.path.join(ent, e)
            try:
                if os.path.isdir(p):
                    shutil.rmtree(p, ignore_errors=True)
                else:
                    os.remove(p)
            except Exception:
                pass

    def dirs():
        for d in [
            os.path.join(local, "Microsoft", "Windows", "INetCache"),
            os.path.join(fivem, "cache"),
            os.path.join(fivem, "logs"),
            os.path.join(fivem, "crashes"),
        ]:
            shutil.rmtree(d, ignore_errors=True)

    def takeown():
        run(r"takeown /A /R /D Y /F C:\windows\temp")
        os.makedirs(r"C:\windows\temp", exist_ok=True)

    def logs():
        for folder in [
            r"C:\windows\logs\cbs", r"C:\Windows\Logs\MoSetup",
            r"C:\Windows\Panther", r"C:\Windows\inf",
            r"C:\Windows\logs", r"C:\Windows\SoftwareDistribution",
            r"C:\Windows\Microsoft.NET",
            os.path.join(local, "Microsoft", "Windows", "WebCache"),
            os.path.join(local, "Microsoft", "Windows", "SettingSync"),
        ]:
            if not os.path.exists(folder):
                continue
            for root, _, files in os.walk(folder):
                for f in files:
                    if f.lower().endswith(".log"):
                        try:
                            os.remove(os.path.join(root, f))
                        except Exception:
                            pass

    def stop():
        for s in ["XblAuthManager", "XblGameSave",
                  "XboxNetApiSvc", "XboxGipSvc"]:
            run(f"sc stop {s}")

    def delete():
        for s in ["XblAuthManager", "XblGameSave",
                  "XboxNetApiSvc", "XboxGipSvc"]:
            run(f"sc delete {s}")

    def reg():
        for k in [
            r"HKLM\SYSTEM\CurrentControlSet\Services\xbgm",
            r"HKEY_LOCAL_MACHINE\SOFTWARE\INextUUID",
            r"HKEY_CURRENT_USER\SOFTWARE\Microsoft\Windows\CurrentVersion\Run",
            r"HKEY_CURRENT_USER\SOFTWARE\CitizenFX",
            r"HKEY_CURRENT_USER\SOFTWARE\Valve",
            r"HKEY_CURRENT_USER\SOFTWARE\nk",
        ]:
            run(f'reg delete "{k}" /f')

    def tasks_off():
        run(r'schtasks /Change /TN "Microsoft\XblGameSave\XblGameSaveTask" /disable')
        run(r'schtasks /Change /TN "Microsoft\XblGameSave\XblGameSaveTaskLogon" /disable')

    def dvr():
        run(r'reg add "HKLM\SOFTWARE\Policies\Microsoft\Windows\GameDVR" '
            r'/v AllowGameDVR /t REG_DWORD /d 0 /f')

    return [
        Task("Purge FiveM data cache",       rm_data,   "fivem"),
        Task("Clean DigitalEntitlements",    clean_ent, "fivem"),
        Task("Remove stale directories",     dirs,      "fivem"),
        Task("Take ownership of temp",       takeown,   "system"),
        Task("Purge Windows log files",      logs,      "system"),
        Task("Stop Xbox services",           stop,      "system"),
        Task("Delete Xbox services",         delete,    "system"),
        Task("Clean registry traces",        reg,       "system"),
        Task("Disable Xbox scheduled tasks", tasks_off, "system"),
        Task("Enforce GameDVR policy",       dvr,       "system"),
    ]


def tag_color(tag):
    return {"fivem": C.AMBER, "system": C.SKY}.get(tag, C.MINT)


def render_runner(tasks):
    clear()
    w = term_width()
    print()
    print(f"  {C.BOLD}{C.SKY}PIPELINE{C.RESET} "
          f"{C.SLATE}·{C.RESET} "
          f"{C.TEAL_LT}executing {len(tasks)} tasks{C.RESET}")
    print("  " + C.COAL + "─" * (w - 4) + C.RESET)
    print()

    hide()
    name_pad = 38

    for i, t in enumerate(tasks):
        col = tag_color(t.tag)
        tag = f"[{t.tag}]"
        t0 = time.monotonic()

        try:
            t.fn()
            t.done = True
        except Exception:
            t.done = False

        spin_i = 0
        while time.monotonic() - t0 < 0.18:
            spin = DOTS[spin_i % len(DOTS)]
            line = (
                f"  {C.SLATE}{i+1:>2}/{len(tasks)}{C.RESET}  "
                f"{col}{tag:<9}{C.RESET}  "
                f"{C.WHITE}{t.name:<{name_pad}}{C.RESET}  "
                f"{C.SKY}{spin}{C.RESET}"
            )
            sys.stdout.write("\r" + line)
            sys.stdout.flush()
            spin_i += 1
            time.sleep(0.04)

        mark = f"{C.MINT}{SYM_OK}{C.RESET}" if t.done else f"{C.CORAL}{SYM_FAIL}{C.RESET}"
        line = (
            f"  {C.SLATE}{i+1:>2}/{len(tasks)}{C.RESET}  "
            f"{col}{tag:<9}{C.RESET}  "
            f"{C.WHITE}{t.name:<{name_pad}}{C.RESET}  "
            f"{mark}"
        )
        sys.stdout.write("\r" + line + "   \n")
        sys.stdout.flush()

    show()


def render_report(tasks):
    w = term_width()
    ok = sum(1 for t in tasks if t.done)
    fail = len(tasks) - ok
    pct = int(ok / len(tasks) * 100) if tasks else 0

    bar_w = min(50, w - 20)
    filled = int(pct / 100 * bar_w)
    bar = "█" * filled + "░" * (bar_w - filled)

    print()
    print("  " + C.COAL + "─" * (w - 4) + C.RESET)
    print()
    print(f"  {C.SLATE}success rate{C.RESET}")
    print(f"  {C.MINT}{bar}{C.RESET}  {C.BOLD}{C.WHITE}{pct}%{C.RESET}")
    print()
    print(f"  {C.MINT}{SYM_DOT}{C.RESET} {C.SLATE}passed  {C.RESET} {C.BOLD}{C.WHITE}{ok}{C.RESET}")
    print(f"  {C.CORAL}{SYM_DOT}{C.RESET} {C.SLATE}failed  {C.RESET} {C.BOLD}{C.WHITE}{fail}{C.RESET}")
    print(f"  {C.SKY}{SYM_DOT}{C.RESET} {C.SLATE}total   {C.RESET} {C.BOLD}{C.WHITE}{len(tasks)}{C.RESET}")
    print()


def run_pipeline():
    tasks = make_tasks()
    render_runner(tasks)
    render_report(tasks)
    wait()


def wait(msg="back"):
    print(f"  {C.GRAY}{SYM_ARROW} ENTER {msg}{C.RESET}", end="")
    try:
        input()
    except (KeyboardInterrupt, EOFError):
        pass


def main():
    try:
        boot()
    except (KeyboardInterrupt, EOFError):
        show()
        return

    require_admin()

    while True:
        dashboard()
        try:
            ch = input(f"  {C.BOLD}{C.SKY}{SYM_ARROW} {C.RESET}").strip()
        except (KeyboardInterrupt, EOFError):
            print()
            break

        if ch == "1":
            run_pipeline()
        elif ch == "2" or ch.lower() in ("q", "exit"):
            clear()
            print()
            typewriter("shutting down dashboard…", C.CORAL, delay=0.012)
            time.sleep(0.2)
            print(f"\n  {C.GRAY}⌥ {C.SKY}{GITHUB}{C.RESET}\n")
            break
        else:
            print(f"  {C.CORAL}{SYM_FAIL} invalid choice{C.RESET}")
            time.sleep(0.6)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        show()
        print(f"\n\n  {C.TEAL_LT}cancelled.{C.RESET}\n")