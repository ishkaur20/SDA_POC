import mysql.connector


mydb = mysql.connector.connect(
  host="localhost",
  user="labadmin",
  password="C1sco12345",
  database="domains"
)

mycursor = mydb.cursor()


join = "SELECT * FROM domainInfo NATURAL JOIN snapshotInfo;"
mycursor.execute(join)
print(mycursor.fetchall())

