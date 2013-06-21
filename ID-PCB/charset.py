# -*- coding: cp1252 -*-
#teesting to make bftable

import sqlite3

charset = u"abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890~`!@#$%^&*()_-+=[]{}\\|<>\"\':;,.? /ñ"

bftable = []

for char in charset:
    bftable.append( (char, charset) )

       
conn = sqlite3.connect('bftable.db')
cur = conn.cursor()

with conn:
    #BruteForce Table. Start=one char for client to start on. charset full charset 
    cur.execute('''CREATE TABLE IF NOT EXISTS bftable
                 (start text, charset text)''')    

    cur.executemany("INSERT INTO bftable VALUES(?, ?)", bftable)



