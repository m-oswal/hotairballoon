import mysql.connector as msc
db= msc.connect(host='127.0.0.1',
                user='your_user_name',
                password='your_password')
cursor = db.cursor()

cursor.execute('create database hotairballoon ;')

cursor.execute('use hotairballoon;')

cursor.execute('create table players (USERNAME VARCHAR(20) PRIMARY KEY,PASSWORD varchar(20) , SCORE INT) ; ')

cursor.execute('insert into players values("MOKSH12","your_user_name100",325),("DISHA11","CD123",495),("KRISH","ABCD12@",987),'
               '("15AAROHI","1918IND",900),("DEV1","WIN1@",988),("K@H@N","2004",300);')

cursor.execute('create table log(username varchar(20));')
db.commit()

db.close()


