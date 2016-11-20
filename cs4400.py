from Tkinter import *
import pymysql
from re import findall

class cs4400Project:


    def __init__(self, rootwin):

        #Login GUI
        self.rootwin = rootwin
        self.rootwin.title("Login")

        self.frame = Frame(self.rootwin)
        self.frame.pack()
        Label(self.frame, text = "Username:").grid(row = 1, column = 0)
        self.usernameEntry = Entry(self.frame, width = 30)
        self.usernameEntry.grid(row=1, column = 1)
        Label(self.frame, text = "Password:").grid(row = 2, column = 0)
        self.passwordEntry = Entry(self.frame, width = 30)
        self.passwordEntry.grid(row=2, column = 1)

        self.loginButton = Button(self.frame, text = "Login", command = self.loginCheck)
        self.loginButton.grid(row = 3, column = 0)


    def loginCheck(self):
        #check to see if the username and password passed in is in the database
        #if so, then bring them to the welcome page

        #connect to the database
        try:
            db = pymysql.connect(host = "academic-mysql.cc.gatech.edu", user = "cs4400_Team_5",
                                 passwd = "2KZtbzKa", db = "cs4400_Team_5")
            print("connected")
            cursor = db.cursor()
            print("yes")
            username = self.usernameEntry.get().strip()
            print(username)
            password = self.passwordEntry.get().strip()
            print(password)
            cursor.execute("SELECT Username,Password FROM USER WHERE Username = %s", (username,))
            print("lol")

            #try to see if anything was fetched from the query, if it is empty
            #then the username did not match, if not then we check the password
            #to see if those are equal 
            aList = cursor.fetchall()
            if(len(aList) != 0):
                realUsername = aList[0][0]
                print(realUsername)
                realPassword = aList[0][1]
                print(realPassword)
                if (realPassword != password):
                    print("wrong password")
                else:
                    print("logged in")
            else:
                print("wrong username")
        except:
             print("nope")


win = Tk()
app = cs4400Project(win)
win.mainloop()

