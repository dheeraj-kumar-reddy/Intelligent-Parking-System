from cProfile import label
from tkinter import *
import tkinter
from tkinter.font import Font
import os
from pydrive2.drive import GoogleDrive
from pydrive2.auth import GoogleAuth
from qrcode import *
import qrcode
import sqlite3
import pandas as pd
t=Tk()
e1=StringVar()
e2=StringVar()
e3=StringVar()
e4=StringVar()
gauth=GoogleAuth()
gauth.LocalWebserverAuth()	
drive=GoogleDrive(gauth)
conn=sqlite3.connect('parking.db')
c=conn.cursor()
#c.execute("create table t_data(flat_no varchar(10),park_slot varchar(10),Available varchar(1))")
def addNewSlot():
    t1=Tk()
    t1.title("New User Application")
    Label(t1,text="Enter Vehicle Number : ").grid(row=0,column=0)
    e1=Entry(t1, width=50, borderwidth=5)
    e1.grid(row=0,column=1)
    Label(t1,text=" ").grid(row=1,column=0,columnspan=2)
    Label(t1,text="Enter Owner Full Name : ").grid(row=2,column=0)
    e2=Entry(t1, width=50, borderwidth=5)
    e2.grid(row=2,column=1)
    Label(t1,text=" ").grid(row=3,column=0,columnspan=2)
    Label(t1,text="Enter Mobile Number : ").grid(row=4,column=0)
    e3=Entry(t1, width=50, borderwidth=5)
    e3.grid(row=4,column=1)
    Label(t1,text=" ").grid(row=5,column=0,columnspan=2)
    Label(t1,text="Select Flat Number : ").grid(row=6,column=0)
    l=c.execute("select flat_no from t_data where Available=='1';")
    a=[]
    for i in l:
        a.append(i)
    val=tkinter.StringVar(t1)
    val.set("Select the flat no.       ")
    o=OptionMenu(t1,val,*a)
    o.grid(row=6,column=1)
    def print_val():
        s=val.get()[2:7]
        jk=c.execute("SELECT park_slot FROM t_data WHERE flat_no==?;",[s])
        for i in jk:
            e5=str(i)[2:6]
        c.execute("update t_data set Available='0' where flat_no==?",[s])
        c.execute("insert into security values(:flat_number,:Name,:park_slot,:Mobile_no)",{
        'flat_number':s,
        'Name':e2.get(),
        'park_slot':e5,
        'Mobile_no':e3.get(),        
        })
        conn.commit()
        return e5
    Label(t1,text=" ").grid(row=9,column=0,columnspan=2)
    Label(t1,text="Allocated Parking Slot : ").grid(row=10,column=0)
    def click():
        str1=print_val()
        Label(t1,text=str1).grid(row=10,column=1)
        path=r"/media/dheeraj/DHEERAJ/ENGINEERING DOCUMENTS/SEM 5/MACHINE LEARNING/Mini Project/data"
        os.chdir(path)
        file_name='{}.txt'.format(e1.get())
        f=open(file_name,"w")
        f.write("\t\t\t\t\t\t\tSAI PARKING SOLUTIONS\n")
        f.write("Vehicle Number : {}\n".format(e1.get()))
        f.write("Owner Name : {}\n".format(e2.get()))
        #f.write("Mobile Number : {}\n".format(e3.get()))
        f.write("Flat No. : {}\n".format(val.get()[2:7]))
        f.write("Allotted Parking Slot : {}\n".format(str1))
        f.write("Contact Security @ 799 308 0020 for contact details")
        f.close()
        f1=drive.CreateFile({'title': file_name})
        f1.SetContentFile(os.path.join(path, file_name))
        f1.Upload()
        f1.InsertPermission({
            'type':'anyone',
            'value':'anyone',
            'role':'reader'
        })
        qr=qrcode.QRCode(version=1,box_size=40,border=3)
        qr.add_data(f1['alternateLink'])
        qr.make(fit=True)
        generate_image=qr.make_image(fill_color='black',back_color='white')
        generate_image.save('{0}.png'.format(str1))
        f1=None
        Label(t1,text="No more data to be added... close the window").grid(row=13,column=0,columnspan=2)
    Label(t1,text=" ").grid(row=11,column=0,columnspan=2)
    Button(t1,text="Submit", command=click).grid(row=12,column=0,columnspan=2)
    t1.mainloop()
def updateSlot():
    t2=Tk()
    t2.title("Delete/Update slot")
    Label(t2,text="In order to update a slot, delete it and Add it again!!!").grid(row=0,column=0,columnspan=2)
    Label(t2,text=" ").grid(row=1,column=0,columnspan=2)
    Label(t2,text="Select Flat Number : ").grid(row=2,column=0)
    l=c.execute("select flat_no from t_data where Available=='0';")
    a=[]
    for i in l:
        a.append(i)
    val=tkinter.StringVar(t2)
    val.set("Select the flat no.       ")
    o=OptionMenu(t2,val,*a)
    o.grid(row=2,column=1)
    def delete():
        park=""
        s=val.get()[2:7]
        jk=c.execute("SELECT park_slot FROM t_data WHERE flat_no==?;",[s])
        for i in jk:
            park+=str(i)[2:6]
        c.execute("update t_data set Available='1' where flat_no==?",[s])
        c.execute("delete from security where park_slot==?",[park])
        conn.commit()
        t2.destroy()
    Label(t2,text=" ").grid(row=3,column=0,columnspan=2)
    Button(t2,text="Delete",command=delete).grid(row=4,column=0,columnspan=2)
def reports():
    c.execute("select * from security")
    path=r"/media/dheeraj/DHEERAJ/ENGINEERING DOCUMENTS/SEM 5/MACHINE LEARNING/Mini Project/reports"
    os.chdir(path)
    f=open('security_data.csv','w')
    while True:
        df = pd.DataFrame(c.fetchmany(1000))
        if len(df) == 0:
            break
        else:
            df.to_csv(f, header=["Flat Number","Name","Parking Slot","Mobile Number"], index=True)
    f.close()
    Label(t,text="Report generation successful").pack()
def exitWindow():
    t.destroy()
t.title("Home Page")
t.maxsize(width=1500,height=1500)
fontstyle=Font(family="Times New Roman",size=25)
Label(t,text="Welcome to Parking Management System using QR Code", font=fontstyle).pack()
Label(t,text=" ").pack()
fontstyle=Font(family="Times New Roman",size=14)
Button(t,text="Add New Slot",height=3, width=30,font=fontstyle, command=addNewSlot).pack()
Label(t,text=" ").pack()
Button(t,text="Delete/Update Slot",height=3, width=30, font=fontstyle, command=updateSlot).pack()
Label(t,text=" ").pack()
Button(t,text="Generate Reports",height=3, width=30, font=fontstyle, command=reports).pack()
Label(t,text=" ").pack()
Button(t,text="Exit",height=3, width=30, font=fontstyle, command=exitWindow).pack()
Label(t,text="  ").pack()
t.mainloop()