import tkinter as tk 
import mysql.connector as sql
from tkinter import ttk 
import subprocess as sub
import sys
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
        try:
            mycon = sql.connect(host="localhost",user=user1,password=pas,charset="utf8")
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
    def refresh():
        dash.destroy()
        database()
    if x == 1:
        try:
            curser.execute(f'Create database {entered_name};')
            temp.config(text='New table added successfully Please refresh to see the change in the database',fg='Green')
            refresh()
        except:
            temp.config(text=' May be name is already taken Please check again and make sure name do not already exist in database.',fg='Red')
    elif x == 2 :
        try:
            curser.execute(f'Drop Database {entered_name}')
            temp.config(text=f'Successfully remove the database:{entered_name}',fg='Green')
            refresh()
        except:
            temp.config(text=' No such database found(Check the spelling once again)')

def build_buttons(student_list):
    global button_frame
    global n
    for name in student_list:
        btn = tk.Button(button_frame, text=name, width=20,
                        command=lambda n=name: table(n))
        n = name
        btn.pack(pady=5)
        
def open_table(name1,table):
    global mycon,table2,database1,Table1,columes1
    database1=name1
    Table1 = table 
    table2 = table
    cur = mycon.cursor()
    columes1=rows()
    print("Output 116:",columes1)
    print('Output 117:',name1)
    print('Output 118:',table)
    cur.execute(f'use {name1};')
    table2=(cur.execute(f'select * from {table};') or cur.fetchall())
    print('Output 122:',table2)
    newroot = tk.Tk()
    newroot.title(f'Table {table} of Database {name1}')
    newroot.geometry('800x600')
    frame = tk.Frame(newroot)
    frame.pack(fill='both',expand=True)
    frame1 = tk.Frame(newroot)
    frame1.pack(side='bottom', fill= 'x' , padx= 10, pady=10)
    tk.Button(frame1,text='Add data:',command=lambda:data_manipulator(1),fg='green').pack(side='right',padx=5)
    tk.Button(frame1,text='Remove data:',command=lambda:data_manipulator(2),fg='red').pack(side='right',padx=5) 
    columes1 = ['index',] + columes1
    tree = ttk.Treeview(frame, columns=columes1, show='headings')
    tree.pack(side='left', fill='both', expand=True)
    tree.heading('index',text='index')
    tree.column('index', width=40, anchor='center')
    for col in columes1:
        tree.heading(col, text=col)
        tree.column(col, width=100, anchor='center')
    scrolbar = ttk.Scrollbar(frame, orient='vertical', command=tree.yview)
    tree.configure(yscrollcommand=scrolbar.set)    
    scrolbar.pack(side='right', fill='y')
    for i, row in enumerate(table2, start=1):
        tree.insert('', 'end', values=(i,) + row)
    def table_refresh():
        tree.delete(*tree.get_children())
        new_data = (cur.execute(f'select * from {table};') or cur.fetchall())
        for i, row in enumerate(new_data, start=1):
            tree.insert('', 'end', values=(i,) + row)
    def data_manipulator(x):
        global mycon,columes1
        curser = mycon.cursor()
        if x == 1:
            add = tk.Toplevel(newroot)
            add.geometry('600x400')
            add.title('Adding Data!')
            entries = []
            for col in columes1[1:]:
                tk.Label(add, text=f'Enter {col}:').pack(pady=5)
                entry = tk.Entry(add)
                entry.pack(pady=5)
                entries.append(entry)
            def add_data():
                values = [entry.get().strip() for entry in entries]
                placeholders = ', '.join(['%s'] * len(values))
                try:
                    curser.execute(f'INSERT INTO {table} ({", ".join(columes1[1:])}) VALUES ({placeholders})', values)
                    mycon.commit()
                    add.destroy()
                    table_refresh()
                except Exception as e:
                    print(f"Error: {e}")
            tk.Button(add, text='Add Data', fg='Green', command=add_data).pack(pady=20)
        elif x == 2:
            global entery
            add = tk.Toplevel(newroot)
            add.geometry('600x300')
            add.title('Removing Data!')
            tk.Label(add, text='Enter the index of the row to remove:').pack(pady=20)
            entery = tk.Entry(add)
            entery.pack(pady=5)
            def remove_data():
                global mycon,columes1,entery
                curser = mycon.cursor()
                index = entery.get().strip()
                try:
                    curser.execute(f'SELECT * FROM {table};')
                    rows = curser.fetchall()
                    if 1 <= int(index) <= len(rows):
                        row_to_delete = rows[int(index) - 1]
                        conditions = ' AND '.join([f"{col} = %s" for col in columes1[1:]])
                        curser.execute(f'DELETE FROM {table} WHERE {conditions}', row_to_delete)
                        mycon.commit()
                        add.destroy()
                        table_refresh()
                    else:
                        print("Index out of range")
                except Exception as e:
                    print(f"Error: {e}")
            tk.Button(add,text='Remove Data', fg='Red', command=remove_data).pack(pady=5)
            
def table(name):
    dash.destroy()
    global mycon,n
    global bf
    global dtw
    global c
    global database1
    database1=name
    def refresh(table_name=name):
        dtw.destroy()
        table(table_name)
    cursor = mycon.cursor()
    cursor.execute(f'use {name};')
    all_tabels = list(cursor.execute("show Tables;") or cursor.fetchall())
    all_tabels = [row[0] for row in all_tabels]

    def build_buttons1(s):
        global bf
        for name1 in s:
            btn = tk.Button(bf, text=name1, width=20,
                            command=lambda n=name1:open_table(database1,n))
            btn.pack(pady=5)
            
    def table_executor(x,name=None):
        global mycon
        global temp1
        curser = mycon.cursor()
        if x == 1:
            try:
                print(name)
                curser.execute(f'use {name};')
                result = sub.run([sys.executable,'SQL_Creator.py'],capture_output=True,text=True, timeout=300)
                stderr = result.stdout
                curser.execute(f'Use {name};')
                curser.execute(stderr) # this is the SQL or custom query
            except:
                print('Some error occured')
        elif x == 2 :
            entered_name=name.get().strip()
            try:
                curser.execute(f'Drop table {entered_name};')
                print(entered_name)
                temp1.config(text=f'Successfully remove the table:{entered_name}',fg='Green')
            except:
                temp1.config(text=' No such table found(Check the spelling once again)')

    def table_manipulation_Window(x,names=None):
        global mycon
        curser = mycon.cursor()
        global temp1
        if x == 1:
            table_executor(1,names)
            
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
    filemenu.add_command(label='Refresh',command=lambda:refresh(name))
    filemenu.add_command(label='Back_To_Database',command=database)
    menubar.add_cascade(label='File',menu=filemenu)
    dtw.config(menu=menubar)
    bf=tk.Frame(dtw)
    bf.pack(fill='both',expand=True)
    button_frame1 = tk.Frame(dtw)
    button_frame1.pack(fill="both", expand=True)
    buten_frame2 = tk.Frame(dtw).pack(side='bottom', fill= 'x' , padx= 10, pady=10)
    tk.Button(buten_frame2,text='+ Add New Table.',fg='Green',command=lambda:table_manipulation_Window(1,name)).pack(side='right',padx=5)
    tk.Button(buten_frame2,text='- Remove Table.',fg='Red',command=lambda:table_manipulation_Window(2)).pack(side='right',padx=5)
    if all_tabels == []:
        l.config(text='No table found Create new....',fg='Red')
    else:
        build_buttons1(all_tabels)
        
def rows(): 
    global mycon
    cur = mycon.cursor()
    print('Output 233:',database1,Table1)
    try:
        columns=list(cur.execute(f"""
        SELECT COLUMN_NAME
        FROM INFORMATION_SCHEMA.COLUMNS
        WHERE TABLE_SCHEMA = '{database1}'
        AND TABLE_NAME = '{Table1}'
        ORDER BY ORDINAL_POSITION;
            """) or cur.fetchall())
        columns = [row[0] for row in columns]
    except:
        return ['Some error occured']
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
