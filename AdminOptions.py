from tkinter import *
from tkinter import messagebox
import cx_Oracle


class AdminSubMenu:
    def __init__(self):
        self.window = Toplevel()
        self.window.title("Admin - Sub Menu")
        self.window.geometry("425x150")
        Button(self.window, text="Closed Accounts History", height=2, width=60, command = self.closedHistory).grid(row=0)
        Button(self.window, text="Logout", height=2, width=60, command = self.logout).grid(row=1)
         
   
            
    def closedHistory(self):
        con = cx_Oracle.connect("system/123@xe")
        cur = con.cursor()
        try:
            cur.execute("SELECT ACCOUNTNUMBER, STATUSDATE FROM ACCOUNT WHERE STATUS= :1 ",(['LOCKED']))
            res = cur.fetchall()
            if res:
                window2 = Toplevel()
                window2.geometry('370x150')
                window2.title("Closed History")
                Label(window2, text="ACCOUNTNUMBER", width=30).grid(row=0, column=0)
                Label(window2, text="DATE", width=10).grid(row=0, column=1)
                for index, d in enumerate(res):
                    Label(window2, text = d[0]).grid(row=index+1,column=0)
                    Label(window2, text = d[1].date()).grid(row=index+1,column=1)
        except Exception as e:
            messagebox.showerror("Error", e)
            self.window.lift()
        finally:
            con.close()
            
    def logout(self):
        self.window.destroy()
        messagebox.showinfo("Success", "Admin Logged Out")
    
            