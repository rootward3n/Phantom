"""
memory.py
Phantom Memory Engine
"""

from database import JsonDatabase


class Memory:

    def __init__(self):
        self.db = JsonDatabase("memory.json")

    def remember(self, key: str, value: str):
        """
        Save a memory.
        """

        data = self.db.load()

        data[key] = value

        self.db.save(data)

    def recall(self, key: str):

        data = self.db.load()

        return data.get(key)

    def forget(self, key: str):

        data = self.db.load()

        if key in data:
            del data[key]
            self.db.save(data)

            return True

        return False

    def all(self):

        return self.db.load()

    def clear(self):

        self.db.clear()

    def count(self):

        return len(self.db.load())
