import os
import asyncio
import random
import subprocess
from telethon import TelegramClient
from PIL import Image
import time
import socks

# ===== ENV =====
api_id = int(os.getenv("TG_API_ID"))
api_hash = os.getenv("TG_API_HASH")
channel_id = int(os.getenv("TG_CHANNEL_ID"))

BASE_INTERVAL = 15 * 60
RANDOM_SHIFT = 13 * 60
SCREEN_PATH = "/tmp/tg_screen2.png"
SESSION = os.environ.get("XDG_SESSION_TYPE", "x11")
MIN_SCREENSHOT_SIZE = 50 * 1024   # 100 KB
RETRY_DELAY = 5 * 60               # 5 минут
SNAPSHOTS_PATH = '/home/user/Files/utils/snapshots/'

proxy = (socks.SOCKS5, "127.0.0.1", 10808)
client = TelegramClient(
    "/home/user/Files/utils/helsenki_session",
    api_id,
    api_hash,
    proxy=proxy,
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

def is_screenshot_valid(path):
    if not os.path.exists(path):
        return False
    if os.path.getsize(path) < MIN_SCREENSHOT_SIZE:
        return False
    try:
        with Image.open(path) as img:
            w, h = img.size
            if w < 100 or h < 100:
                return False
    except Exception:
        return False

    return True


async def main():
    print("start main")
    await client.start()
    INCRIMINANT = 0
    BREAK_MESSEAGE_ALREADY_SENTED = False

    last_screenshot_time = time.time()

    while True:
        print("loop")
        screenshot = make_screenshot()
        if not is_screenshot_valid(screenshot):
            if os.path.exists(screenshot):
                os.remove(screenshot)
            if not BREAK_MESSEAGE_ALREADY_SENTED:
                await client.send_message(channel_id, "Сейчас перерыв")
                BREAK_MESSEAGE_ALREADY_SENTED = True
            print("screenshot not valid")
            await asyncio.sleep(60)  # короткая пауза, если ошибка
            continue
        
        caption = f"#{INCRIMINANT}"
        print(f"{caption = }")
        INCRIMINANT += 1
        print("try send screenshot")
        await client.send_file(channel_id, screenshot, caption=caption)
        print("send complited screenshot")
        os.remove(screenshot)


        BREAK_MESSEAGE_ALREADY_SENTED = False

        now = time.time()
        elapsed = now - last_screenshot_time
        target_interval = BASE_INTERVAL + RANDOM_SHIFT * (2 * random.random() - 1)**3

        if elapsed >= target_interval:
            # уже прошло достаточно времени (после долгого suspend) — делаем скрин сразу
            last_screenshot_time = now
        else:
            sleep_needed = target_interval - elapsed
            await asyncio.sleep(sleep_needed)
            last_screenshot_time = time.time()
        

asyncio.run(main())
