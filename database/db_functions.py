import aiosqlite


async def create_db():
    async with aiosqlite.connect("translate-db.sqlite") as conn:
        await conn.execute(
            """
            CREATE TABLE IF NOT EXISTS text_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                original_text TEXT,
                translated_text TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        await conn.commit()
    return "Database created successfully"


async def update_user(user_id, original_text, translated_text):
    async with aiosqlite.connect("translate-db.sqlite") as conn:
        await conn.execute(
            "INSERT INTO text_history (user_id, original_text, translated_text) VALUES (?, ?, ?)",
            (user_id, original_text, translated_text),
        )
        await conn.commit()
    return "User history updated successfully"


async def get_user_history(user_id):
    async with aiosqlite.connect("translate-db.sqlite") as conn:
        async with conn.execute(
            "SELECT original_text, translated_text, created_at FROM text_history WHERE user_id = ?",
            (user_id,),
        ) as cursor:
            history = [
                {
                    "original_text": row[0],
                    "translated_text": row[1],
                    "created_at": row[2],
                }
                for row in await cursor.fetchall()
            ]
    return history


async def get_user_history_dates(user_id):
    async with aiosqlite.connect("translate-db.sqlite") as conn:
        async with conn.execute(
            "SELECT DISTINCT DATE(created_at) FROM text_history WHERE user_id = ? LIMIT 10",
            (user_id,),
        ) as cursor:
            dates = [row[0] for row in await cursor.fetchall()]
    return dates


async def get_user_history_by_date(user_id, date):
    async with aiosqlite.connect("translate-db.sqlite") as conn:
        async with conn.execute(
            "SELECT original_text, translated_text, created_at FROM text_history WHERE user_id = ? AND DATE(created_at) = ?",
            (user_id, date),
        ) as cursor:
            history = [
                {
                    "original_text": row[0],
                    "translated_text": row[1],
                    "created_at": row[2],
                }
                for row in await cursor.fetchall()
            ]
    return history


async def delete_user_history(user_id):
    async with aiosqlite.connect("translate-db.sqlite") as conn:
        await conn.execute(
            "DELETE FROM text_history WHERE user_id = ?",
            (user_id,),
        )
        await conn.commit()
    return "User history deleted successfully"
