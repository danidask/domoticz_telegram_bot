from botdb import *
from sys import argv

db = BotDb()

nopermission = list(set(db._allusers) - set(db._okusers))

if len(nopermission) < 1:
    print("No registers without permission")
    quit()

if len(argv) < 2:
    for id, chatid in enumerate(nopermission):
        print("ID {}\tchat number: {}".format(id+1, chatid))
    print ("add id numbers for give permission to those users\n"
           "example 'python3 {} 3 5' for ID 3 and ID 5".format(argv[0]))
else:
    for i in argv[1:]:
        index = int(i)-1
        chatid = nopermission[index]
        db.give_permission(chatid)
        print("Permission granted for ", chatid)
