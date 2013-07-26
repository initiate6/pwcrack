import re
import sqlite3
import sys

def bfupdate(hashName, bfstart, status):
    hashName = ''.join(hashName.split('-'))
    tableName = hashName+'bftable'
    try:
        conn = sqlite3.connect('TBFTable.db')

        with conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM %s" % tableName)
            rows = cur.fetchall()

            for row in rows:
                #testChar = row[0].encode('ascii')
                if re.match(re.escape(bfstart),row[0]):
                    cur.execute("UPDATE "+tableName+" SET status=? WHERE start=?",(status, bfstart))
                    print row

                    conn.commit()
    except sqlite3.Error, e:
        print "Error bfupdate %s:" % e.args[0]
        sys.exit(1)

    finally:
        if conn:
            conn.close()


hashName = 'raw-md5'
bfstart = '$'
status = 'inprogress'

bfupdate(hashName, bfstart, status)
