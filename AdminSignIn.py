from tkinter import *
from tkinter import messagebox
from AdminOptions import *
import cx_Oracle


class adminSignIn:
    def __init__(self):
        self.window = Toplevel()
        self.window.title("Admin Sign In")
        self.window.geometry("250x100")
        self.attempts = 3
        Label(self.window, text="Admin-id: ").grid(row=0, sticky = E)
        self.id = Entry(self.window)
        self.id.grid(row=0, column=1)
        Label(self.window, text="Password: ").grid(row=1, sticky = E)
        self.pwd = Entry(self.window)
        self.pwd.grid(row=1, column=1)
        Button(self.window, text="Login", command = self.checkAdmin).grid(row=2)
        Button(self.window, text="Cancel", command = self.window.destroy).grid(row=2, column=1, sticky=W) 
    
    def checkAdmin(self):
        con = cx_Oracle.connect("SYSTEM/123@XE")
        cur = con.cursor()
        try:
            if self.attempts > 1:
                ID = int(self.id.get())
                idCheck = False
                cur.execute("SELECT ADMIN_ID FROM ADMIN WHERE ADMIN_ID = :1",([ID]))
                if cur.fetchone():
                    idCheck = True
                else:
                    messagebox.showerror("Error", "This admin-id is not present.")
                    self.window.destroy()
                    return
                PWD = str(self.pwd.get())
                cur.execute("SELECT PASSWORD FROM ADMIN WHERE PASSWORD= :1 AND ADMIN_ID = :2",([PWD, ID]))
                if cur.fetchone() and idCheck:
                    messagebox.showinfo("Success", "Login Successfull")
                    self.window.destroy()
                    AdminSubMenu()
                else:
                    self.attempts = self.attempts - 1 
                    messagebox.showerror("Error", "Invalid password.\nRetries left = {}".format(self.attempts))
                    self.window.lift() 
                    return
            elif self.attempts == 1:
                messagebox.showerror("Error", "Too many attempts.\nTry again later.")
                self.window.destroy()
        except Exception as e:
            messagebox.showerror("Error", e) 
        finally:
            con.close()  
            return  
        