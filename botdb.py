import sqlite3
from datetime import datetime
from time import time


class BotDb:
    # TODO change prints for logs
    _okusers = []
    _allusers = []

    def __init__(self, filename=None):
        if filename:
            self.filename = filename
        else:
            self.filename = 'bot.sqlite'
        self._open()
        self._create_table() # Only if it doesnt exist
        self._read_all_users()
        self._read_allaw_users()
        self._close()
        if len(self._allusers) == 0:
            print("Empty database. First user will be added as administrator")


    def _create_table(self):
        # date as YYYY-MM-DD HH:MM:SS
        self.c.execute("CREATE TABLE IF NOT EXISTS users('ID' INTEGER PRIMARY KEY, "
                       "'chat_id' NUMERIC, 'name' TEXT, 'permission' INTEGER DEFAULT 0, 'first_seen' TEXT)")


    def add_user(self, chatid, name, permission=False):
        #If database is empty, add the first user as administrator
        if len(self._allusers) == 0:
            permission = True  # If its the first, give permission
        # Check if already exists
        if chatid in self._allusers:
            return
        self._open()
        # TODO real date
        fsdate = '2017-01-11 13:53:39'
        if permission:
            permission = 1
        else:
            permission = 0
        self.c.execute("INSERT INTO users ('chat_id', 'name', 'permission', 'first_seen') "
                        "VALUES({}, '{}', {}, '{}')".format(chatid, name, permission, fsdate))

        self.conn.commit()
        self._close()
        self._allusers.append(chatid)
        if permission:
            self._okusers.append(chatid)
        print("New register added: chat_id {}, name {}, permission {}, first_seen {}".format(chatid, name, permission, fsdate))


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
        if chatid in self._okusers:
            return True
        return False

    def _open(self):
        self.conn = sqlite3.connect(self.filename)
        self.c = self.conn.cursor()

    def _close(self):
        self.c.close()
        self.conn.close()

    def give_permission(self, chatid):
        sqq = "UPDATE users SET permission = 1 WHERE chat_id = {}".format(chatid)
        self._open()
        self.c.execute(sqq)
        self.conn.commit()
        self._close()
