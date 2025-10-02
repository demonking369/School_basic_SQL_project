import tkinter as tk 
import mysql.connector as sql
mycon = None
def sql_connected():
    global mycon
    pas=enter.get()
    try:
        mycon = sql.connect(host="localhost",user="root",password=pas)
    except:
        lable1.config(text='Not Connected!(Wrong Pasword)',fg='Red')
    if mycon.is_connected() or pas.lower()=='q':
        lable1.config(text='Connected!',fg="Green")
        root.destroy()
        database()
def database():
    dash = tk.Tk()
    dash.geometry('800x600')
    dash.title('Database')
    menubar = tk.Menu(dash)
    filemenu = tk.Menu(menubar,tearoff=0)
    filemenu.add_command(label='Exit',command=dash.destroy)
    menubar.add_cascade(label='File',menu=filemenu)
    dash.config(menu=menubar)
    tk.Label(dash,text='Ok').pack(pady=20)
def rows():
    global mycon
    cur = mycon.cursor()
    cur.execute("""
    SELECT COLUMN_NAME
    FROM INFORMATION_SCHEMA.COLUMNS
    WHERE TABLE_SCHEMA = 'shopdb'
      AND TABLE_NAME = 'customers'
    ORDER BY ORDINAL_POSITION;
        """)
    columns = [row[0] for row in cur.fetchall()]
    return columns
root = tk.Tk()
root.title('App')
root.geometry('800x600')
label=tk.Label(root,text="This is created by Arun")
label.pack(padx=1,pady=2)
tk.Label(root,text='Enter the pasword!').pack(padx="20")
enter = tk.Entry(root)
enter.pack(pady=20)
lable1=tk.Label(root,text="")
lable1.pack(pady=20)
tk.Button(root,text='Check',command=sql_connected).pack(pady=20)
root.mainloop()