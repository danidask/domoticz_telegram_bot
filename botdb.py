import sqlite3
from datetime import datetime
from time import time


class BotDb:
    # TODO change prints for logs
    _okusers = []
    _allusers = []

    def __init__(self):
        self._open()
        self._create_table() # Only if it doesnt exist
        self._read_all_users()
        self._read_allaw_users()
        self._close()

    def _create_table(self):
        # date as YYYY-MM-DD HH:MM:SS
        self.c.execute("CREATE TABLE IF NOT EXISTS users('ID' INTEGER PRIMARY KEY, "
                       "'chat_id' NUMERIC, 'name' TEXT, 'permission' INTEGER DEFAULT 0, 'first_seen' TEXT)")

    def add_user(self, chatid, name):
        # Check if already exists
        for id in self._allusers:
            if id == chatid:
                return
        self._open()
        # TODO real date
        fsdate = '2017-01-11 13:53:39'
        self.c.execute("INSERT INTO users ('chat_id', 'name', 'first_seen') "
                       "VALUES({}, '{}', '{}')".format(chatid, name, fsdate))
        self.conn.commit()
        self._close()
        self._allusers.append(chatid)
        print("New register added: chat_id {}, name {}, first_seen {}".format(chatid, name, fsdate))

    def _read_all_users(self):
        self.c.execute("SELECT chat_id FROM users")
        data = self.c.fetchall()
        for field in data:
            self._allusers.append(field[0])

    def _read_allaw_users(self):
        self.c.execute("SELECT chat_id FROM users WHERE permission>0")
        data = self.c.fetchall()
        for field in data:
            self._okusers.append(field[0])

    def userallowed(self, chatid):
        """Return True if the chatid is in the database with the 'permission' flag
        False otherwise"""
        # TODO can be done with if chatid in dbid
        for dbid in self._okusers:
            if dbid == chatid:
                return True
        return False

    def _open(self):
        self.conn = sqlite3.connect('bot.sqlite')
        self.c = self.conn.cursor()

    def _close(self):
        self.c.close()
        self.conn.close()
