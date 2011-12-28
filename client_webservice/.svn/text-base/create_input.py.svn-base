import MySQLdb

conn = MySQLdb.connect (host = "localhost",
                        user = "root",
                        passwd = "helloall",
                        db = "fydp_db")
cursor = conn.cursor ()
input = """INSERT INTO fydp_db.feeditem VALUES ('guid-%s', 'feedurl-%s', 'this is a huge string representing text-%s', 'title-%s', 'link-%s', 'author-%s', 'comments-%s', '01-%s-2010 12:00')"""
for i in range(2, 20):
	cursor.execute (input, [i]*8)
cursor.close ()
conn.close ()

