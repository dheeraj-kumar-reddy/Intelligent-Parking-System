import sqlite3
conn=sqlite3.connect("parking.db")
c=conn.cursor()
c.execute("create table security(flat_number varchar(10),Name varchar(30),park_slot varchar(10),Mobile_no varchar(10))")
#c.execute("drop table security")
#c.execute("alter table security drop column Name")
#c.execute("delete from security where Name=='7382129046' ")
conn.commit()