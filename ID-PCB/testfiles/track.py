import string, sys, os, re, sqlite3

def main(clientID, status, foundCount):

    try:

        conn = sqlite3.connect('pwcrack.db')

        with conn:

            cur = conn.cursor()

            cur.execute("UPDATE completed SET status=?,foundCount=? WHERE clientID=? AND status='working'", (status, foundCount, clientID))



    except sqlite3.Error, e:
        print "Error updating completed %s:" % e.args[0]
        sys.exit(1)

    finally:
        if conn:
            conn.close()


ClientID = 'CID_9150_734'
status = 'completed'
foundCount = '50'

main(ClientID, status, foundCount)
