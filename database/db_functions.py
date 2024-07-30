import sqlite3


def create_db():
    conn = sqlite3.connect("translate-db.sqlite")
    cur = conn.cursor()

    # Create the 'text_history' table if it doesn't exist
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS text_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            original_text TEXT,
            translated_text TEXT
        )
    """
    )

    conn.commit()
    conn.close()
    # Return a success message or a boolean indicating success
    return "Database created successfully"


def update_user(user_id, original_text, translated_text):
    conn = sqlite3.connect("translate-db.sqlite")
    cur = conn.cursor()

    # Insert a new text history record
    cur.execute(
        "INSERT INTO text_history (user_id, original_text, translated_text) VALUES (?, ?, ?)",
        (user_id, original_text, translated_text),
    )

    conn.commit()
    conn.close()
    return "User history updated successfully"


def get_user_history(user_id):
    conn = sqlite3.connect("translate-db.sqlite")
    cur = conn.cursor()

    cur.execute(
        "SELECT original_text, translated_text FROM text_history WHERE user_id = ?",
        (user_id,),
    )
    history = [
        {"original_text": row[0], "translated_text": row[1]} for row in cur.fetchall()
    ]

    conn.close()
    return history


def delete_user_history(user_id):
    conn = sqlite3.connect("translate-db.sqlite")
    cur = conn.cursor()

    # Delete records for the user and get the count of deleted records
    cur.execute("DELETE FROM text_history WHERE user_id = ?", (user_id,))
    deleted_count = cur.rowcount

    conn.commit()
    conn.close()

    return deleted_count
