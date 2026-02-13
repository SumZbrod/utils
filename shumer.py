import pyudev
import time
import datetime
import subprocess
import random
import threading

# === Твои настройки ===
YOUR_EDIFIER_VID = "2d99"          # ← замени на свой VID из lsusb (hex, без 0x)
YOUR_EDIFIER_PID = "e067"          # ← замени на свой PID (hex, без 0x)
PUNISH_AFTER_HOUR = 18             # после 18:00 — без наказания
DELAY_AFTER_CONNECT = 60*5          # 5 минут спокойствия после подключения
MIN_BEEP_INTERVAL = 40            # мин пауза между писками (сек)
MAX_BEEP_INTERVAL = 240            # макс пауза (4 мин)
BEEP_COMMAND = ["aplay", "/home/user/Files/utils/annoying_beep.wav"]  # ← путь к файлу или ["aplay", ...]

# Глобальные
punishment_active = False
last_connect_time = None

def play_beep():
    try:
        subprocess.run(BEEP_COMMAND, timeout=3, check=False)
    except:
        pass

def punishment_loop():
    global punishment_active
    print("[EDIFIER USB] Наказание запущено — случайные писки...")
    while punishment_active:
        delay = random.randint(MIN_BEEP_INTERVAL, MAX_BEEP_INTERVAL)
        time.sleep(delay)
        if punishment_active:
            print(f"   → Писк! (пауза была {delay} сек)")
            play_beep()

def is_my_edifier_usb_added(device):
    if device.action != 'add':
        return False
    if device.subsystem != 'usb':
        return False

    vid = device.get('ID_VENDOR_ID')
    pid = device.get('ID_MODEL_ID')

    if vid == YOUR_EDIFIER_VID and pid == YOUR_EDIFIER_PID:
        # Дополнительно проверяем, что это аудио-устройство
        if 'Audio' in str(device) or device.get('DEVTYPE') == 'usb_device':
            return True
    return False

def monitor():
    global last_connect_time, punishment_active

    context = pyudev.Context()
    monitor = pyudev.Monitor.from_netlink(context)
    monitor.filter_by(subsystem='usb')

    print("Мониторим подключение твоих Edifier по USB...")

    for device in iter(monitor.poll, None):
        if is_my_edifier_usb_added(device):
            now = datetime.datetime.now()
            if now.hour >= PUNISH_AFTER_HOUR:
                print(f"Edifier USB подключены после {PUNISH_AFTER_HOUR}:00 → без писка")
                continue

            last_connect_time = time.time()
            print(f"Твои Edifier подключены по USB в {now.strftime('%H:%M')} → ждём {DELAY_AFTER_CONNECT//60} мин")

            # Ждём задержку
            time.sleep(DELAY_AFTER_CONNECT)

            # Если всё ещё подключены (можно добавить проверку remove, но для простоты)
            if time.time() - last_connect_time >= DELAY_AFTER_CONNECT:
                if not punishment_active:
                    punishment_active = True
                    threading.Thread(target=punishment_loop, daemon=True).start()

        # Опционально: ловим remove и останавливаем писк
        elif device.action == 'remove':
            vid = device.get('ID_VENDOR_ID')
            pid = device.get('ID_MODEL_ID')
            if vid == YOUR_EDIFIER_VID and pid == YOUR_EDIFIER_PID:
                punishment_active = False
                print("Edifier USB отключены → писк остановлен")

def main():
    return
    threading.Thread(target=monitor, daemon=True).start()

    try:
        while True:
            time.sleep(10)  # основной поток спит
    except KeyboardInterrupt:
        global punishment_active
        punishment_active = False
        print("Скрипт остановлен")

if __name__ == "__main__":
    main()