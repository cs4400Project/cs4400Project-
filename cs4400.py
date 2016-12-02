from tkinter import *
import pymysql
from re import findall
import urllib.request
import re



class cs4400Project:


    def __init__(self, rootwin):

        #Login GUI
        self.rootwin = rootwin
        self.rootwin.title("Login")
        self.rootwin.configure(background="gray")

        self.frame = Frame(self.rootwin,background="gray")
        self.frame.pack()  ###fill? 

        self.frame2 = Frame(self.rootwin,background="gray")
        self.frame2.pack(side=LEFT) ###

        self.frame3 = Frame(self.rootwin,background="gray")
        self.frame3.pack(side=RIGHT)
        
        
        #picc SLS
        url = "http://imageshack.com/a/img923/492/NJ18VG.gif" 
        response = urllib.request.urlopen(url)
        myPicture = response.read()
        import base64
        b64_data = base64.encodebytes(myPicture)
        self.photo = PhotoImage(data=b64_data)
        l = Label(self.frame, image = self.photo)
        l.grid(row= 0, column = 0, sticky= E)
        #picc


        
        #Labels and Entry Boxes
        Label(self.frame2, text = "Username:",background="gray").grid(row = 2, column = 0,sticky=W)
        self.usernameEntry = Entry(self.frame2, width = 30)
        self.usernameEntry.grid(row=3, column = 0)
        Label(self.frame2, text = "Password:",background="gray").grid(row = 4, column = 0,sticky=W)
        self.passwordEntry = Entry(self.frame2, width = 30)
        self.passwordEntry.grid(row=5, column = 0)

        #Buttons
        #Login takes you to welcome if correct
        #Register takes you to the register page
        self.loginButton = Button(self.frame2, text = "Login", command = self.loginCheck,width=12,background="gray")
        self.loginButton.grid(row = 6, column = 0,sticky=W)
        self.registerButton = Button(self.frame2, text = "Register", command = self.registerPage,width=12,background="gray")
        self.registerButton.grid(row = 6, column = 0,sticky=E)

        #pic2

        url2 = "http://imageshack.com/a/img924/234/jPYnHe.gif" ## smaller pic http://imageshack.com/a/img922/3895/F4owQE.gif 
        response2 = urllib.request.urlopen(url2)
        myPicture2 = response2.read()
        import base64
        b64_data2 = base64.encodebytes(myPicture2)
        self.photo2 = PhotoImage(data=b64_data2)
        l2 = Label(self.frame3, image = self.photo2)
        l2.grid(row= 0, column = 0, sticky= E)

        #pic2


    def loginCheck(self):
        #check to see if the username and password passed in is in the database
        #if so, then bring them to the welcome page

        #connect to the database
        try:
            db = pymysql.connect(host = "academic-mysql.cc.gatech.edu", user = "cs4400_Team_5",
                                 passwd = "2KZtbzKa", db = "cs4400_Team_5")
            print("connected")
            cursor = db.cursor()
            username = self.usernameEntry.get().strip()
            password = self.passwordEntry.get().strip()
            cursor.execute("SELECT Username,Password FROM USER WHERE Username = %s", (username,))

            #try to see if anything was fetched from the query, if it is empty
            #then the username did not match, if not empty then we check the password
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
                    self.loginToWelcome()
            else:
                print("wrong username")
            cursor.close()
            db.close()
        except:
             print("could not connect to database")

    def registerPage(self):

        #GUI for the Register Page
        print("register page")
        self.rootwin.withdraw()
        self.regWin = Toplevel()
        self.regWin.title("Register")
        self.regWin.configure(background="gray")

        ###slspic

        self.picFrame =Frame(self.regWin,background="gray")
        self.picFrame.pack()
        
        urlsls = "http://imageshack.com/a/img923/492/NJ18VG.gif" 
        responsesls = urllib.request.urlopen(urlsls)
        myPicturesls = responsesls.read()
        import base64
        b64_datasls = base64.encodebytes(myPicturesls)
        self.photosls = PhotoImage(data=b64_datasls)
        lsls = Label(self.picFrame, image = self.photosls)
        lsls.grid(row= 0, column = 0, sticky= E)
        #slspicc
        
        self.regFrame = Frame(self.regWin,background="gray")
        self.regFrame.pack()
        
        #Labels and Entry Boxes
        Label(self.regFrame, text = "Username:",background="gray").grid(row = 0, column = 0)
        Label(self.regFrame, text = "GT Email:",background="gray").grid(row = 1, column = 0)
        Label(self.regFrame, text = "Password:",background="gray").grid(row = 2, column = 0)
        Label(self.regFrame, text = "Confirm Password:",background="gray").grid(row = 3, column = 0)
        self.regUsernameEntry = Entry(self.regFrame, width = 30)
        self.regUsernameEntry.grid(row = 0, column = 1,columnspan=2)
        self.regEmailEntry = Entry(self.regFrame, width = 30)
        self.regEmailEntry.grid(row = 1, column = 1,columnspan=2)
        self.regPasswordEntry = Entry(self.regFrame, width = 30)
        self.regPasswordEntry.grid(row = 2, column = 1,columnspan=2)
        self.regConfirmPasswordEntry = Entry(self.regFrame, width = 30)
        self.regConfirmPasswordEntry.grid(row = 3, column = 1,columnspan=2)

        #Buttons
        #Register submits the information (if correct) and straight to the welcome page
        #Back sends you back to the login page
        self.regButton = Button(self.regFrame, text = "Back", command = self.backToLogin,width=5,background="gray")
        self.regButton.grid(row = 4, column = 1,sticky=E)
        self.regBackButton = Button(self.regFrame, text = "Register", command = self.registerUser,width=8,background="gray") 
        self.regBackButton.grid(row = 4, column = 2,sticky=E+W)       


    def loginToWelcome(self):
        #If the login is successful, then the login window will close
        #And the welcome screen will appear
        self.rootwin.withdraw()
        print("at welcome")

    def registerUser(self):
        #Register a new user that has a unique email and password
        #If successful, then bring them to the welcome page
        try:
            #connect to database
            db = pymysql.connect(host = "academic-mysql.cc.gatech.edu", user = "cs4400_Team_5",
                                 passwd = "2KZtbzKa", db = "cs4400_Team_5")
            print("connected")
            cursor = db.cursor()
            username = self.regUsernameEntry.get().strip()
            email = self.regEmailEntry.get().strip()
            password = self.regPasswordEntry.get().strip()
            confirmPassword = self.regConfirmPasswordEntry.get().strip()

            #Check all the cases
            #1.none of it can be blank
            #2.must be a gatech email
            #3.unique username and email
            #4.passwords must match
            if(len(password) == 0 or len(username) == 0 or len(email) == 0):
                print("none of the fields above can be empty")
            elif(email[email.index("@")+1:] != "gatech.edu"):
                print("must have a gatech email")
            else:
                cursor.execute("SELECT Username FROM USER WHERE Username = %s",(username,))
                databaseUser = cursor.fetchall()
                cursor.execute("SELECT Email FROM USER WHERE Email = %s",(email,))
                databaseEmail = cursor.fetchall()
                if(password != confirmPassword):
                    print("passwords must match")
                elif len(databaseUser) != 0:
                    print("username already taken")
                elif len(databaseEmail) != 0:
                    print("email already taken")
                else:
                    #If everything works then we insert the new user into the database
                    statement = "INSERT INTO USER (Username, Password, Email, UserType) values (%s, %s, %s, %s)"
                    data = (username, password, email, "User")
                    cursor.execute(statement,data)
                    db.commit()
                    print("You have registered a user")
                    self.regToWelcome()
            cursor.close()
            db.close()
        except:
            print("could not connect to database")
        
    def regToWelcome(self):
        #If the register is successful, then the register window will close
        #And the welcome screen will appear
        self.regWin.withdraw()
        print("at welcome")

    def backToLogin(self):
        #If they are on the register screen and want to go back to the login screen
        #Then they click the button, the reg screen will close and the login will appear
        self.regWin.withdraw()
        self.rootwin.iconify()

    

win = Tk()
app = cs4400Project(win)
win.mainloop()

