"""
history.py
Conversation history manager.
"""

from database import JsonDatabase


class History:

    def __init__(self):
        self.db = JsonDatabase("history.json")

    def add(self, role: str, message: str):
        data = self.db.load()

        history = data.get("history", [])

        history.append({
            "role": role,
            "message": message
        })

        data["history"] = history

        self.db.save(data)

    def get_all(self):
        data = self.db.load()
        return data.get("history", [])

    def last(self, count: int = 10):
        return self.get_all()[-count:]

    def clear(self):
        self.db.save({"history": []})

    def count(self):
        return len(self.get_all())
