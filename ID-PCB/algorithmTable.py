#LOTS OF WORK TO BE DONE HERE!!!!!  ONLY ADD WHAT THEY HAD LAST YEAR.
import sys
import sqlite3

def main():
#algorithm, hashFile, mcode, AMDaccel, AMDloops, NVaccel, NVloops
    

    hashtypes = (
        ('raw-md5', 'hashes/raw-md5.hash', '-m 0', '-n 256', '-u 1024', '-n 256', '-u 1024'),
        ('raw-md5u', 'hashes/raw-md5u.hash', '-m 30', '-n 256', '-u 1024', '-n 256', '-u 1024'),
        ('raw-sha1', 'hashes/raw-sha1.hash', '-m 100', '-n 256', '-u 1024', '-n 256', '-u 1024'),
        ('mysql-sha1', 'hashes/mysql-sha1.hash', '-m 300', '-n 256', '-u 1024', '-n 256', '-u 1024'),
        ('nsldap', 'hashes/nsldap.hash', '-m 101', '-n 256', '-u 1000', '-n 256', '-u 1000'),
        ('raw-md4', 'hashes/raw-md4.hash', '-m 900', '-n 160', '-u 1024', '-n 160', '-u 1024'),
        ('ntlm', 'hashes/ntlm.hash', '-m 1000', '-n 160', '-u 1024', '-n 160', '-u 1024'),
)
    try:
    
        conn = sqlite3.connect('algorithm.db')

        with conn:

            cur = conn.cursor()

            cur.execute("DROP TABLE IF EXISTS algorithms")
            cur.execute('''CREATE TABLE IF NOT EXISTS algorithms
                         (algorithm text, hashFile text, mcode text, AMDaccel text, AMDloops text, NVaccel text, NVloops text)''')
            cur.executemany("INSERT INTO algorithms VALUES(?, ?, ? , ?, ?, ?, ?)", hashtypes)

    except sqlite3.Error, e:
        print "Error %s:" % e.args[0]
        sys.exit(1)

    finally:
        if conn:
            conn.close()
            
main()
