from flask import current_app
import json

class MoveDAO:
    @staticmethod
    def save(game_id, from_pos, to_pos, piece):
        db = current_app.get_db()
        cursor = db.execute(
            "INSERT INTO moves (game_id, from_pos, to_pos, piece) VALUES (?, ?, ?, ?)",
            (game_id, json.dumps(from_pos), json.dumps(to_pos), piece)
        )
        db.commit()
        return cursor.lastrowid
