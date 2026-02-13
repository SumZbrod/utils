#!/bin/bash
set -euo pipefail

# --- поиск всех клавиатур и всех указателей в XInput ---
readarray -t KEY_IDS < <(xinput list --short | awk -F'id=' '/keyboard/ {print $2}' | awk '{print $1}')
readarray -t PTR_IDS < <(xinput list --short | awk -F'id=' '/pointer/  {print $2}' | awk '{print $1}')

# --- функция возврата устройств и экрана (на случай выхода/ошибки) ---
restore() {
  for id in "${KEY_IDS[@]}"; do xinput --enable "$id" 2>/dev/null || true; done
  for id in "${PTR_IDS[@]}"; do xinput --enable "$id" 2>/dev/null || true; done
  xset dpms force on 2>/dev/null || true
}
trap restore EXIT

# --- отключаем ввод ---
for id in "${KEY_IDS[@]}"; do xinput --disable "$id"; done
for id in "${PTR_IDS[@]}"; do xinput --disable "$id"; done

# --- гасим экран DPMS'ом ---
xset dpms force off

# --- ждём 5 секунд (можно менять) ---
sleep 5

# --- включаем экран и возвращаем ввод ---
xset dpms force on
for id in "${KEY_IDS[@]}"; do xinput --enable "$id"; done
for id in "${PTR_IDS[@]}"; do xinput --enable "$id"; done
trap - EXIT
