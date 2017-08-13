from botdb import *
from sys import argv

db = BotDb()

if len(argv) < 2:
    for id, chatid in enumerate(db._allusers):
        print("ID {}\tchat number: {}".format(id+1, chatid))
    print ("add id numbers for give permission to those users\n"
           "example 'python3 {} 3 5' for ID 3 and ID 5".format(argv[0]))
else:
    for i in argv[1:]:
        index = int(i)-1
        db.give_permission(db._allusers[index])
