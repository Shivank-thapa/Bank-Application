from tkinter import *
from tkinter import messagebox
import cx_Oracle
from datetime import datetime

class SubSignInMenu():
    def __init__(self, ID):
        self.ID = ID 
        self.window = Toplevel()
        self.window.title("Sign In - Sub Menu")
        self.window.geometry("425x295")
        Button(self.window, text="Address Change", height=2, width=60, command = self.changeAddress).grid(row=0)
        Button(self.window, text="Money Deposit", height=2, width=60, command = self.depositMoney).grid(row=1)
        Button(self.window, text="Money Withdrawal", height=2, width=60, command = self.withdrawMoney).grid(row=2)
        Button(self.window, text="Print statement", height=2, width=60, command = self.printStatement).grid(row=3)
        Button(self.window, text="Transfer Money", height=2, width=60, command = self.transferMoney).grid(row=4)
        Button(self.window, text="Account closure", height=2, width=60, command = self.closeAccount).grid(row=5)
        Button(self.window, text="Customer Logout", height=2, width=60, command = self.logout).grid(row=6)
    
    def changeAddress(self):
        addr1 = input("Address line 1: ")
        addr2 = input("Address line 2: ")
        city = input("City: ")
        state = input("State: ")
        pincode = int(input("Pincode: "))
        con = cx_Oracle.connect("SYSTEM/123@XE")
        cur = con.cursor()
        try:
            cur.execute("""UPDATE CUSTOMER SET ADDRESSLINE1 = :1, ADDRESSLINE2 = :2, CITY = :3, STATE = :4, 
            PINCODE = :5 WHERE CUSTOMER_ID = :6""",([addr1, addr2, city, state, pincode,self.ID]))
            con.commit()
            messagebox.showinfo("Success", "Address changed")
            self.window.lift()
        except Exception as e:
            messagebox.showerror("Error", e)
        finally:
            con.close()
            self.window.lift()
            
    def depositMoney(self):
        amount = int(input("Enter amount to deposit: "))
        if amount > 0:
            con = cx_Oracle.connect("SYSTEM/123@XE")
            cur = con.cursor()
            try:
                cur.execute("SELECT SEQUENCE1.NEXTVAL FROM DUAL")
                res, = cur.fetchone()
                cur.execute("UPDATE ACCOUNT SET AMOUNT = :1+AMOUNT WHERE ACCOUNTNUMBER = :2",([amount, self.ID]))
                cur.execute("SELECT AMOUNT FROM ACCOUNT WHERE ACCOUNTNUMBER= :1",([self.ID]))
                bal, =cur.fetchone()
                cur.execute("INSERT INTO TRANSACTIONS(TRANSACTIONDATE, TRANSACTIONNUMBER, ACCOUNTNUMBER, TRANSACTIONTYPE, AMOUNT, BALANCE) VALUES(SYSDATE, :1,:2,:3,:4,:5)",([res, self.ID, "DEPOSIT",amount, bal]))
                con.commit()
                messagebox.showinfo("Success", "Amount deposited.\nFinal balance = {}".format(bal))
                self.window.lift()
            except Exception as e:
                messagebox.showerror("Error", e)
            finally:
                con.close()
        else:
            messagebox.showerror("Error", "Invalid amount!")
            self.window.lift()
            
    def withdrawMoney(self):
        amount = int(input("Enter amount to withdraw: "))
        con = cx_Oracle.connect("SYSTEM/123@XE")
        cur = con.cursor()
        try:
            cur.execute("SELECT AMOUNT FROM ACCOUNT WHERE ACCOUNTNUMBER = :1",([self.ID]))
            balance, = cur.fetchone()
            if balance - amount <= 0:
                raise Exception("Insufficient balance.")
            cur.execute("SELECT ACCOUNTTYPE FROM ACCOUNT WHERE ACCOUNTNUMBER=:1",([self.ID]))
            _type, = cur.fetchone()
            if _type == 'Savings':
                cur.execute("SELECT ADD_MONTHS(REGISTERDATE,1) FROM CUSTOMER WHERE CUSTOMER_ID=:1",([self.ID]))
                validity = cur.fetchall()
                for data in validity:
                    pass
                cur.execute("SELECT COUNT(TRANSACTIONTYPE) FROM TRANSACTIONS WHERE TRANSACTIONTYPE=:1 AND SYSDATE <:2",(['WITHDRAW',data[0].date()]))
                count=cur.fetchone()
                d = count[0]
                if d >= 10:
                    raise Exception("WITHDRAW LIMIT EXCEEDED")
                else:
                    self.trans(amount)
            else:
                self.trans(amount)
        except Exception as e:
            messagebox.showerror("Error", e)
            self.window.lift()
        finally:
            con.close()

    def trans(self,amount):
        self.amount=amount
        con = cx_Oracle.connect("SYSTEM/123@xe")
        cur = con.cursor()
        try:
            cur.execute("SELECT SEQUENCE1.NEXTVAL FROM DUAL")
            res, = cur.fetchone()
            cur.execute("UPDATE ACCOUNT SET AMOUNT = AMOUNT-:1 WHERE ACCOUNTNUMBER = :2",([amount, self.ID]))
            cur.execute("SELECT AMOUNT FROM ACCOUNT WHERE ACCOUNTNUMBER= :1",([self.ID]))
            bal, = cur.fetchone()
            cur.execute("INSERT INTO TRANSACTIONS(TRANSACTIONDATE, TRANSACTIONNUMBER, ACCOUNTNUMBER, TRANSACTIONTYPE, AMOUNT, BALANCE) VALUES(SYSDATE,:1,:2,:3,:4,:5)",([res, self.ID, "WITHDRAW", amount, bal]))
            con.commit()
            messagebox.showinfo("Success", "Amount withdrawn.\nFinal balance = {}".format(bal))
            self.window.lift()
        except Exception as e:
            messagebox.showerror("Error", e)
        finally:
            con.close()

            
    def printStatement(self):
        date1 = datetime.strptime(input("Enter first date(dd-mm-yy): "), '%d-%m-%y')
        date1 = date1.date()
        date2 = datetime.strptime(input("Enter second date(dd-mm-yy): "), '%d-%m-%y')
        date2 = date2.date()
        con = cx_Oracle.connect("SYSTEM/123@XE")
        cur = con.cursor()
        try:
            cur.execute("SELECT TRANSACTIONDATE, TRANSACTIONTYPE, AMOUNT, BALANCE FROM TRANSACTIONS WHERE TRANSACTIONDATE BETWEEN :1 AND :2 AND ACCOUNTNUMBER= :3",([date1, date2, self.ID]))
            res = cur.fetchall()
            if res:
                window2=Toplevel()
                window2.geometry('350x150')
                window2.title("Table")
                dateLabel= Label(window2, text="Date", width=10)
                dateLabel.grid(row=0, column=0)
                _type= Label(window2,text="Type", width=10)
                _type.grid(row=0, column=1)
                amount= Label(window2, text="Amount", width=10)
                amount.grid(row=0,column=2)
                balance= Label(window2, text="Balance", width=10)
                balance.grid(row=0,column=3)
                for index, d in enumerate(res):
                    Label(window2, text = d[0].date()).grid(row=index+1,column=0)
                    Label(window2, text = d[1]).grid(row=index+1,column=1)
                    Label(window2, text = d[2]).grid(row=index+1,column=2)
                    Label(window2, text = d[3]).grid(row=index+1,column=3)
                window2.lift(self.window)
        except Exception as e:
            messagebox.showerror("Error", e)
        finally:
            self.window.lift()
            con.close()
    
    def closeAccount(self):
        con = cx_Oracle.connect("SYSTEM/123@XE")
        cur = con.cursor()
        try:
            cur.execute("UPDATE ACCOUNT SET STATUS = :1, STATUSDATE = SYSDATE WHERE ACCOUNTNUMBER = :2",(["LOCKED", self.ID]))
            con.commit()
            cur.execute("SELECT AMOUNT FROM ACCOUNT WHERE ACCOUNTNUMBER = :1",([self.ID]))
            bal, = cur.fetchone()
            messagebox.showinfo("Success", "Account closed successfully! Amount {} to be sent to your address".format(bal))
        except Exception as e:
            messagebox.showinfo("Error", e)
        finally:
            self.window.destroy()
            con.close()
        
    def transferMoney(self):
        con = cx_Oracle.connect("SYSTEM/123@XE")
        cur = con.cursor()
        to_Acc = int(input("Transfer to account number: "))
        try:
            cur.execute("SELECT ACCOUNTNUMBER FROM ACCOUNT WHERE ACCOUNTNUMBER = :1 AND STATUS <> 'LOCKED'",([to_Acc]))
            if cur.fetchone():
                amt = int(input("Enter amount to transfer: "))
                cur.execute("SELECT AMOUNT FROM ACCOUNT WHERE ACCOUNTNUMBER = :1",([to_Acc]))
                balance, = cur.fetchone()
                if balance - amt <= 0:
                    messagebox.showerror("Error", "Insufficient balance.")
                    return 
                else:
                    cur.execute("SELECT SEQUENCE1.NEXTVAL FROM DUAL")
                    res, = cur.fetchone()
                    con.commit()
                    cur.execute("UPDATE ACCOUNT SET AMOUNT = AMOUNT-:1 WHERE ACCOUNTNUMBER = :2", ([amt, self.ID]))
                    cur.execute("SELECT AMOUNT FROM ACCOUNT WHERE ACCOUNTNUMBER= :1",([self.ID]))
                    bal1, = cur.fetchone()
                    cur.execute("INSERT INTO TRANSACTIONS(TRANSACTIONDATE, TRANSACTIONNUMBER, ACCOUNTNUMBER, TRANSACTIONTYPE, AMOUNT, BALANCE) VALUES(SYSDATE, :1,:2,:3,:4,:5 )",([res, self.ID, "WITHDRAW", amt, bal1]))
                    cur.execute("SELECT SEQUENCE1.NEXTVAL FROM DUAL")
                    con.commit()
                    res, = cur.fetchone()
                    cur.execute("UPDATE ACCOUNT SET AMOUNT = :1+AMOUNT WHERE ACCOUNTNUMBER = :2",([amt, to_Acc]))
                    cur.execute("SELECT AMOUNT FROM ACCOUNT WHERE ACCOUNTNUMBER= :1",([to_Acc]))
                    bal2, = cur.fetchone()
                    cur.execute("INSERT INTO TRANSACTIONS(TRANSACTIONDATE, TRANSACTIONNUMBER, ACCOUNTNUMBER, TRANSACTIONTYPE, AMOUNT, BALANCE) VALUES(SYSDATE,:1,:2,:3,:4,:5)",([res, to_Acc, "DEPOSIT", amt, bal2]))
                    con.commit()
                    messagebox.showinfo("Success","Transfer Successfull\nYour balance is {}".format(bal1))
            else:
                messagebox.showerror("Error", "Account not found!")
        except Exception as e:
            messagebox.showerror("Error", e)
        finally:
            self.window.lift()
            con.close()
            
    def logout(self):
        messagebox.showinfo("Logout", "{} is logged out.".format(self.ID))
        self.window.destroy()