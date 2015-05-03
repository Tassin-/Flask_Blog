#sql.py - CREATE a SQLite3 table and populate it with data

import sqlite3

#create a new database
with sqlite3.connect("blog.db") as connection:
	c = connection.cursor()

	#Create table
	c.execute("""CREATE TABLE posts(title TEXT, post TEXT)""")

	#Insert dummy data into the table
	c.execute('INSERT INTO posts VALUES("Good", "I\im good.")')
	c.execute('INSERT INTO posts VALUES("Well", "I\'m well.")')
	c.execute('INSERT INTO posts VALUES("Excellent", "I\'m excellent.")')
	c.execute('INSERT INTO posts VALUES("Okay", "I\'m okay")')