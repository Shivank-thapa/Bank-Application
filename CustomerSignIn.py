from tkinter import *
from tkinter import messagebox
from SubSignInMenu import *
import cx_Oracle

class CustomerSignIn:
    def __init__(self):
        self.window = Toplevel()
        self.window.title("Sign In")
        self.window.geometry("250x100")
        self.attempts = 3
        Label(self.window, text="Customer-id: ").grid(row=0, sticky = E)
        self.id = Entry(self.window)
        self.id.grid(row=0, column=1)
        Label(self.window, text="Password: ").grid(row=1, sticky = E)
        self.pwd = Entry(self.window)
        self.pwd.grid(row=1, column=1)
        Button(self.window, text="Login", command = self.checkUser).grid(row=2)
        Button(self.window, text="Cancel", command = self.window.destroy).grid(row=2, column=1, sticky=W) 
            
    def checkUser(self):
        con = cx_Oracle.connect("SYSTEM/123@XE")
        cur = con.cursor()
        try:
            if self.attempts > 1:
                ID = int(self.id.get())
                idCheck = False
                cur.execute("SELECT ACCOUNTNUMBER FROM ACCOUNT WHERE ACCOUNTNUMBER = :1 AND ACCOUNT.STATUS <> 'LOCKED' ",([ID]))
                if cur.fetchone():
                    idCheck = True
                else:
                    messagebox.showinfo("Sign up", "This customer-id is not present. Please sign up first.")
                    self.window.destroy()
                    return  
                PWD = str(self.pwd.get())
                cur.execute("SELECT PASSWORD FROM CUSTOMER WHERE PASSWORD= :1 AND CUSTOMER_ID = :2",([PWD, ID]))
                if cur.fetchone() and idCheck:
                    messagebox.showinfo("Success", "Login Successful")
                    self.window.destroy()
                    SignInSubMenu(ID)
                else:
                    self.attempts = self.attempts - 1 
                    messagebox.showerror("Error", "Invalid password.\nRetries left = {}".format(self.attempts))
                    self.window.lift()
                
            elif self.attempts == 1:
                messagebox.showerror("Error", "Invalid password")
                messagebox.showerror("Error", "Maximum retries. Customer-id {} is blocked.".format(self.id.get()))
                cur.execute("UPDATE ACCOUNT SET STATUS = :1, STATUSDATE = SYSDATE WHERE ACCOUNTNUMBER = :2",(["LOCKED", self.id.get()]))
                con.commit()
                self.window.destroy()
        except Exception as e:
            messagebox.showerror("Error", e)      
        finally:
            con.close() 
            return  