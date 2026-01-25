import subprocess
import time
import os
import signal

# Настройки
CHECK_INTERVAL = 1
MAX_TIME_ON_SITE = 60
BROWSER_PROCESS_NAME = "firefox" 

restricted_domains = {
    "web.telegram.org": 0,
    "youtube": 0,
}

def get_active_window_title():
    try:
        # Получаем ID активного окна
        window_id = subprocess.check_output(["xdotool", "getactivewindow"]).decode().strip()
        # Получаем заголовок окна
        title = subprocess.check_output(["xprop", "-id", window_id, "_NET_WM_NAME"]).decode()
        title = title.split('=')[1].strip().strip('"')  # Очищаем
        return title
    except Exception as e:
        print(f"Ошибка получения заголовка: {e}")
        return None

def close_browser():
    try:
        # Закрываем процесс браузера (можно заменить на закрытие окна через xdotool)
        subprocess.run(["pkill", BROWSER_PROCESS_NAME])
        print("Браузер закрыт из-за превышения времени.")
    except Exception as e:
        print(f"Ошибка закрытия браузера: {e}")

def one_loop():
    current_title = get_active_window_title()
    if current_title:
        current_title = current_title.lower()
        # Проверяем, содержит ли заголовок индикатор браузера (опционально)
        if BROWSER_PROCESS_NAME in current_title:
            for domain in restricted_domains:
                if domain in current_title:
                    restricted_domains[domain] += CHECK_INTERVAL
                else:
                    restricted_domains[domain] = max(0, restricted_domains[domain]-CHECK_INTERVAL)

                if restricted_domains[domain] > MAX_TIME_ON_SITE:
                    print(f"Время на сайте ({current_title}) превысило 5 минут. Закрываем.")
                    close_browser()
    time.sleep(CHECK_INTERVAL)
def main():
    while True:
        one_loop()

if __name__ == "__main__":
    print("Мониторинг запущен. Нажмите Ctrl+C для остановки.")
    main()


