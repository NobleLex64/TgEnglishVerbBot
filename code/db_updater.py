import aiosqlite
import sqlite3
from datetime       import datetime

from globals        import DB_PATH, VERBS_COUNT, LOG_PATH, ADMIN_ID
from help_functions import set_bit

## START DATABASE SEGMENT
# add new user in sqlite db
async def add_user_in_db(user_id: int, username: str) -> None:
  access = "new"
  if ADMIN_ID and user_id == int(ADMIN_ID): 
    access = "admin"

  async with aiosqlite.connect(DB_PATH) as conn:
    cursor = await conn.execute("SELECT id FROM users WHERE id = ?", (user_id,))
    row    = await cursor.fetchone()
    if not row :
      await conn.execute('''
                  INSERT INTO users (id, access, username, progress, data_last_update)
                  VALUES (?, ?, ?, ?, ?)
              ''', (
                  user_id,
                  access,
                  username, bytearray(VERBS_COUNT // 8),
                  datetime.now().strftime("%Y-%m-%d %H:%M:%S")
              )
      )
      await conn.commit()
    else:
      access = "student"
      if ADMIN_ID and user_id == int(ADMIN_ID): 
        access = "admin"

      async with aiosqlite.connect(DB_PATH) as conn:
        await conn.execute("UPDATE users SET data_last_update = ?, access = ? WHERE id = ?",
                           (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), access, user_id))
        await conn.commit()

# Update user progress
async def upd_usr_progress(user_id: int, verbs_id: str) -> None:
  async with aiosqlite.connect(DB_PATH) as conn:
    cursor   = await conn.execute("SELECT progress FROM users WHERE id = ?", (user_id,))
    row      = await cursor.fetchone()
    progress = bytearray(row[0])

    for verb_index in verbs_id:
      set_bit(progress, verb_index - 1)

    await conn.execute("UPDATE users SET progress = ? WHERE id = ?", (progress, user_id))
    await conn.commit()

# create log database
async def create_log_db() -> None: 
  async with aiosqlite.connect(LOG_PATH) as conn:
    cursor = await conn.execute('''
        CREATE TABLE IF NOT EXISTS logs (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            date       TEXT,
            user_id    INT,
            error_data TEXT    
        )
    ''')
    await conn.commit()
#
## END DATABASE SEGMENT