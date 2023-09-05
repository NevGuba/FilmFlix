import sqlite3 as sql 

dbCon = sql.connect("PythonProject/filmflix.db")

dbCursor = dbCon.cursor()