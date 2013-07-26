# -*- coding: cp1252 -*-
import sys, os, sqlite3

def createBFtable(hashName):
    hashName = ''.join(hashName.split('-'))
    tableName = hashName+'bftable'
    
    charset1 = "a~`!@#$%^&*()_-+=[]{}\\|<>\"\':;,.\? /"
    #charset2 = u"abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890~`!@#$%^&*()_-+=[]{}\\|<>\"\':;,.\? /\ñ"
    
    charset = 'charset1'
    #charset = 'charset2'

    bftable = []
    for char in charset1:
        bftable.append( (char, charset, 'incomplete') )
        
    try:
        conn = sqlite3.connect('TBFTable.db')

        with conn:
            cur = conn.cursor()

            #result = cur.execute("SELECT 1 FROM %s" % tableName )
            #print result
            
            #BruteForce Table. Start=one char for client to start on. charset full charset.
            #status can be incomplete, inprogress, completed
            #commented this out to preserv database across starts.
            #cur.execute("DROP TABLE IF EXISTS %s" % tableName)
            cur.execute('''CREATE TABLE IF NOT EXISTS %s
                         (start text, charset text, status text)''' % tableName)    

            cur.executemany("INSERT INTO "+tableName+" VALUES(?, ?, ?)", bftable)

    except sqlite3.Error, e:
        print "Error create bf table %s:" % e.args[0]
        sys.exit(1)

    finally:
        if conn:
            conn.close()

hashName = 'raw-md5'
createBFtable(hashName)
