from tkinter import *
from Signup import *
from Accounts import *
from CustomerSignIn import *
from AdminSignIn import *

def createButtons(root):
    Button1 = Button(root, text = "Sign Up (New Customer)", bg = "white", fg = "red", height=2, width=100, command=SignUp)
    Button2 = Button(root, text = "Sign In (Existing Customer)", bg = "white", fg = "red", height=2, width=100, command=CustomerSignIn)
    Button3 = Button(root, text = "Admin Sign In", bg = "white", fg = "red", height=2, width=100, command=adminSignIn)
    Button4 = Button(root, text = "Quit",bg = "white", fg = "red", command = quit, height=2, width=100)
    Button1.pack(fill = BOTH, expand=1)
    Button2.pack(fill = BOTH, expand=1)
    Button3.pack(fill = BOTH, expand=1)
    Button4.pack(fill = BOTH, expand=1)
    return

root = Tk()
root.title("Main Menu")
root.geometry("400x163")
createButtons(root)
root.mainloop()