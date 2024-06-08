# TODO Fazer com que este arquivo utilize o objeto do ..\sources\postgres.py

from werkzeug.security import generate_password_hash
import psycopg2

con = psycopg2.connect(
	host='localhost', 
	database='unimar', 
	port='5432',
	user='postgres', 
	password='postgres'
)

cur = con.cursor()

sql = "CREATE TABLE IF NOT EXISTS registro(id SERIAL NOT NULL UNIQUE PRIMARY KEY, data TIMESTAMP, qntErvasDetec INT NOT NULL, porcErvasDetectadas INT NOT NULL, situacao VARCHAR(8), risco VARCHAR(8));"
cur.execute(sql)
con.commit()

sql = "CREATE TABLE IF NOT EXISTS usuario(id_usuario SERIAL NOT NULL UNIQUE PRIMARY KEY, email VARCHAR(50) NOT NULL, hash TEXT NOT NULL);"
cur.execute(sql)
con.commit()

def createUserAdmin():
    sql = """INSERT INTO usuario(email, hash) VALUES ('admin@admin.com', %s);"""
    cur.execute(sql, (generate_password_hash('admin'),))
    con.commit()

createUserAdmin()
con.close()