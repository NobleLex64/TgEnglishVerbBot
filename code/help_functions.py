import aiosqlite

## Help function for progress command
# Put a bit on index -> void
def set_bit(progress, index) -> None:
  byte_index = index // 8
  bit_index  = index % 8
  progress[byte_index] |= (1 << bit_index)

# Check bit on index -> bool
def is_bit_set(progress, index) -> bool:
  byte_index = index // 8
  bit_index  = index % 8
  return (progress[byte_index] & (1 << bit_index)) != 0

# Get first 5 not learned verb index
def find_next_unlearned(progress, size) -> list:
    indexes = []
    for i in range(0, len(progress) * 8):
        if not is_bit_set(progress, i):
            indexes.append(i + 1)
            if len(indexes) == size:
                break
    return indexes
#
## end function

## Help function for echo command
async def search_present_simple(verb: str, db_name: str) -> None | str:
    async with aiosqlite.connect(db_name) as conn:
        cursor = await conn.execute("SELECT id, base_form FROM verbs")
        verbs  = await cursor.fetchall()

        for v in verbs:
            if v[1].startswith(verb):
                return v[0]
    return None

async def search_past_simple(verb: str, db_name: str) -> None | str:
    async with aiosqlite.connect(db_name) as conn:
        cursor = await conn.execute("SELECT id, past_simple FROM verbs")
        row    = await cursor.fetchall()

        for id, verbs in row:
            parts = verbs.split(" ") # parts[0] = verbs, parts[1] = transcriptions
            part  = parts[0].split("/")
            if part[0] == verb or (len(part) > 1 and part[1] == verb):
                return id
    return None

async def search_past_participle(verb: str, db_name: str) -> None | str:
    async with aiosqlite.connect(db_name) as conn:
        cursor = await conn.execute("SELECT id, past_participle FROM verbs")
        row    = await cursor.fetchall()

        for id, verbs in row:
            parts = verbs.split(" ")  # parts[0] = verbs, parts[1] = transcriptions
            part = parts[0].split("/")
            if part[0] == verb or (len(part) > 1 and part[1] == verb):
                return id
    return None
## end Search