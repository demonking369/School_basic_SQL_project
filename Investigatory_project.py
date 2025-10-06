import tkinter as tk 
import mysql.connector as sql
from tkinter import ttk 
import subprocess as sub
import sys, re
mycon = None
database1= None
Table1= None
button_frame = None

def sql_connected(): # Secure login system 
    global mycon
    pas=enter.get()
    user=enter1.get()
    if user == (''): #Default
        user1='root' 
    try:
        mycon = sql.connect(host="localhost",user=user1,password=pas)
    except:
        lable1.config(text='Not Connected!(Wrong Pasword/UserName)',fg='Red')
    if mycon.is_connected() or pas.lower()=='q':
        lable1.config(text='Connected!',fg="Green")
        root.destroy()
        database()

def database():
    global mycon
    global button_frame
    global dash
    global c
    cur = mycon.cursor()
    try:
        dtw.destroy()
    except:
        print('Currently no window open')
    def refresh():
        dash.destroy()
        database()
    c=list(cur.execute("show Databases;") or cur.fetchall())
    c= [row[0] for row in c]
    dash = tk.Tk()
    dash.geometry('800x600')
    dash.title('Database')
    menubar = tk.Menu(dash)
    filemenu = tk.Menu(menubar,tearoff=0)
    filemenu.add_command(label='Exit',command=dash.destroy)
    filemenu.add_command(label='Refresh',command=refresh)
    menubar.add_cascade(label='File',menu=filemenu)
    dash.config(menu=menubar)
    tk.Label(dash,text='Select the database:',font=("Arial",12)).pack(padx=20)
    button_frame = tk.Frame(dash)
    button_frame.pack(fill="both", expand=True)
    buten_frame1 = tk.Frame(dash).pack(side='bottom', fill= 'x' , padx= 10, pady=10)
    tk.Button(buten_frame1,text='+ Add New DataBase.',fg='Green',command=lambda:database_manipulation_Window(1)).pack(side='right',padx=5)
    tk.Button(buten_frame1,text='- Remove Database.',fg='Red',command=lambda:database_manipulation_Window(2)).pack(side='right',padx=5)
    build_buttons(c)
    
def database_manipulation_Window(x):
    global mycon
    curser = mycon.cursor()
    global temp
    if x == 1:
        add=tk.Toplevel(dash)
        add.geometry('600x300')
        add.title('Adding The DataBase!')
        temp=tk.Label(add,text='')
        temp.pack(pady=20)
        tk.Label(add,text='Ente The Name of the new DataBase!').pack(side='top')
        name = tk.Entry(add)
        name.pack(pady=2)
        tk.Button(add,text="+ Add",fg='Green',command=lambda ent=name:Database_executor(x,ent)).pack(padx=20)
        
    elif x == 2:
        add = tk.Toplevel(dash)
        add.geometry('600x300')
        add.title('Removing database!')
        temp=tk.Label(add,text='')
        temp.pack(pady=20)
        tk.Label(add,text='Write the name of the database you want to remove.').pack(side='top')
        name = tk.Entry(add)
        name.pack(padx=20)
        tk.Button(add,text="- Remove",fg='Red',command=lambda ent = name:Database_executor(x,ent)).pack(padx=20)
        
def Database_executor(x,name):
    global mycon
    global temp
    curser = mycon.cursor()
    entered_name=name.get().strip()
    if x == 1:
        try:
            curser.execute(f'Create database {entered_name};')
            temp.config(text='New table added successfully Please refresh to see the change in the database',fg='Green')
        except:
            temp.config(text=' May be name is already taken Please check again and make sure name do not already exist in database.',fg='Red')
    elif x == 2 :
        try:
            curser.execute(f'Drop Database {entered_name}')
            temp.config(text=f'Successfully remove the database:{entered_name}',fg='Green')
        except:
            temp.config(text=' No such database found(Check the spelling once again)')

def build_buttons(student_list):
    global button_frame
    for name in student_list:
        btn = tk.Button(button_frame, text=name, width=20,
                        command=lambda n=name: table(n))
        btn.pack(pady=5)
        
def table(name):
    print(name)
    dash.destroy()
    global mycon
    global bf
    global dtw
    global c
    def refresh():
        dtw.destroy()
        table(name)
    cursor = mycon.cursor()
    cursor.execute(f'use {name};')
    all_tabels = list(cursor.execute("show Tables;") or cursor.fetchall())
    all_tabels = [row[0] for row in all_tabels]
    def on_click1(n):
        print(n)
    def build_buttons1(s):
        global bf
        for name in s:
            btn = tk.Button(bf, text=name, width=20,
                            command=lambda n=name: on_click1(n))
            btn.pack(pady=5)
            
    def table_executor(x,name=None):
        global mycon
        global temp1
        curser = mycon.cursor()
        if x == 1:
            try:
                #curser.execute(f'Create database {entered_name};')
                result = sub.run([sys.executable,'test.py'],capture_output=True,text=True, timeout=300)
                stderr = result.stderr.strip()
                output = result.stdout.strip()
                print("Return code:", output)
                if result.returncode != 0:
                    print("GUI exited with error, rc:", result.returncode)
                    print("stderr:", stderr)
                else:
                    print("GUI produced:")
                    print(result.stdout)
                    curser.execute(f'Use {name};')
                    curser.execute(result.stderr)   # this is the SQL or custom query
                
            except:
                temp1.config(text=' May be name is already taken Please check again and make sure name do not already exist in database.',fg='Red')
        elif x == 2 :
            entered_name=name.get().strip()
            try:
                curser.execute(f'Drop Database {entered_name}')
                print(entered_name)
                temp1.config(text=f'Successfully remove the database:{entered_name}',fg='Green')
            except:
                temp1.config(text=' No such database found(Check the spelling once again)')

    def table_manipulation_Window(x):
        global mycon
        curser = mycon.cursor()
        global temp1
        if x == 1:
            table_executor(1)
            
        elif x == 2:
            add = tk.Toplevel(dtw)
            add.geometry('600x300')
            add.title('Removing Table!')
            temp1=tk.Label(add,text='')
            temp1.pack(pady=20)
            tk.Label(add,text='Write the name of the Table you want to remove.').pack(side='top')
            name = tk.Entry(add)
            name.pack(padx=20)
            tk.Button(add,text="- Remove",fg='Red',command=lambda ent = name:table_executor(x,ent)).pack(padx=20)
    
    dtw = tk.Tk()
    dtw.title(f"Database {name}")
    dtw.geometry('800x600')
    l=tk.Label(dtw,text=' Select the Table:')
    l.pack(padx=20)
    menubar = tk.Menu(dtw)
    filemenu = tk.Menu(menubar,tearoff=0)
    filemenu.add_command(label='Exit',command=dtw.destroy)
    filemenu.add_command(label='Refresh',command=refresh)
    filemenu.add_command(label='Back_To_Database',command=database)
    menubar.add_cascade(label='File',menu=filemenu)
    dtw.config(menu=menubar)
    bf=tk.Frame(dtw)
    bf.pack(fill='both',expand=True)
    button_frame1 = tk.Frame(dtw)
    button_frame1.pack(fill="both", expand=True)
    buten_frame2 = tk.Frame(dtw).pack(side='bottom', fill= 'x' , padx= 10, pady=10)
    tk.Button(buten_frame2,text='+ Add New Table.',fg='Green',command=lambda:table_manipulation_Window(1)).pack(side='right',padx=5)
    tk.Button(buten_frame2,text='- Remove Table.',fg='Red',command=lambda:table_manipulation_Window(2)).pack(side='right',padx=5)
    if all_tabels == []:
        l.config(text='No table found Create new....',fg='Red')
    else:
        build_buttons1(all_tabels)
        
def rows() -> list: 
    global mycon
    cur = mycon.cursor()
    columns=cur.execute(f"""
    SELECT COLUMN_NAME
    FROM INFORMATION_SCHEMA.COLUMNS
    WHERE TABLE_SCHEMA = {database1}
      AND TABLE_NAME = {Table1}
    ORDER BY ORDINAL_POSITION;
        """) or cur.fetchall()
    return columns
root = tk.Tk()
root.title('App')
root.geometry('800x600')
label=tk.Label(root,text="This is created by Arun")
label.pack(padx=1,pady=2)
tk.Label(root,text='Enter User_Name(Default is root)').pack(pady=20)
enter1= tk.Entry(root)
enter1.pack(pady=20)
tk.Label(root,text='Enter the pasword!').pack(padx="20")
enter = tk.Entry(root,show='*')
enter.pack(pady=20)
lable1=tk.Label(root,text="")
lable1.pack(pady=20)
tk.Button(root,text='Check',command=sql_connected).pack(pady=20)
root.mainloop()
