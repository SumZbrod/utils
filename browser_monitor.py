import subprocess
import time

# Настройки
CHECK_INTERVAL = 5          # секунды между проверками
MAX_TIME_ALLOWED = 60       # секунд — лимит за один "сеанс"
TELEGRAM_WM_CLASS = "telegramdesktop"   # в нижнем регистре, как мы приводим

ACCUMULATED_TIME = 0.0

def get_active_window_class():
    """Возвращает WM_CLASS в нижнем регистре или ''"""
    try:
        win_id = subprocess.check_output(["xdotool", "getactivewindow"]).decode().strip()
        output = subprocess.check_output(["xprop", "-id", win_id, "WM_CLASS"]).decode()
        parts = output.split('"')
        if len(parts) >= 4:
            class_name = parts[3].strip().lower()  # TelegramDesktop → telegramdesktop
            return class_name
        return ""
    except Exception:
        return ""

def is_telegram_active():
    cls = get_active_window_class()
    return TELEGRAM_WM_CLASS in cls

def close_telegram():
    global ACCUMULATED_TIME
    try:
        # Вариант 1: самый надёжный для Telegram Desktop на Linux
        subprocess.run(["pkill", "-f", "tsetup.*Telegram/Telegram"], check=False)
        
        # Вариант 2: если не сработает — попробуй это (раскомментируй)
        # subprocess.run(["killall", "-r", "telegram.*"], timeout=5)
        
        print(f"Telegram закрыт (накоплено {ACCUMULATED_TIME:.1f} сек)")
    except subprocess.TimeoutExpired:
        print("Закрытие Telegram зависло (timeout)")
    except Exception as e:
        print("Ошибка при закрытии Telegram:", e)

def main():
    global ACCUMULATED_TIME
    print("Мониторинг Telegram Desktop запущен.")
    print(f"Лимит: {MAX_TIME_ALLOWED} сек | Интервал: {CHECK_INTERVAL} сек")
    print(f"Ожидаемый WM_CLASS (lower): {TELEGRAM_WM_CLASS}")

    while True:
        if is_telegram_active():
            ACCUMULATED_TIME += CHECK_INTERVAL
            print(f"Telegram в фокусе → +{CHECK_INTERVAL} сек | всего {ACCUMULATED_TIME:.1f} сек")

            if ACCUMULATED_TIME > MAX_TIME_ALLOWED:
                print(f"Лимит превышен ({ACCUMULATED_TIME:.1f} сек) → закрываем")
                close_telegram()
        else:
            if ACCUMULATED_TIME > 0:
                ACCUMULATED_TIME = max(0, ACCUMULATED_TIME - CHECK_INTERVAL)
                print(f"Telegram НЕ в фокусе → -{CHECK_INTERVAL} сек | осталось {ACCUMULATED_TIME:.1f} сек")

        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nОстановлено пользователем.")