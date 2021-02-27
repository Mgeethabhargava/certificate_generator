import sqlite3

conn = sqlite3.connect('database.db')
print("Opened database successfully")

conn.execute('CREATE TABLE SIGNUPLIST(FULLNAME  TEXT  NOT NULL,USERNAME  TEXT  NOT NULL,EMAILID  CHAR(50) NOT NULL,ACCOUNTTYPE  TEXT  NOT NULL,CONTACTNO   INT(50) NOT NULL,PASSWORD   CHAR(50) NOT NULL)')

conn.execute('CREATE TABLE IF NOT EXISTS certificateissuelist(fullname text NOT NULL,registeredno text PRIMARY KEY,coursename text NOT NULL,courseyear text NOT NULL,specialization text NOT NULL,joiningyear text NOT NULL,courseduration text NOT NULL,  emailid text NOT NULL)')

print("Table created successfully")
conn.close()