import sqlite3
import sys

            
def main():       
        try:
            state = 'ready'
            conn = sqlite3.connect('pwcrack.db')

            with conn:

                cur = conn.cursor()
                cur.execute("SELECT * FROM clients")
                rows = cur.fetchall()
                    
                for row in rows:
                    clientID = row[0]
                    cur.execute("UPDATE clients SET state=? WHERE clientID=?",(state, clientID))

        except sqlite3.Error, e:
            print "Error updateClient %s:" % e.args[0]
            sys.exit(1)

        finally:
            if conn:
                conn.close()


main()
