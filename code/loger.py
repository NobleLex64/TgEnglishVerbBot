import asyncio
import aiosqlite
from datetime import datetime

from globals    import LOG_PATH, LOGS_BUFFER
from db_updater import create_log_db

async def create_log(id: int, log: str) -> None:
  messages = []
  if LOGS_BUFFER.get(id) is not None:
    for message in LOGS_BUFFER[id]:
      messages.append(message)
  messages.append(log)
  LOGS_BUFFER[id] = messages

async def logs_init() -> None:
  await create_log_db()

async def write_log(message: str, user_id: str) -> None:
  async with aiosqlite.connect(LOG_PATH) as conn:
    cursor   = await conn.execute (
      "INSERT INTO logs (date, user_id, error_data) VALUES (?, ?, ?)",
      (
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 
        user_id, 
        message
      )
    )
    await conn.commit()

async def start_writing_log() -> None:
  await logs_init()
  while True:
    await asyncio.sleep(120) 
    for id, logs in LOGS_BUFFER.items():
      for log in logs:
        await write_log(log, id)
      LOGS_BUFFER[id] = []
