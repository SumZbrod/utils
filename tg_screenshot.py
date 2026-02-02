import os
import asyncio
import random
import subprocess
from telethon import TelegramClient
from PIL import Image
import numpy as np
import timm
from torchvision import transforms
import torch

claster_cats=[
    0,#0
    0,#1
    0,#2
    1,#3
    1,#4
    1,#5
    1,#6
    0,#7
    1,#8
    1,#9
]
with open("K_centrs.npy", 'rb') as f:
    K_centrs = np.load(f)
device = "cuda"

model = timm.create_model(
    "vit_base_patch14_dinov2",
    pretrained=True,
    num_classes=0
).to(device).eval()

transform = transforms.Compose([
    transforms.Resize(518),
    transforms.CenterCrop(518),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=(0.485, 0.456, 0.406),
        std=(0.229, 0.224, 0.225),
    ),
])

def embed_image(path):
    img = Image.open(path).convert("RGB")
    x = transform(img).unsqueeze(0).to(device)
    with torch.no_grad():
        return model(x).cpu().numpy()[0]

def get_claster_cat(path):
    p = embed_image(path)
    argmin = int(np.argmin([np.linalg.norm(k - p) for k in K_centrs]))
    return claster_cats[argmin]


# ===== ENV =====
api_id = int(os.getenv("TG_API_ID"))
api_hash = os.getenv("TG_API_HASH")
channel_id = int(os.getenv("TG_CHANNEL_ID"))

BASE_INTERVAL = 15 * 60
RANDOM_SHIFT = 13 * 60
SCREEN_PATH = "/tmp/tg_screen2.png"
SESSION = os.environ.get("XDG_SESSION_TYPE", "x11")
MIN_SCREENSHOT_SIZE = 100 * 1024   # 100 KB
RETRY_DELAY = 5 * 60               # 5 минут

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


def is_screenshot_valid(path):
    # файл существует
    if not os.path.exists(path):
        return False

    # проверка размера
    if os.path.getsize(path) < MIN_SCREENSHOT_SIZE:
        return False

    # проверка разрешения (на всякий случай)
    try:
        with Image.open(path) as img:
            w, h = img.size
            if w < 100 or h < 100:
                return False
    except Exception:
        return False

    return True

# ---------- MAIN ----------
async def main():
    await client.start()
    INCRIMINANT = 0
    BREAK_MESSEAGE_ALREADY_SENTED = False
    while True:
        screenshot = make_screenshot()
        if not is_screenshot_valid(screenshot):
            if os.path.exists(screenshot):
                os.remove(screenshot)
            if not BREAK_MESSEAGE_ALREADY_SENTED:
                await client.send_message(
                    channel_id,
                    "Сейчас перерыв"
                )
                BREAK_MESSEAGE_ALREADY_SENTED = True
            await asyncio.sleep(random.randint(0, RANDOM_SHIFT))
            continue
        screenshot_cat = get_claster_cat(screenshot)
        caption = f"#{INCRIMINANT} | cat {screenshot_cat}"
        INCRIMINANT += 1
        await client.send_file(
            channel_id,
            screenshot,
            caption=caption
        )

        os.remove(screenshot)

        BREAK_MESSEAGE_ALREADY_SENTED = False
        delay = BASE_INTERVAL +  RANDOM_SHIFT * (2*random.random()-1)**3
        print("delay =", delay)
        await asyncio.sleep(delay)

asyncio.run(main())
