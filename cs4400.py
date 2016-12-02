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
        #picc SLS



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
        self.loginButton.grid(row = 6, column = 0,sticky=W,pady=10)
        self.registerButton = Button(self.frame2, text = "Register", command = self.registerPage,width=12,background="gray")
        self.registerButton.grid(row = 6, column = 0,sticky=E,pady=10)

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
            cursor.execute("SELECT Username,Password,UserType FROM USER WHERE Username = %s", (username,))

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
                    
                    if(aList[0][2] == "Admin"):
                        self.loginToFunctionality()
                    else:
                        self.newUser = False
                        self.loginToWelcome()
                    print("login")
                    self.currentUser = realUsername

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
        self.welcomeScreen()
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
                    self.newUser = True
                    self.currentUser = username
                    self.regToEditProfile()
            cursor.close()
            db.close()
        except:
            print("could not connect to database")
        
    def regToEditProfile(self):
        #If the register is successful, then the register window will close
        #And the user will be taken straight to the edit profile screen
        self.regWin.withdraw()
        self.toEditProfile()
        print("at edit profile")

    def backToLogin(self):
        #If they are on the register screen and want to go back to the login screen
        #Then they click the button, the reg screen will close and the login will appear
        self.regWin.withdraw()
        self.rootwin.iconify()

    def welcomeScreen(self):
        #GUI for the welcome screen
        self.welcomeWin = Toplevel()
        self.welcomeWin.title("Welcome")
        self.welcomeFrame = Frame(self.welcomeWin)
        self.welcomeFrame.pack()

        #Me Button
        self.meButton = Button(self.welcomeFrame, text = "Me", command = self.meWindow)
        self.meButton.grid(row = 0, column = 0)

    def meWindow(self):

        #GUI for the Me page
        self.welcomeWin.withdraw()
        self.meWin = Toplevel()
        self.meWin.title("Me")
        self.meFrame = Frame(self.meWin)
        self.meFrame.pack()

        #Has 2 buttons, Edit Profile and My Applications 
        self.editProfileButton = Button(self.meFrame, text = "Edit Profile", command = self.toEditProfile)
        self.editProfileButton.grid(row = 0, column = 0)
        self.myApplicationButton = Button(self.meFrame, text = "My Application")
        self.myApplicationButton.grid(row = 1, column = 0)

    def toEditProfile(self):
        #If the user logged in, then it would first be taken to the welcome screen
        #And then the edit profile is only if they choose to
        #But if they are registering for the first time, they are instantly
        #Taken to the edit profile page
        if(not self.newUser):
            self.meWin.withdraw()
        self.editWin = Toplevel()
        self.editWin.title("Edit Profile")

        self.piceditFrame = Frame(self.editWin,background="gray")
        self.piceditFrame.pack()

        #picc SLS
        editurl = "http://imageshack.com/a/img923/492/NJ18VG.gif"
        editresponse = urllib.request.urlopen(editurl)
        myeditPicture = editresponse.read()
        import base64
        editb64_data = base64.encodebytes(myeditPicture)
        self.editphoto = PhotoImage(data=editb64_data)
        editpicl = Label(self.piceditFrame, image = self.editphoto)
        editpicl.grid(row= 0, column = 0, sticky= E)
        #picc SLS

        self.editFrame = Frame(self.editWin,background="gray")
        self.editFrame.pack(fill=X)
        print("at edit profile")

        try:
        #connect to database
            db = pymysql.connect(host = "academic-mysql.cc.gatech.edu", user = "cs4400_Team_5",
                                 passwd = "2KZtbzKa", db = "cs4400_Team_5")
            print("connected")
            cursor = db.cursor()

            #Setting up the major option
            cursor.execute("SELECT * FROM MAJOR")
            majorTuple = cursor.fetchall()
            cursor.execute("SELECT Major,Year FROM USER WHERE Username = %s", (self.currentUser,))
            currentUser = cursor.fetchall()

            #Using what we got from the SQL statement, majorTuple holds
            #tuples that look like (major, department) so we are going to
            #Make a dictionary to hold all of the mappings as well as
            #Make a list of all the majors to have for the dropdown menu
            majorList = []
            self.majorDict = {}
            for major in majorTuple:
                self.majorDict[major[0]] = major[1]
                majorList.append(major[0])

            Label(self.editFrame, text = "Major:",background="gray").grid(row = 0, column = 0)
            self.majorVariable = StringVar()
            #If the user is new, then what is shown is the first major from the
            #List, if not then it is the major they currently have
            if(self.newUser):
                self.majorVariable.set(majorList[0])
            else:
                self.majorVariable.set(currentUser[0][0])

            #setting the initial department, same concept with new user v. old
            self.departmentVar = StringVar()
            if(self.newUser):
                self.departmentVar.set(self.majorDict[majorList[0]])
            else:
                self.departmentVar.set(self.majorDict[currentUser[0][0]])
            majorOptionMenu = OptionMenu(self.editFrame, self.majorVariable, *majorList,command = self.changeDepartment)
            majorOptionMenu.grid(row = 0, column = 1)

            #same concept with year for old v new users
            Label(self.editFrame, text = "Year:",background="gray").grid(row = 1, column = 0)
            yearVariable = StringVar()
            if(self.newUser):
                yearVariable.set("Freshman")
            else:
                yearVariable.set(currentUser[0][1])
            yearOptionMenu = OptionMenu(self.editFrame, yearVariable, "Freshman", "Sophomore", "Junior", "Senior", command = self.changeYear)
            yearOptionMenu.grid(row = 1, column = 1)

            #once things are selected the user is no longer new
            self.newUser = False

            Label(self.editFrame, text = "Department:",background="gray").grid(row = 2, column = 0)
            self.departmentLabel = Label(self.editFrame, text = self.departmentVar.get())
            self.departmentLabel.grid(row = 2, column = 1)

            self.editToWelcomeButton = Button(self.editFrame, text = "Back", command = self.editToWelcome)
            self.editToWelcomeButton.grid(row=3, column = 0)
            
            cursor.close()
            db.close()
        except:
            print("could not connect to database")


    def changeDepartment(self,major):
        #Whenever a new option is selected from the optionMenu, it is instantly
        #changed in the database. Changing the major also instantly changes
        #the department
        try:
        #connect to database
            db = pymysql.connect(host = "academic-mysql.cc.gatech.edu", user = "cs4400_Team_5",
                                 passwd = "2KZtbzKa", db = "cs4400_Team_5")
            print("connected")
            cursor = db.cursor()
            cursor.execute("UPDATE USER SET Major = %s WHERE Username = %s", (major,self.currentUser))
            db.commit()
            cursor.close()
            db.close()
            
            self.departmentLabel.grid_forget()
            self.departmentVar.set("")
            department = self.majorDict[major]
            self.departmentVar.set(department)
            self.departmentLabel = Label(self.editFrame, text = self.departmentVar.get())
            self.departmentLabel.grid(row = 2, column = 1)
        except:
            print("cannot connect to database")

    def changeYear(self, year):
        #Whenever we choose an option for year, it is instantly updated in the
        #database
        try:
        #connect to database
            db = pymysql.connect(host = "academic-mysql.cc.gatech.edu", user = "cs4400_Team_5",
                                 passwd = "2KZtbzKa", db = "cs4400_Team_5")
            print("connected")
            cursor = db.cursor()
            cursor.execute("UPDATE USER SET Year = %s WHERE Username = %s", (year, self.currentUser))
            db.commit()
            cursor.close()
            db.close()
        except:
            print("cannot connect to database")

    def editToWelcome(self):
        self.editWin.withdraw()
        self.welcomeScreen()







    ###################################ADMIN#################################
    def loginToFunctionality(self):
        #Goes to admin page
        self.rootwin.withdraw()
        self.chooseFunctionality()
        
    def chooseFunctionality(self):
        #GUI for admin "choose functionality" page
        self.chooseFunctionalityWin = Toplevel()
        self.chooseFunctionalityWin.title("Choose Functionality")
        self.chooseFunctionalityWin.configure(background="grey")

        self.adminpicFrame = Frame(self.chooseFunctionalityWin,background="grey")
        self.adminpicFrame.pack()

        #picc SLS
        adminurl = "http://imageshack.com/a/img923/492/NJ18VG.gif"
        adminresponse = urllib.request.urlopen(adminurl)
        myadminPicture = adminresponse.read()
        import base64
        adminb64_data = base64.encodebytes(myadminPicture)
        self.adminphoto = PhotoImage(data=adminb64_data)
        adminl = Label(self.adminpicFrame, image = self.adminphoto)
        adminl.grid(row= 0, column = 0, sticky= E)
        #picc SLS


        self.chooseFunctionalityFrame = Frame(self.chooseFunctionalityWin,background="grey")
        self.chooseFunctionalityFrame.pack()

        self.viewAppButton = Button(self.chooseFunctionalityFrame, text = "View Application", command = self.CFToViewApp)
        self.viewAppButton.grid(row = 0, column = 0, pady=5)
        self.viewPopProReportButton = Button(self.chooseFunctionalityFrame, text = "View Popular Project Report", command = self.CFToViewPopPro)
        self.viewPopProReportButton.grid(row = 2, column = 0, pady=5)
        self.viewAppReportButton = Button(self.chooseFunctionalityFrame, text = "View Application Report", command = self.CFToAppReport)
        self.viewAppReportButton.grid(row = 4, column = 0,pady=5)
        self.addAProjectButton = Button(self.chooseFunctionalityFrame, text = "Add A Project", command = self.CFToAddPro)
        self.addAProjectButton.grid(row = 6, column = 0, pady=5)
        self.addACourseButton = Button(self.chooseFunctionalityFrame, text = "Add A Course", command = self.CFToAddCourse)
        self.addACourseButton.grid(row = 8, column = 0,pady=5)

        self.logoutButton = Button(self.chooseFunctionalityFrame, text = "Logout", command = self.logout)
        self.logoutButton.grid(row = 9, column = 0)


    def CFToViewApp(self):
        print("View App")

    def CFToViewPopPro(self):
        print("Popular Project")

    def CFToAppReport(self):
        print("Application Report")

    def CFToAddPro(self):
        self.chooseFunctionalityWin.withdraw()
        self.addProject()

    def CFToAddCourse(self):
        print("Add Project")

    def logout(self):
        self.chooseFunctionalityWin.withdraw()
        self.rootwin.iconify()
        print("logged out")

    def addProject(self):

        #GUI For Add Project Page
        #Has entry boxes for some, drop down menus for others
        self.addProjectWin = Toplevel()
        self.addProjectWin.title("Add Project")
        self.addProjectFrame = Frame(self.addProjectWin)
        self.addProjectFrame.pack()

        Label(self.addProjectFrame, text = "Project Name").grid(row = 0, column= 0)
        self.projectNameEntry = Entry(self.addProjectFrame)
        self.projectNameEntry.grid(row = 0, column = 1)
        Label(self.addProjectFrame, text = "Advisor").grid(row = 1, column = 0)
        self.advisorNameEntry = Entry(self.addProjectFrame)
        self.advisorNameEntry.grid(row = 1, column = 1)
        Label(self.addProjectFrame, text = "Advisor Email").grid(row = 2, column = 0)
        self.advisorEmailEntry = Entry(self.addProjectFrame)
        self.advisorEmailEntry.grid(row = 2, column = 1)
        Label(self.addProjectFrame, text = "Descipriton").grid(row = 3, column = 0)
        self.projectDescriptionEntry = Entry(self.addProjectFrame)
        self.projectDescriptionEntry.grid(row = 3, column = 1)

        try:
        #connect to database
            db = pymysql.connect(host = "academic-mysql.cc.gatech.edu", user = "cs4400_Team_5",
                                 passwd = "2KZtbzKa", db = "cs4400_Team_5")
            print("connected")
            cursor = db.cursor()

            cursor.execute("SELECT * FROM CATEGORY;")
            aList = cursor.fetchall()
            categoryList = []
            for category in aList:
                categoryList.append(category[0])
            Label(self.addProjectFrame, text = "Category").grid(row = 4, column= 0)
            self.categorySelection = StringVar()
            self.categorySelection.set(categoryList[0])
            self.categoryOption = OptionMenu(self.addProjectFrame, self.categorySelection, *categoryList)
            self.categoryOption.grid(row = 4, column = 1)

            cursor.execute("SELECT * FROM DESIGNATION;")
            aList = cursor.fetchall()
            designationList = []
            for designation in aList:
                designationList.append(designation[0])
            Label(self.addProjectFrame, text = "Designation").grid(row = 5, column = 0)
            self.designationVar = StringVar()
            self.designationVar.set(designationList[0])
            self.designationOption = OptionMenu(self.addProjectFrame, self.designationVar, *designationList)
            self.designationOption.grid(row = 5, column = 1)

            Label(self.addProjectFrame, text = "Estimated Number of Students").grid(row = 6, column = 0)
            self.estNumStudentsEntry = Entry(self.addProjectFrame)
            self.estNumStudentsEntry.grid(row = 6, column = 1)

            cursor.execute("SELECT * FROM MAJOR")
            majorTuple = cursor.fetchall()
            majorList = []
            for major in majorTuple:
                majorList.append(major[0])
            Label(self.addProjectFrame, text = "Major Requirement").grid(row = 7, column = 0)
            majorVar = StringVar()
            majorVar.set(majorList[0])
            self.projectMajorOption = OptionMenu(self.addProjectFrame, majorVar, *majorList)
            self.projectMajorOption.grid(row = 7, column = 1)

            yearVar = StringVar()
            yearVar.set("Freshman")
            Label(self.addProjectFrame, text = "Year Requirement").grid(row = 8, column = 0)
            self.projectYearOption = OptionMenu(self.addProjectFrame, yearVar, "Freshman","Sophomore", "Junior","Senior")
            self.projectYearOption.grid(row = 8, column = 1)

            cursor.execute("SELECT * FROM DEPARTMENT")
            departmentTuple = cursor.fetchall()
            departmentList = []
            for department in departmentTuple:
                departmentList.append(department[0])
            Label(self.addProjectFrame, text = "Department Requirement").grid(row = 9, column = 0)
            departmentVar = StringVar()
            departmentVar.set(departmentList[0])
            self.projectDepartmentOption = OptionMenu(self.addProjectFrame, departmentVar, *departmentList)
            self.projectDepartmentOption.grid(row = 9, column = 1)
    
            self.addProjectBackButton = Button(self.addProjectFrame, text = "Back")
            self.addProjectBackButton.grid(row = 10, column = 0)
            self.addProjectSubmitButton = Button(self.addProjectFrame, text = "Submit", command = self.submitProject)
            self.addProjectSubmitButton.grid(row = 11, column = 0)

            cursor.close()
            db.close()
        
        except:
            print("could not connect to database")

    def submitProject(self):
        projectName = self.projectNameEntry.get().strip()
        advisorName = self.advisorNameEntry.get().strip()
        advisorEmail = self.advisorEmailEntry.get().strip()
        description = self.projectDescriptionEntry.get().strip()
        print("submitted project")
win = Tk()
app = cs4400Project(win)
win.mainloop()

