import sqlite3
import sys

            
def main():
	hashName = 'rawmd5'       
  	tableName = hashName+'ruleTable'
        try:
            state = 'ready'
            conn = sqlite3.connect('RuleTable.db')

            with conn:

                cur = conn.cursor()
                cur.execute("SELECT * FROM %s" % tableName)
                rows = cur.fetchall()
                    
                for row in rows:
                    print row

        except sqlite3.Error, e:
            print "Error updateClient %s:" % e.args[0]
            sys.exit(1)

        finally:
            if conn:
                conn.close()


main()
