import re
from Accounts import *
from tkinter import *
from tkinter import messagebox


class SignUp():
    def __init__(self):
        self.window = Toplevel()
        self.window.title("Sign Up")
        self.window.geometry("245x250")
        Label(self.window, text="First name: ").grid(row=0, sticky=E)
        self.fnameEntry = Entry(self.window)
        self.fnameEntry.grid(row=0, column=1)
        Label(self.window, text="Last name: ").grid(row=1, sticky=E)
        self.lnameEntry = Entry(self.window)
        self.lnameEntry.grid(row=1, column=1)
        Label(self.window, text="Address Line 1: ").grid(row=2, sticky=E)
        self.addrLine1 = Entry(self.window)
        self.addrLine1.grid(row=2, column=1)
        Label(self.window, text="Address Line 2: ").grid(row=3, sticky=E)
        self.addrLine2 = Entry(self.window)
        self.addrLine2.grid(row=3, column=1)
        Label(self.window, text="City: ").grid(row=4, sticky=E)
        self.cityEntry = Entry(self.window)
        self.cityEntry.grid(row=4, column=1)
        Label(self.window, text="State: ").grid(row=5, sticky=E)
        self.stateEntry = Entry(self.window)
        self.stateEntry.grid(row=5, column=1)
        Label(self.window, text="Pincode: ").grid(row=6, sticky=E)
        self.pinCodeEntry = Entry(self.window)
        self.pinCodeEntry.grid(row=6, column=1)
        Label(self.window, text="Password: ").grid(row=7, sticky=E)
        self.passwordEntry = Entry(self.window, show="*")
        self.passwordEntry.grid(row=7, column=1)
        self.v = IntVar()
        Label(self.window, text="Amount: ").grid(row=8)
        self.amountEntry = Entry(self.window)
        self.amountEntry.grid(row=8,column=1) 
        self.savingsCheck = Radiobutton(self.window, text="Savings Account", variable = self.v, value=1,command=self.sel)
        self.savingsCheck.grid(row=9)
        self.currentCheck = Radiobutton(self.window, text="Current Account", variable = self.v, value=2,command=self.sel)
        self.currentCheck.grid(row=9,column=1)
        Button(self.window, text="Submit", command = self.newAccount).grid(row=10, column=0)
        Button(self.window, text="Cancel", command = self.window.destroy).grid(row=10, column=1, sticky=W)
            
    def sel(self):
        return (self.v.get())

    def newAccount(self):
        Account(self.fnameEntry.get(), self.lnameEntry.get(), self.addrLine1.get(), self.addrLine2.get(),
        self.cityEntry.get(), self.stateEntry.get(), self.pinCodeEntry.get(), self.passwordEntry.get(), self.amountEntry.get(),
        self.sel())
        self.window.destroy()
        return 