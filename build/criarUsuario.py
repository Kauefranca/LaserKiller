from werkzeug.security import generate_password_hash

import psycopg2

con = psycopg2.connect(
	host='localhost', 
	database='postgres', 
	port='5432',
	user='postgres', 
	password='postgres'
)

cur = con.cursor()

def createUserAdmin():
    sql = """INSERT INTO usuario(email, hash) VALUES ('admin@admin.com', %s);"""
    cur.execute(sql, (generate_password_hash('admin'),))
    con.commit()

createUserAdmin()
con.close()