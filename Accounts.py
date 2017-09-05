import re
from tkinter import *
from tkinter import messagebox
import cx_Oracle

class Account():
    def __init__(self, fname, lname, addr1, addr2, city, state, pin, password, amount, accountType):
        self.fname = fname
        self.lname = lname
        self.addr1 = addr1
        self.addr2 = addr2
        self.city = city
        self.state = state
        self.pin = pin
        if re.match(r'[(A-Z)+(a-z)+(0-9)+(@#$%^&!+=)+]{8,}', password):
            self.password = password
        else:
            messagebox.showinfo("Error", "Password rules not followed. Please Sign Up again.")
            return
        if accountType == 1:
            self.accType = "Savings"
        elif accountType == 2:
            self.accType = "Current"
        self.amount = amount
        con = cx_Oracle.connect("SYSTEM/shivank@XE")
        cur = con.cursor()
        try:
            cur.execute("SELECT S1.NEXTVAL FROM DUAL")
            result, = cur.fetchone()
            cur.execute("INSERT INTO CUSTOMER VALUES(:1, :2, :3, :4, :5, :6, :7, :8, :9, SYSDATE)",([result, self.fname, self.lname,
                                                                                  self.addr1, self.addr2, self.city,
                                                                                  self.state, self.pin, self.password]))
            cur.execute("INSERT INTO ACCOUNT(ACCOUNTNUMBER, AMOUNT, ACCOUNTTYPE) VALUES(:1, :2, :3)",([result, self.amount, self.accType]))
            con.commit()
            messagebox.showinfo("Success", "Account created successfully!\nYour Account Number: {}".format(result))
        except Exception as e:
            messagebox.showerror("Error", "Invalid entry in table\n"+str(e))
        finally:
            con.close()
            return