#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import asyncio
import logging
from datetime import datetime, timezone
from telethon import TelegramClient
from telethon.tl.types import InputPeerChannel
from dotenv import load_dotenv
import subprocess

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)-7s | %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger("TG-Watchdog")

# Загружаем переменные окружения
load_dotenv()

API_ID = int(os.getenv("TG_API_ID", "0"))
API_HASH = os.getenv("TG_API_HASH", "")
CHANNEL_ID = int(os.getenv("TG_CHANNEL_ID", "0"))

CHECK_INTERVAL = 300          # каждые 5 минут проверяем
MAX_SILENCE_MINUTES = 30      # если тишина больше этого → перезагрузка

if API_ID == 0 or not API_HASH or CHANNEL_ID == 0:
    logger.error("Не заданы TG_API_ID, TG_API_HASH или TG_CHANNEL_ID в .env")
    exit(1)


async def get_last_message_date(client, channel_id: int):
    try:
        # Для приватных/публичных каналов лучше использовать entity
        entity = await client.get_entity(channel_id)
        
        # Берём самое последнее сообщение
        async for message in client.iter_messages(entity, limit=1):
            if message.date:
                # date уже в UTC
                return message.date
        return None
    except Exception as e:
        logger.error(f"Ошибка при получении последнего сообщения: {e}")
        return None


async def main():
    logger.info("Запуск Telegram Watchdog")
    logger.info(f"Мониторим канал {CHANNEL_ID} | тишина > {MAX_SILENCE_MINUTES} мин → reboot")

    client = TelegramClient("/home/user/Files/utils/session.session", API_ID, API_HASH)
    trysef = 0
    async with client:
        while True:
            last_msg_date = await get_last_message_date(client, CHANNEL_ID)

            if last_msg_date is None:
                logger.warning("Не удалось получить дату последнего сообщения")
            else:
                now = datetime.now(timezone.utc)
                minutes_silent = (now - last_msg_date).total_seconds() / 60

                logger.info(f"Последнее сообщение: {last_msg_date} UTC → прошло {minutes_silent:.1f} мин")

                if minutes_silent > MAX_SILENCE_MINUTES:
                    trysef += 1
                    if trysef > 1:
                        logger.error(f"!!! Тишина {minutes_silent:.1f} мин → перезагрузка сервера")
                        subprocess.run(["systemctl", "--user", "restart", "tg-screenshot.service"])
                        trysef = 1
                    else:
                        logger.error(f"!!! Тишина {minutes_silent:.1f} мин → если она продолжится то через 5 минут перезагрузка")
                    # После этой команды система перезагрузится, цикл дальше не пойдёт
                else:
                    trysef = 0

            await asyncio.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Остановка по Ctrl+C")
    except Exception as e:
        logger.exception("Критическая ошибка в главном цикле")