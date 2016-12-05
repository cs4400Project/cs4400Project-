from tkinter import *
import pymysql
from re import findall
import urllib.request
import re
import base64
import datetime



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

        try:
        #connect to database
            db = pymysql.connect(host = "academic-mysql.cc.gatech.edu", user = "cs4400_Team_5",
                                 passwd = "2KZtbzKa", db = "cs4400_Team_5")
            print("connected")
            cursor = db.cursor()

            #Setting up the major option
            cursor.execute("SELECT * FROM MAJOR")
            majorTuple = cursor.fetchall()

            self.majorDict = {}
            for major in majorTuple:
                self.majorDict[major[0]] = major[1]

            cursor.close()
            db.close()
        except:
            print("cannot connect to database")


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
                if (realPassword != password):  #checks if password is correct
                    messagebox.showerror(title = "Error",message = "Wrong Password!")
                else:
                    
                    if(aList[0][2] == "Admin"):
                        self.loginToFunctionality()
                    else:
                        self.newUser = False
                        self.loginToWelcome()
                    print("login")
                    self.currentUser = realUsername

            else: #username not in database
                messagebox.showerror(title = "Error",message = "Wrong Username!")
            cursor.close()
            db.close()
        except: #cant connect to database
            messagebox.showerror(title = "Error",message = "Could not connect to database.")


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
        self.regUsernameEntry.grid(row = 0, column = 1,columnspan=2,pady=6)
        self.regEmailEntry = Entry(self.regFrame, width = 30)
        self.regEmailEntry.grid(row = 1, column = 1,columnspan=2,pady=6)
        self.regPasswordEntry = Entry(self.regFrame, width = 30)
        self.regPasswordEntry.grid(row = 2, column = 1,columnspan=2,pady=6)
        self.regConfirmPasswordEntry = Entry(self.regFrame, width = 30)
        self.regConfirmPasswordEntry.grid(row = 3, column = 1,columnspan=2,pady=6)

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
            if(len(password) == 0 or len(username) == 0 or len(email) == 0): #checks if fields have values
                messagebox.showerror(title = "Error",message = "No field is allowed to be empty!")
            elif(email[email.index("@")+1:] != "gatech.edu"): #checks if a gatech email
                messagebox.showerror(title = "Error",message = "Must have a gatech email to register.")
            else:
                cursor.execute("SELECT Username FROM USER WHERE Username = %s",(username,))
                databaseUser = cursor.fetchall()
                cursor.execute("SELECT Email FROM USER WHERE Email = %s",(email,))
                databaseEmail = cursor.fetchall()
                if(password != confirmPassword): #password and confirm must match
                    messagebox.showerror(title = "Error",message = "Password and Confirm Password must match.")
                elif len(databaseUser) != 0: #checks if username not taken
                    messagebox.showerror(title = "Error",message = "Username already in use.")
                elif len(databaseEmail) != 0: #checks if email not taken
                    messagebox.showerror(title = "Error",message = "Email already in use.")
                else:
                    #If everything works then we insert the new user into the database
                    statement = "INSERT INTO USER (Username, Password, Email, UserType) values (%s, %s, %s, %s)"
                    data = (username, password, email, "Student")
                    cursor.execute(statement,data)
                    db.commit()
                    messagebox.showinfo(title = "Success", message = "You have registered a new user!")
                    self.newUser = True
                    self.currentUser = username
                    self.regToEditProfile()
            cursor.close()
            db.close()
        except: #cannot connect to database
            messagebox.showerror(title = "Error",message = "Could not connect to database.")
        
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

        ###slspic

        self.picFrame =Frame(self.welcomeWin,background="gray")
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

        self.welcomeFrame = Frame(self.welcomeWin)
        self.welcomeFrame.pack()

        #Me Button
        self.meButton = Button(self.welcomeFrame, text = "My Profile", command = self.meWindow)
        self.meButton.grid(row = 0, column = 0, padx = 20, pady = 20)

        Label(self.welcomeFrame, text = "Main Page").grid(row = 0, column = 1)
        Label(self.welcomeFrame, text = "Title").grid(row = 1, column = 0)
        self.welcomeTitleEntry = Entry(self.welcomeFrame)
        self.welcomeTitleEntry.grid(row = 1, column = 1)
        try:
        #connect to database
            db = pymysql.connect(host = "academic-mysql.cc.gatech.edu", user = "cs4400_Team_5",
                                 passwd = "2KZtbzKa", db = "cs4400_Team_5")
            print("connected")
            cursor = db.cursor()
            Label(self.welcomeFrame, text = "Category").grid(row = 2, column = 0)
            self.categories = []
            self.optionMenus = []
            cursor.execute("SELECT * FROM CATEGORY;")
            aList = cursor.fetchall()
            self.categoryList = []
            for category in aList:
                self.categoryList.append(category[0])
            self.categoryList.insert(0,"Please Select")
            print("populated my category list")
            self.categorySelection = StringVar()
            print("made my var")
            self.categorySelection.set(self.categoryList[0])
            self.categories.append(self.categorySelection)
            self.numOfCategories = 1
            categoryOption = OptionMenu(self.welcomeFrame, self.categorySelection, *self.categoryList)
            categoryOption.grid(row = 2, column = 1,pady=6)

            addCategoryButton = Button(self.welcomeFrame, text = "Add a Category", command = self.mainPageAddCategory)
            addCategoryButton.grid(row = 3, column = 0)
            
            Label(self.welcomeFrame, text = "Designation").grid(row = 4, column = 0)
            cursor.execute("SELECT * FROM DESIGNATION;")
            aList = cursor.fetchall()
            designationList = []
            for designation in aList:
                designationList.append(designation[0])
            designationList.insert(0,"")
            self.welcomeDesignationVar = StringVar()
            self.welcomeDesignationVar.set(designationList[0])
            designationOption = OptionMenu(self.welcomeFrame, self.welcomeDesignationVar, *designationList)
            designationOption.grid(row = 4, column = 1,pady=6)
            
            Label(self.welcomeFrame, text = "Major").grid(row = 4, column = 2)
            cursor.execute("SELECT * FROM MAJOR")
            majorTuple = cursor.fetchall()
            majorList = []
            for major in majorTuple:
                majorList.append(major[0])
            majorList.insert(0, "")
            self.welcomeMajorVar = StringVar()
            self.welcomeMajorVar.set(majorList[0])
            majorOption = OptionMenu(self.welcomeFrame, self.welcomeMajorVar, *majorList)
            majorOption.grid(row = 4, column = 3,pady=6)
            
            Label(self.welcomeFrame, text = "Year").grid(row = 4, column = 4)
            self.welcomeYearVar = StringVar()
            self.welcomeYearVar.set("")
            yearOption = OptionMenu(self.welcomeFrame, self.welcomeYearVar, "", "Freshman","Sophomore", "Junior","Senior")
            yearOption.grid(row = 4, column = 5,pady=6)

            self.filterRadio = StringVar()
            self.radio1 = Radiobutton(self.welcomeFrame, text = "Project", variable = self.filterRadio, value = "Project")
            self.radio1.grid(row = 5, column = 0)
            radio2 = Radiobutton(self.welcomeFrame, text = "Course", variable = self.filterRadio, value = "Course")
            radio2.grid(row = 5, column = 1)
            radio3 = Radiobutton(self.welcomeFrame, text = "Both", variable = self.filterRadio, value = "Both")
            radio3.grid(row = 5, column = 2)
            self.radio1.select()

            applyFilterButton = Button(self.welcomeFrame, text = "Apply Filter", command = self.applyFilter)
            applyFilterButton.grid(row = 6, column = 0)
            resetFilterButton = Button(self.welcomeFrame, text = "Reset Filter", command = self.resetFilter)
            resetFilterButton.grid(row = 6, column = 1)

            tableFrame = Frame(self.welcomeWin)
            tableFrame.pack()

            scrollbar = Scrollbar(tableFrame)
            scrollbar.pack(side = RIGHT, fill = Y)

            self.nameBox = Listbox(tableFrame, yscrollcommand=scrollbar.set)
            self.typeBox = Listbox(tableFrame, yscrollcommand=scrollbar.set)

            self.nameBox.insert(0,"NAME")
            self.typeBox.insert(0,"TYPE")
            self.nameBox.pack(side = LEFT, fill = BOTH)
            self.typeBox.pack(side = LEFT, fill = BOTH)

            listboxes = [self.nameBox, self.typeBox]

            def onVSB(*args):
                for lb in listboxes:
                    lb.yview(*args)

            scrollbar.config(command=onVSB)

            bottomFrame = Frame(self.welcomeWin)
            bottomFrame.pack()

            self.viewButton = Button(bottomFrame, text = "View", command = self.viewElement)
            self.viewButton.grid(row = 0, column = 1, padx = 20, pady = 20)
            self.logoutButton = Button(bottomFrame, text = "Log Out", command = self.logoutMe)
            self.logoutButton.grid(row = 0, column = 0, padx = 20, pady = 20)

            cursor.close()
            db.close()

        except:
            print("cannot connect to database")

    def mainPageAddCategory(self):
        self.categories.append(StringVar())
        self.categories[len(self.categories)-1].set(self.categoryList[0])
        self.numOfCategories += 1
        self.optionMenus.append(OptionMenu(self.welcomeFrame, self.categories[len(self.categories)-1], *self.categoryList))
        self.optionMenus[len(self.optionMenus)-1].grid(row = 2, column = self.numOfCategories)

    def applyFilter(self):
        try:
        #connect to database
            db = pymysql.connect(host = "academic-mysql.cc.gatech.edu", user = "cs4400_Team_5",
                                 passwd = "2KZtbzKa", db = "cs4400_Team_5")
            print("connected")
            cursor = db.cursor()
            filterCategories = []
            for k in self.categories:
                filterCategories.append(k.get())
            categoryStatement = "sub.Category_name = '" + filterCategories[0] + "'"
            x = len(filterCategories)
            print(x)
            for i in range(1, x):
                if(filterCategories[i] != "Please Select"):
                    categoryStatement += " OR sub.Category_name = '" + filterCategories[i] + "'"
            for j in filterCategories:
                if(j == "Please Select"):
                    filterCategories.remove(j)

            #categoryStatement = categoryStatement[:len(categoryStatement)-1]
            categoryStatement += ";"
            print(self.filterRadio.get())
            if(self.filterRadio.get() == "Project"):
                statement = "SELECT Name FROM (SELECT * FROM PROJECT NATURAL JOIN PROJECT_REQUIREMENT NATURAL JOIN PROJECT_IS_CATEGORY)sub WHERE (sub.Designation LIKE '" + self.welcomeDesignationVar.get()+ "%' OR ISNULL(sub.Designation)) AND (sub.Year_Requirement LIKE '" +self.welcomeYearVar.get()+ "%' OR ISNULL(sub.Year_Requirement)) AND (sub.Major_Requirement LIKE '" +self.welcomeMajorVar.get()+"%' OR ISNULL(sub.Major_Requirement)) AND "
                statement += categoryStatement
                print(statement)
                cursor.execute(statement)
                aList = cursor.fetchall()
                print("executed statement")
                nameList=[]
                for i in aList:
                    nameList.append(i[0])
                for j in nameList:
                    self.nameBox.insert(END, j)
                    self.typeBox.insert(END, "Project")
            elif(self.filterRadio.get() == "Course"):
                statement = "SELECT Name FROM (SELECT * FROM COURSE NATURAL JOIN COURSE_IS_CATEGORY)sub WHERE "
                statement += categoryStatement
                print(statement)
                cursor.execute(statement)
                aList = cursor.fetchall()
                print("executed statement")
                nameList=[]
                for i in aList:
                    nameList.append(i[0])
                for j in nameList:
                    self.nameBox.insert(END, j)
                    self.typeBox.insert(END, "Course")
            else:
                print("here")
                projectStatement = "SELECT Name FROM (SELECT * FROM PROJECT NATURAL JOIN PROJECT_REQUIREMENT NATURAL JOIN PROJECT_IS_CATEGORY)sub WHERE (sub.Designation LIKE '" + self.welcomeDesignationVar.get()+ "%' OR ISNULL(sub.Designation)) AND (sub.Year_Requirement LIKE '" +self.welcomeYearVar.get()+ "%' OR ISNULL(sub.Year_Requirement)) AND (sub.Major_Requirement LIKE '" +self.welcomeMajorVar.get()+"%' OR ISNULL(sub.Major_Requirement)) AND " 
                courseStatement = "SELECT Name FROM (SELECT * FROM COURSE NATURAL JOIN COURSE_IS_CATEGORY)sub WHERE "
                projectStatement += categoryStatement
                courseStatement += categoryStatement
                print(projectStatement)
                print(courseStatement)
                cursor.execute(projectStatement)
                aList = cursor.fetchall()
                print("executed statement")
                nameList=[]
                for i in aList:
                    nameList.append(i[0])
                for j in nameList:
                    self.nameBox.insert(END, j)
                    self.typeBox.insert(END, "Project")
                typeList=[]
                cursor.execute(courseStatement)
                bList = cursor.fetchall()
                for k in bList:
                    typeList.append(k[0])
                for l in typeList:
                    self.nameBox.insert(END, j)
                    self.typeBox.insert(END, "Course")

            cursor.close()
            db.close()
        except:
            print("can not connect to database")
                
    def resetFilter(self):
        print("reset")
        self.welcomeTitleEntry.delete(0, 'end')
        self.welcomeDesignationVar.set("Please Select")
        self.welcomeMajorVar.set("Please Select")
        self.welcomeYearVar.set("Please Select")
        for OM in self.optionMenus:
            OM.grid_forget()
        self.optionMenus = []
        self.categorySelection.set("Please Select")
        self.categories = []
        self.categories.append(self.categorySelection)
        self.numOfCategories = 1
            
        self.radio1.select()

    def viewElement(self):
        now = self.nameBox.curselection()
        nameOfElement = self.nameBox.get(now)
        print(nameOfElement)
        typeOfElement = self.typeBox.get(now)
        if(typeOfElement == "Project"):
            self.viewProject(nameOfElement)
        else:
            self.viewCourse(nameOfElement)

    def logoutMe(self):
        self.welcomeWin.withdraw()
        self.rootwin.iconify()
        print("logged out")

    def viewProject(self, name):
        self.welcomeWin.withdraw()
        self.viewProjectWin = Toplevel()
        self.viewProjectWin.title(name)
        self.viewProjectWin.configure(background='gray')

        ###slspic
        self.picFrame =Frame(self.viewProjectWin,background="gray")
        self.picFrame.pack()

        urlsls = "http://imageshack.com/a/img923/492/NJ18VG.gif"
        responsesls = urllib.request.urlopen(urlsls)
        myPicturesls = responsesls.read()
        b64_datasls = base64.encodebytes(myPicturesls)
        self.photosls = PhotoImage(data=b64_datasls)
        lsls = Label(self.picFrame, image = self.photosls)
        lsls.grid(row= 0, column = 0, sticky= E)
        #slspicc

        self.viewProjectFrame = Frame(self.viewProjectWin, background="gray", width=550)
        self.viewProjectFrame.pack(side = LEFT )

        try:

            db = pymysql.connect(host = "academic-mysql.cc.gatech.edu", user = "cs4400_Team_5",
                                 passwd = "2KZtbzKa", db = "cs4400_Team_5")
            print("connected")

            cursor = db.cursor()
            cursor.execute("SELECT * FROM PROJECT WHERE PROJECT.Name = '" + name + "';")
            aList = cursor.fetchall()

            cursor.execute("SELECT B.Category_name FROM PROJECT A JOIN PROJECT_IS_CATEGORY B ON A.Name = B.Name WHERE A.Name = '" + name + "';")
            categoryTuple = cursor.fetchall()
            categoryList = "";
            for cat in categoryTuple:
                categoryList += cat[0] + ", "

            cursor.execute("SELECT B.Requirement FROM PROJECT A JOIN PROJECT_REQUIREMENT B ON A.Name = B.Name WHERE A.Name = '" + name + "';")
            reqTuple = cursor.fetchall()
            reqList = "";
            for req in reqTuple:
                reqList += req[0] + "; "

            Label(self.viewProjectFrame, text = aList[0][0], background="gray", wraplength = 500, justify = LEFT).grid(row = 0, column= 0, padx = 25, pady = 5, sticky= W)
            Label(self.viewProjectFrame, text = aList[0][2] + " (" + aList[0][3] + ")", background="gray", wraplength = 500, justify = LEFT).grid(row = 1, column= 0, padx = 25, pady = 5, sticky= W)
            Label(self.viewProjectFrame, text = aList[0][4], background="gray", wraplength = 500, justify = LEFT).grid(row = 2, column= 0, sticky= W, padx = 25, pady = 5)
            Label(self.viewProjectFrame, text = "Designation: " + aList[0][5], background="gray", wraplength = 500, justify = LEFT).grid(row = 3, column= 0, sticky= W, padx = 25, pady = 5)
            Label(self.viewProjectFrame, text = "Estimated Number of Students: " + str(aList[0][1]), background="gray", wraplength = 500, justify = LEFT).grid(row = 6, column= 0, sticky= W, padx = 25, pady = 5) 
            Label(self.viewProjectFrame, text = "Category: " + categoryList, background="gray", wraplength = 500, justify = LEFT).grid(row = 4, column= 0, sticky= W, padx = 25, pady = 5)
            Label(self.viewProjectFrame, text = "Requirement: " + reqList, background="gray", wraplength = 500, justify = LEFT).grid(row = 5, column= 0, sticky= W, padx = 25, pady = 5)

            self.backButton = Button(self.viewProjectFrame, text = "Back", command = self.backViewProject)
            self.backButton.grid(row = 7, column = 0, padx = 5, pady = 20)

            self.applyButton = Button(self.viewProjectFrame, text = "Apply", command = lambda:self.viewApply(name))
            self.applyButton.grid(row = 8, column = 0, padx = 5, pady = 20)

            cursor.close()
            db.close()

        except:
            print ("Unexpected error:", sys.exc_info()[0])

    def backViewProject(self):
        self.viewProjectWin.withdraw()
        self.welcomeScreen()

    def viewApply(self, name):
        try:

            db = pymysql.connect(host = "academic-mysql.cc.gatech.edu", user = "cs4400_Team_5",
                                 passwd = "2KZtbzKa", db = "cs4400_Team_5")
            print("connected")

            cursor = db.cursor()

            # cursor.execute("SELECT B.Requirement FROM PROJECT_REQUIREMENT B JOIN PROJECT A ON A.Name = B.Name WHERE A.Name = '" + name + "';")
            # reqTupleTest = cursor.fetchall()
            # reqListTest = [];
            # for req in reqTupleTest:
            #     reqListTest.append(req[0].replace("students only","").replace("s only","").replace("only", "").rstrip(" "))
            # print (reqListTest)

            # cursor.execute("SELECT A.Year, A.Major, B.Dept_name FROM USER A JOIN MAJOR B WHERE A.Major = B.Name AND A.Username = '" + self.currentUser + "';")
            # userTuple = cursor.fetchall()
            # print (userTuple)
            # if(len(userTuple) != 0):
            #     userListTest = userTuple[0]
            #     print (userListTest)

            #     reqCount = 0

            #     for x in reqListTest:
            #         if x in userListTest:
            #             reqCount += 1

            #     print (len(reqListTest))
            #     print (reqCount)


                # cursor.execute("SELECT B.Requirement FROM PROJECT A JOIN PROJECT_REQUIREMENT B ON A.Name = B.Name WHERE A.Name = '" + name + "';")
                # if (len(reqListTest) == reqCount):
            #         date = datetime.datetime.now().strftime("%m/%d/%Y")
            #         cursor.execute("INSERT INTO APPLY VALUES(%s, %s, %s, %s)", (self.currentUser, name, date, "Pending"))
            #     else:
            #         print("Does not meet Requirements")
            # else:
            #     print("Student has NULL field")


            cursor.execute("""SELECT COUNT(*)
                    FROM (
                    SELECT *
                    FROM PROJECT_REQUIREMENT
                    WHERE NAME = 'Excel Peer Support Network') A
                    WHERE REQUIREMENT LIKE '%Freshman%'
                    OR REQUIREMENT LIKE '%Sophomore%'
                    OR REQUIREMENT LIKE '%Junior%'
                    OR REQUIREMENT LIKE '%Senior%'""")
            checkforYearReq = cursor.fetchall()

            passYear = True

            if (checkforYearReq[0][0] > 0):
                passYear = False
                cursor.execute("""SELECT COUNT(*)
                        FROM (SELECT B.* FROM PROJECT_REQUIREMENT B JOIN PROJECT A ON A.Name = B.Name WHERE A.Name = '""" + name +"""') A
                        JOIN (
                        SELECT A.Year FROM USER A JOIN MAJOR B WHERE A.Major = B.Name AND A.Username = '""" + self.currentUser +"""') B
                        WHERE A.Requirement LIKE CONCAT('%', B.Year, '%')""")

                yearCheck = cursor.fetchall()
                if (yearCheck[0][0] > 0):
                    passYear = True

            cursor.execute(""" SELECT COUNT(*)
                        FROM (
                        SELECT *
                        FROM PROJECT_REQUIREMENT
                        WHERE NAME = '""" + name +"""') A
                        WHERE REQUIREMENT LIKE '%%students%'""")
            checkforMajorReq = cursor.fetchall()

            passMajor = True
            if (checkforMajorReq[0][0] > 0):
                passMajor = False
                cursor.execute("""SELECT COUNT( * )
                        FROM (

                        SELECT B . *
                        FROM PROJECT_REQUIREMENT B
                        JOIN PROJECT A ON A.Name = B.Name
                        WHERE A.Name =  '""" + name +"""'
                        )A
                        JOIN (

                        SELECT A.Major, B.Dept_name
                        FROM USER A
                        JOIN MAJOR B
                        WHERE A.Major = B.Name
                        AND A.Username =  '""" + self.currentUser +"""'
                        )B
                        WHERE A.Requirement LIKE CONCAT(  '%', B.Dept_name,  '%' )
                        OR A.Requirement LIKE CONCAT(  '%', B.Major,  '%' )""")
                majorCheck = cursor.fetchall()
                if (majorCheck[0][0] > 0):
                    passMajor = True

            if (passYear and passMajor):
                date = datetime.datetime.now().strftime("%m/%d/%Y")
                cursor.execute("INSERT INTO APPLY VALUES(%s, %s, %s, %s)", (self.currentUser, name, date, "Pending"))
            else:
                print("Doesn't meet requirements")


            cursor.close()
            db.close()

        except:
            print ("Unexpected error:", sys.exc_info()[0])

    def viewCourse(self, name):
        self.welcomeWin.withdraw()
        self.viewCourseWin = Toplevel()
        self.viewCourseWin.configure(background='gray')

        ###slspic
        self.picFrame =Frame(self.viewCourseWin, background="gray")
        self.picFrame.pack()

        urlsls = "http://imageshack.com/a/img923/492/NJ18VG.gif"
        responsesls = urllib.request.urlopen(urlsls)
        myPicturesls = responsesls.read()
        b64_datasls = base64.encodebytes(myPicturesls)
        self.photosls = PhotoImage(data=b64_datasls)
        lsls = Label(self.picFrame, image = self.photosls)
        lsls.grid(row= 0, column = 0, sticky= E)
        #slspicc

        self.viewCourseFrame = Frame(self.viewCourseWin, background="gray", width=550)
        self.viewCourseFrame.pack(side = LEFT )

        try:

            db = pymysql.connect(host = "academic-mysql.cc.gatech.edu", user = "cs4400_Team_5",
                                 passwd = "2KZtbzKa", db = "cs4400_Team_5")
            print("connected")

            cursor = db.cursor()
            cursor.execute("SELECT * FROM COURSE WHERE COURSE.Name = '" + name + "';")
            aList = cursor.fetchall()

            cursor.execute("SELECT B.Category_name FROM COURSE A JOIN COURSE_IS_CATEGORY B ON A.Name = B.Name WHERE A.Name = '" + name + "';")
            categoryTuple = cursor.fetchall()
            categoryList = "";
            for cat in categoryTuple:
                categoryList += cat[0] + ", "


            Label(self.viewCourseFrame, text = aList[0][1], background="gray", wraplength = 500, justify = LEFT).grid(row = 0, column= 0, padx = 25, pady = 5, sticky= W)
            Label(self.viewCourseFrame, text = "Course Name: " + aList[0][0], background ="gray", wraplength = 500, justify = LEFT).grid(row = 1, column= 0, padx = 25, pady = 5, sticky= W)
            Label(self.viewCourseFrame, text = "Instructor: " + aList[0][2], background ="gray", wraplength = 500, justify = LEFT).grid(row = 2, column= 0, sticky= W, padx = 25, pady = 5)
            Label(self.viewCourseFrame, text = "Designation: " + aList[0][4], background ="gray", wraplength = 500, justify = LEFT).grid(row = 3, column= 0, sticky= W, padx = 25, pady = 5)
            Label(self.viewCourseFrame, text = "Estimated Number of Students: " + str(aList[0][3]), background="gray", wraplength = 500, justify = LEFT).grid(row = 6, column= 0, sticky= W, padx = 25, pady = 5)

            Label(self.viewCourseFrame, text = "Category: " + categoryList, background="gray", wraplength = 500, justify = LEFT).grid(row = 4, column= 0, sticky= W, padx = 25, pady = 5)
            
            self.backButton = Button(self.viewCourseFrame, text = "Back", command = self.backViewCourse)
            self.backButton.grid(row = 7, column = 0, padx = 5, pady = 20)
            
            cursor.close()
            db.close()

        except:
            print ("Unexpected error:", sys.exc_info()[0])

    def backViewCourse(self):
        self.viewCourseWin.withdraw()
        self.welcomeScreen()


    def meWindow(self):

        #GUI for the Me page
        self.welcomeWin.withdraw()
        self.meWin = Toplevel()
        self.meWin.title("Me")

        ###slspic

        self.picFrame =Frame(self.meWin,background="gray")
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

        self.meFrame = Frame(self.meWin)
        self.meFrame.pack()

        #Has 2 buttons, Edit Profile and My Applications 
        self.editProfileButton = Button(self.meFrame, text = "Edit Profile", command = self.toEditProfile)
        self.editProfileButton.grid(row = 0, column = 0, padx = 20, pady = 10)
        print("adding button")
        self.myApplicationButton = Button(self.meFrame, text = "My Application",command = self.viewmyAppFunc)
        self.myApplicationButton.grid(row = 2, column = 0, padx = 20, pady = 10)
        self.backButton = Button(self.meFrame, text = "Back", command = self.backToMe)
        self.backButton.grid(row = 4, column = 0, padx = 20, pady = 10)



    def viewmyAppFunc(self):
        self.meWin.destroy()
        self.viewmyApp = Toplevel()
        self.viewmyApp.title("My Applications")
        self.viewmyApp.configure(background="gray")

        self.apppicFrame =Frame(self.viewmyApp,background="gray")
        self.apppicFrame.pack()

        self.viewmyAppFrame = Frame(self.viewmyApp,background="grey")
        self.viewmyAppFrame.pack()


        ###slspic

        urlsls = "http://imageshack.com/a/img923/492/NJ18VG.gif"
        responsesls = urllib.request.urlopen(urlsls)
        myPicturesls = responsesls.read()
        import base64
        b64_datasls = base64.encodebytes(myPicturesls)
        self.photosls = PhotoImage(data=b64_datasls)
        lsls = Label(self.apppicFrame, image = self.photosls)
        lsls.grid(row= 0, column = 0, sticky= E)
        #slspicc

        print(self.currentUser)

        #Label(self.viewmyAppFrame, text = "Date",background="gray").grid(row = 0, column = 0)
        #Label(self.viewmyAppFrame, text = "Project Name",background="gray").grid(row = 0, column =1)
        #Label(self.viewmyAppFrame, text = "Status",background="gray").grid(row = 0, column = 2)


        newF = Frame(self.viewmyApp)
        newF.pack()

        self.backFrame= Frame(self.viewmyApp,background="gray")
        self.backFrame.pack()


        try:
            #connect to database
            db = pymysql.connect(host = "academic-mysql.cc.gatech.edu", user = "cs4400_Team_5",
                             passwd = "2KZtbzKa", db = "cs4400_Team_5")
            print("connected")
            cursor = db.cursor()

            cursor.execute("SELECT Date,Name,Status FROM APPLY WHERE Username = %s",(self.currentUser,))
            data = cursor.fetchall()
            print(data)
            print(len(data))

            scrollbar = Scrollbar(newF)
            scrollbar.pack(side=RIGHT, fill =Y)

            listbox1 = Listbox(newF, yscrollcommand=scrollbar.set)
            listbox2 = Listbox(newF, yscrollcommand=scrollbar.set)
            listbox3 = Listbox(newF, yscrollcommand=scrollbar.set)

            listbox1.insert(END,"DATE")
            listbox2.insert(END,"PROJECT NAME")
            listbox3.insert(END,"STATUS")

            for t in data:
                print(t)
                listbox1.insert(END,str(t[0]))
                listbox2.insert(END,str(t[1]))
                listbox3.insert(END,str(t[2]))
            listbox1.pack(side=LEFT,fill=BOTH)
            listbox2.pack(side=LEFT,fill=BOTH)
            listbox3.pack(side=RIGHT,fill=BOTH)

            listboxes = [listbox1,listbox2,listbox3]

            def onVSB(*args):
                for lb in listboxes:
                    lb.yview(*args)

            scrollbar.config(command = onVSB)
            cursor.close()
            db.close()
        except:
            #cannot connect to database
            messagebox.showerror(title = "Error",message = "Could not connect to database.")

        self.backButton = Button(self.backFrame, text = "Back",width =13,command=self.backtoMeMain)
        self.backButton.grid(row = 0, column = 0, padx = 20, pady = 10)


    def backtoMeMain(self):
        self.viewmyApp.destroy()
        self.meWindow()

    def backToMe(self):
        self.meWin.destroy()
        self.welcomeScreen()

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
        editurl = "http://imageshack.com/a/img923/4657/0CZ7BM.gif"
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
            for major in majorTuple:
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
            majorOptionMenu.grid(row = 0, column = 1,sticky=W,pady=6)

            #same concept with year for old v new users
            Label(self.editFrame, text = "Year:",background="gray").grid(row = 1, column = 0)
            yearVariable = StringVar()
            if(self.newUser):
                yearVariable.set("Freshman")
            else:
                yearVariable.set(currentUser[0][1])
            yearOptionMenu = OptionMenu(self.editFrame, yearVariable, "Freshman", "Sophomore", "Junior", "Senior", command = self.changeYear)
            yearOptionMenu.grid(row = 1, column = 1,sticky=W,pady=6)

            #once things are selected the user is no longer new
            self.newUser = False

            Label(self.editFrame, text = "Department:",background="gray").grid(row = 2, column = 0)
            self.departmentLabel = Label(self.editFrame, text = self.departmentVar.get())
            self.departmentLabel.grid(row = 2, column = 1,sticky=W,pady=6)

            self.editToWelcomeButton = Button(self.editFrame, text = "Back", command = self.editToWelcome,width=9)
            self.editToWelcomeButton.grid(row=3, column = 1, sticky=E,pady=10)
            
            cursor.close()
            db.close()
        except:
            messagebox.showerror(title = "Error",message = "Could not connect to database.")
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
            
            ##self.departmentLabel.grid_forget()
            self.departmentVar.set("")
            department = self.majorDict[major]
            self.departmentVar.set(department)
            self.departmentLabel.config(text = department)
            ##self.departmentLabel = Label(self.editFrame, text = self.departmentVar.get())
            ##self.departmentLabel.grid(row = 2, column = 1)
        except:
            messagebox.showerror(title = "Error",message = "Could not connect to database.")
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
            messagebox.showerror(title = "Error",message = "Could not connect to database.")
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
        self.viewAppButton.grid(row = 0, column = 0, pady=5, sticky =N+S+E+W)
        self.viewPopProReportButton = Button(self.chooseFunctionalityFrame, text = "View Popular Project Report", command = self.CFToViewPopPro)
        self.viewPopProReportButton.grid(row = 2, column = 0, pady=5, sticky =N+S+E+W)
        self.viewAppReportButton = Button(self.chooseFunctionalityFrame, text = "View Application Report", command = self.CFToAppReport)
        self.viewAppReportButton.grid(row = 4, column = 0,pady=5, sticky =N+S+E+W)
        self.addAProjectButton = Button(self.chooseFunctionalityFrame, text = "Add A Project", command = self.CFToAddPro)
        self.addAProjectButton.grid(row = 6, column = 0, pady=5, sticky =N+S+E+W)
        self.addACourseButton = Button(self.chooseFunctionalityFrame, text = "Add A Course", command = self.CFToAddCourse)
        self.addACourseButton.grid(row = 8, column = 0,pady=5, sticky =N+S+E+W)

        self.logoutButton = Button(self.chooseFunctionalityFrame, text = "Logout", command = self.logout)
        self.logoutButton.grid(row = 9, column = 0)


    def CFToViewApp(self):
        self.chooseFunctionalityWin.withdraw()
        self.viewApplications()
        print("View App")

    def CFToViewPopPro(self):
        print("Popular Project")
        self.chooseFunctionalityWin.withdraw()
        self.viewpopReport = Toplevel()
        self.viewpopReport.title("Popular Applications")
        self.viewpopReport.configure(background="gray")

        self.poppicFrame = Frame(self.viewpopReport,background="gray")
        self.poppicFrame.pack()

        self.viewpopReportFrame = Frame(self.viewpopReport,background="gray")
        self.viewpopReportFrame.pack()

        ###slspic

        urlsls = "http://imageshack.com/a/img923/492/NJ18VG.gif"
        responsesls = urllib.request.urlopen(urlsls)
        myPicturesls = responsesls.read()
        import base64
        b64_datasls = base64.encodebytes(myPicturesls)
        self.photosls = PhotoImage(data=b64_datasls)
        lsls = Label(self.poppicFrame, image = self.photosls)
        lsls.grid(row= 0, column = 0, sticky= E)
        #slspicc

        scrollFrame= Frame(self.viewpopReport)
        scrollFrame.pack()

        backbFrame = Frame(self.viewpopReport,background="gray")
        backbFrame.pack()

        try:
            print("here")
            #connect to database
            db = pymysql.connect(host = "academic-mysql.cc.gatech.edu", user = "cs4400_Team_5",
                passwd = "2KZtbzKa", db = "cs4400_Team_5")
            print("connected")
            cursor = db.cursor()

            cursor.execute("SELECT PROJECT.Name, COUNT(*) AS Name FROM APPLY NATURAL JOIN PROJECT GROUP BY PROJECT.Name HAVING COUNT(*) <= 10 ORDER BY COUNT(*) DESC")
            data = cursor.fetchall()

            print(data)

            scrollbar=Scrollbar(scrollFrame)
            scrollbar.pack(side=RIGHT,fill=Y)
            listbox1 = Listbox(scrollFrame, yscrollcommand=scrollbar.set)
            listbox2 = Listbox(scrollFrame, yscrollcommand=scrollbar.set)

            listbox1.insert(END,"PROJECT")
            listbox2.insert(END,"# OF APPLICANTS")

            for t in data:
                print(t)
                listbox1.insert(END,str(t[0]))
                listbox2.insert(END,str(t[1]))

            listbox1.pack(side=LEFT,fill=BOTH)
            listbox2.pack(side=RIGHT,fill=BOTH)


            listboxes = [listbox1,listbox2]

            def onVSB(*args):
                for lb in listboxes:
                    lb.yview(*args)

            scrollbar.config(command = onVSB)
            cursor.close()
            db.close()


        except:
            #cannot connect to database
            messagebox.showerror(title = "Error",message = "Could not connect to database.")

        backB = Button(backbFrame, text="Back",width =13,command=self.popBackbutton)
        backB.grid(row = 0, column= 0, padx = 20, pady= 10)

    def popBackbutton(self):
        self.viewpopReport.withdraw()
        self.chooseFunctionality()

    def CFToAppReport(self):
        print("Application Report")

    def CFToAddPro(self):
        self.chooseFunctionalityWin.withdraw()
        self.addProject()

    def CFToAddCourse(self):
        self.chooseFunctionalityWin.withdraw()
        self.addCourse()
        print("Add Course")

    def logout(self):
        self.chooseFunctionalityWin.withdraw()
        self.rootwin.iconify()
        print("logged out")

    def viewApplications(self):

        self.viewApplicationsWin = Toplevel()
        self.viewApplicationsWin.title("View Applications")

        self.viewApplicationsFrame = Frame(self.viewApplicationsWin)
        self.viewApplicationsFrame.pack()

        newFrame = Frame(self.viewApplicationsWin)
        newFrame.pack()

        scrollbar = Scrollbar(newFrame)
        scrollbar.pack(side = RIGHT, fill = Y)

        self.listbox = Listbox(newFrame, yscrollcommand=scrollbar.set)
        listbox2 = Listbox(newFrame, yscrollcommand=scrollbar.set)
        listbox3 = Listbox(newFrame, yscrollcommand=scrollbar.set)
        self.listbox4 = Listbox(newFrame, yscrollcommand=scrollbar.set)

        try:
        #connect to database
            db = pymysql.connect(host = "academic-mysql.cc.gatech.edu", user = "cs4400_Team_5",
                                 passwd = "2KZtbzKa", db = "cs4400_Team_5")
            print("connected")
            cursor = db.cursor()
            cursor.execute("SELECT Name, Major, Year, Status FROM APPLY JOIN USER WHERE APPLY.Username=USER.Username;")
            tuples = cursor.fetchall()
            print(tuples)
            for i in tuples:
                print(i)
                self.listbox.insert(END, str(i[0]))
                listbox2.insert(END, str(i[1]))
                listbox3.insert(END, str(i[2]))
                self.listbox4.insert(END, str(i[3]))
            self.listbox.insert(0, "PROJECT")
            listbox2.insert(0, 'APPLICANT MAJOR')
            listbox3.insert(0, 'APPLICANT YEAR')
            self.listbox4.insert(0, 'STATUS')
            self.listbox.pack(side=LEFT, fill=BOTH)
            listbox2.pack(side=LEFT, fill=BOTH)
            listbox3.pack(side=LEFT, fill=BOTH)
            self.listbox4.pack(side=LEFT, fill=BOTH)

            listboxes = [self.listbox,listbox2,listbox3,self.listbox4]

            def onVSB(*args):
                for lb in listboxes:
                    lb.yview(*args)

            scrollbar.config(command=onVSB)

            bottomFrame = Frame(self.viewApplicationsWin)
            bottomFrame.pack()
            print("made frame")
            self.acceptButton = Button(bottomFrame, text = "Accept", command = self.acceptApp)
            self.acceptButton.grid(row = 0, column = 0)
            self.rejectButton = Button(bottomFrame, text = "Reject", command = self.rejectApp)
            self.rejectButton.grid(row = 0, column = 1)
            self.viewAppToFunctionalityButton = Button(bottomFrame, text = "Back", command = self.viewAppToFunctionality)
            self.viewAppToFunctionalityButton.grid(row = 0, column = 2)

            cursor.close()
            db.close()
        except:
            print("can not connect to database")

    def acceptApp(self):
        now = self.listbox.curselection()
        projectName = self.listbox.get(now)
        status = self.listbox4.get(now)
        print(projectName,status)
        try:
        #connect to database
            db = pymysql.connect(host = "academic-mysql.cc.gatech.edu", user = "cs4400_Team_5",
                                 passwd = "2KZtbzKa", db = "cs4400_Team_5")
            print("connected")
            cursor = db.cursor()
            if(status == "Pending"):
                cursor.execute("UPDATE APPLY SET Status = 'Accepted' WHERE Name = %s;", (projectName,))
                db.commit()
                self.listbox4.delete(now)
                self.listbox4.insert(now, "Accepted")
            else:
                print("the status is already determined")

            cursor.close()
            db.close()

        except:
            print("can not connect to database")

    def rejectApp(self):
        now = self.listbox.curselection()
        projectName = self.listbox.get(now)
        status = self.listbox4.get(now)
        print(projectName,status)
        #lol
        try:
        #connect to database
            db = pymysql.connect(host = "academic-mysql.cc.gatech.edu", user = "cs4400_Team_5",
                                 passwd = "2KZtbzKa", db = "cs4400_Team_5")
            print("connected")
            cursor = db.cursor()
            if(status == "Pending"):
                cursor.execute("UPDATE APPLY SET Status = 'Rejected' WHERE Name = %s;", (projectName,))
                db.commit()
                self.listbox4.delete(now)
                self.listbox4.insert(now, "Rejected")
            else:
                print("the status is already determined")

            cursor.close()
            db.close()
        except:
            print("can not connect to database")

    def viewAppToFunctionality(self):
        self.viewApplicationsWin.withdraw()
        self.chooseFunctionality()

    def addProject(self):

        #GUI For Add Project Page
        #Has entry boxes for some, drop down menus for others
        self.addProjectWin = Toplevel()
        self.addProjectWin.title("Add Project")
        self.addProjectWin.configure(background= "gray")

        self.addprojectpic = Frame(self.addProjectWin, background="gray")
        self.addprojectpic.pack()

        #picc SLS
        projecturl = "http://imageshack.com/a/img923/492/NJ18VG.gif"
        projectresponse = urllib.request.urlopen(projecturl)
        myprojectPicture = projectresponse.read()
        import base64
        projectb64_data = base64.encodebytes(myprojectPicture)
        self.projectphoto = PhotoImage(data=projectb64_data)
        projectl = Label(self.addprojectpic, image = self.projectphoto)
        projectl.grid(row= 0, column = 0, sticky= E)
        #picc SLS


        self.addProjectFrame = Frame(self.addProjectWin,background="gray")
        self.addProjectFrame.pack()

        Label(self.addProjectFrame, text = "Project Name:",background="gray").grid(row = 0, column= 0)
        self.projectNameEntry = Entry(self.addProjectFrame)
        self.projectNameEntry.grid(row = 0, column = 1,pady=6)
        Label(self.addProjectFrame, text = "Advisor:",background="gray").grid(row = 1, column = 0)
        self.advisorNameEntry = Entry(self.addProjectFrame)
        self.advisorNameEntry.grid(row = 1, column = 1,pady=6)
        Label(self.addProjectFrame, text = "Advisor Email:",background="gray").grid(row = 2, column = 0)
        self.advisorEmailEntry = Entry(self.addProjectFrame)
        self.advisorEmailEntry.grid(row = 2, column = 1,pady=6)
        Label(self.addProjectFrame, text = "Descipriton:",background="gray").grid(row = 3, column = 0)
        self.projectDescriptionText = Text(self.addProjectFrame,width =35, height=8)
        self.projectDescriptionText.grid(row = 3, column = 1,pady=6)

        try:
        #connect to database
            db = pymysql.connect(host = "academic-mysql.cc.gatech.edu", user = "cs4400_Team_5",
                                 passwd = "2KZtbzKa", db = "cs4400_Team_5")
            print("connected")
            cursor = db.cursor()
            self.categories = []
            cursor.execute("SELECT * FROM CATEGORY;")
            aList = cursor.fetchall()
            self.categoryList = []
            for category in aList:
                self.categoryList.append(category[0])
            print("populated my category list")
            Label(self.addProjectFrame, text = "Category:",background="gray").grid(row = 4, column= 0)
            self.categorySelection = StringVar()
            print("made my var")
            self.categorySelection.set(self.categoryList[0])
            print("made my var")
            self.categories.append(self.categorySelection)
            self.numOfCategories = 1
            self.categoryOption = OptionMenu(self.addProjectFrame, self.categorySelection, *self.categoryList)
            self.categoryOption.grid(row = 4, column = 1,pady=6)

            self.addCategoryButton = Button(self.addProjectFrame, text = "Add Category", command = self.addProjectCategory)
            self.addCategoryButton.grid(row = 5, column = 0)

            cursor.execute("SELECT * FROM DESIGNATION;")
            aList = cursor.fetchall()
            designationList = []
            for designation in aList:
                designationList.append(designation[0])
            Label(self.addProjectFrame, text = "Designation:",background="gray").grid(row = 6, column = 0)
            self.designationVar = StringVar()
            self.designationVar.set(designationList[0])
            self.designationOption = OptionMenu(self.addProjectFrame, self.designationVar, *designationList)
            self.designationOption.grid(row = 6, column = 1,pady=6)

            Label(self.addProjectFrame, text = "Estimated Number of Students:",background="gray").grid(row = 7, column = 0)
            self.estNumStudentsEntry = Entry(self.addProjectFrame)
            self.estNumStudentsEntry.grid(row = 7, column = 1,pady=6)

            cursor.execute("SELECT * FROM MAJOR")
            majorTuple = cursor.fetchall()
            majorList = []
            for major in majorTuple:
                majorList.append(major[0])
            majorList.insert(0, "No Requirement")
            Label(self.addProjectFrame, text = "Major Requirement:",background="gray").grid(row = 8, column = 0)
            self.majorVar = StringVar()
            self.majorVar.set(majorList[0])
            self.projectMajorOption = OptionMenu(self.addProjectFrame, self.majorVar, *majorList)
            self.projectMajorOption.grid(row = 8, column = 1,pady=6)
            
            self.yearVar = StringVar()
            self.yearVar.set("No Requirement")
            Label(self.addProjectFrame, text = "Year Requirement:",background="gray").grid(row = 9, column = 0)
            self.projectYearOption = OptionMenu(self.addProjectFrame, self.yearVar, "No Requirement", "Freshman","Sophomore", "Junior","Senior")
            self.projectYearOption.grid(row = 9, column = 1,pady=6)

            cursor.execute("SELECT * FROM DEPARTMENT")
            departmentTuple = cursor.fetchall()
            departmentList = []
            for department in departmentTuple:
                departmentList.append(department[0])
            departmentList.insert(0, "No Requirement")
            Label(self.addProjectFrame, text = "Department Requirement:",background="gray").grid(row = 10, column = 0)
            self.departmentVar = StringVar()
            self.departmentVar.set(departmentList[0])
            self.projectDepartmentOption = OptionMenu(self.addProjectFrame, self.departmentVar, *departmentList)
            self.projectDepartmentOption.grid(row = 10, column = 1,pady=6)
    
            self.addProjectBackButton = Button(self.addProjectFrame, text = "Back",width=15, command = self.addProToFunctionality)
            self.addProjectBackButton.grid(row = 11, column = 0,sticky=W,pady=6)
            self.addProjectSubmitButton = Button(self.addProjectFrame, text = "Submit", command = self.submitProject,width=15)
            self.addProjectSubmitButton.grid(row = 11, column = 1,sticky=E,pady=6)

            cursor.close()
            db.close()
        
        except:
            messagebox.showerror(title = "Error",message = "Could not connect to database.")
            print("could not connect to database")

    def addProjectCategory(self):
        print('add category')
        self.categories.append(StringVar())
        self.categories[len(self.categories)-1].set(self.categoryList[0])
        self.numOfCategories += 1
        OptionMenu(self.addProjectFrame, self.categories[len(self.categories)-1], *self.categoryList).grid(row = 4, column = self.numOfCategories)

    def submitProject(self):
        projectName = self.projectNameEntry.get().strip()
        advisorName = self.advisorNameEntry.get().strip()
        advisorEmail = self.advisorEmailEntry.get().strip()
        description = self.projectDescriptionText.get("1.0",END)
        designation = self.designationVar.get()
        categories = []
        for i in self.categories:
            categories.append(i.get())
        categories = set(categories)
        estNumOfStudents = self.estNumStudentsEntry.get().strip()
        majorRestriction = self.majorVar.get()
        yearRestriction = self.yearVar.get()
        departmentRestriction = self.departmentVar.get()
        try:
        #connect to database
            db = pymysql.connect(host = "academic-mysql.cc.gatech.edu", user = "cs4400_Team_5",
                                 passwd = "2KZtbzKa", db = "cs4400_Team_5")
            print("+")
            cursor = db.cursor()
            cursor.execute("SELECT Name FROM PROJECT WHERE Name = %s;",(projectName,))
            aList = cursor.fetchall()
            print(aList)
            if(projectName != "" and advisorName != "" and advisorEmail != "" and description != "" and estNumOfStudents != ""):
                if(len(aList) == 0):
                    print("none of the entry boxes are empty")
                    print(designation)
                    print(majorRestriction)
                    print(departmentRestriction)
                    statement = "INSERT INTO PROJECT (Name, estNumOfStudents, aName, aEmail, Description, Designation) VALUES (%s,%s,%s,%s,%s,%s);"
                    data = (projectName, estNumOfStudents, advisorName, advisorEmail, description, designation)
                    cursor.execute(statement, data)
                    db.commit()
                    print("inserted project")
                else:
                    print("Project name already taken")
                    return
            else:
                print("no entry boxes can be empty")
                return
            for category in categories:
                cursor.execute("INSERT INTO PROJECT_IS_CATEGORY (Name, Category_name) VALUES (%s, %s);", (projectName, category))
                db.commit()
                print("inserted category")


            if(majorRestriction == "No Requirement"):
                majorRestriction = None
            if(yearRestriction == "No Requirement"):
                yearRestriction = None
            if(departmentRestriction == "No Requirement"):
                departmentRestriction = None

            cursor.execute("INSERT INTO PROJECT_REQUIREMENT (Name, Year_Requirement, Department_Requirement, Major_Requirement) VALUES (%s,%s,%s,%s);",(projectName, yearRestriction, departmentRestriction, majorRestriction))
            db.commit()
            print("inserted restirction")

            cursor.close()
            db.close()

        except:
            print("cannot connect to database")


    def addCourse(self):
        #GUI for add course
        print('add course')
        self.addCourseWin = Toplevel()
        self.addCourseWin.title("Add Course")
        self.addCourseWin.configure(background="gray")

        self.addcoursepic = Frame(self.addCourseWin,background="gray")
        self.addcoursepic.pack()

        #picc SLS
        courseurl = "http://imageshack.com/a/img923/492/NJ18VG.gif"
        courseresponse = urllib.request.urlopen(courseurl)
        mycoursePicture = courseresponse.read()
        import base64
        courseb64_data = base64.encodebytes(mycoursePicture)
        self.coursephoto = PhotoImage(data=courseb64_data)
        coursel = Label(self.addcoursepic, image = self.coursephoto)
        coursel.grid(row= 0, column = 0, sticky= E)
        #picc SLS

        self.addCourseFrame = Frame(self.addCourseWin,background="gray")
        self.addCourseFrame.pack()
        print('made add course frame')
        Label(self.addCourseFrame, text = "Course Number:",background="gray").grid(row = 0, column = 0)
        self.courseNumberEntry = Entry(self.addCourseFrame)
        self.courseNumberEntry.grid(row = 0, column = 1,pady=6)
        Label(self.addCourseFrame, text = "Course Name:",background="gray").grid(row = 1, column = 0)
        self.courseNameEntry = Entry(self.addCourseFrame)
        self.courseNameEntry.grid(row = 1, column = 1,pady=6)
        Label(self.addCourseFrame, text = "Instructor:",background="gray").grid(row = 2, column = 0)
        self.courseInstructorEntry = Entry(self.addCourseFrame)
        self.courseInstructorEntry.grid(row = 2, column = 1,pady=6)

        
        try:
        #connect to database
            db = pymysql.connect(host = "academic-mysql.cc.gatech.edu", user = "cs4400_Team_5", passwd = "2KZtbzKa", db = "cs4400_Team_5")
            print("connected")
            cursor = db.cursor()

        #if connected, Designation and Categories:
            cursor.execute("SELECT * FROM DESIGNATION;")
            aList = cursor.fetchall()
            designationList = []
            for designation in aList:
                designationList.append(designation[0])
            Label(self.addCourseFrame, text = "Designation:",background="gray").grid(row = 3, column = 0)
            self.designationVar = StringVar()
            self.designationVar.set(designationList[0])
            self.designationOption = OptionMenu(self.addCourseFrame, self.designationVar, *designationList)
            self.designationOption.grid(row = 3, column = 1,pady=6)

            self.categories = []
            cursor.execute("SELECT * FROM CATEGORY;")
            aList = cursor.fetchall()
            self.categoryList = []
            for category in aList:
                self.categoryList.append(category[0])
            print("populated my category list")
            Label(self.addCourseFrame, text = "Category:",background="gray").grid(row = 4, column= 0)
            self.categorySelection = StringVar()
            self.categorySelection.set(self.categoryList[0])
            print("made my var")
            self.categories.append(self.categorySelection)
            self.numOfCategories = 1
            self.categoryOption = OptionMenu(self.addCourseFrame, self.categorySelection, *self.categoryList)
            self.categoryOption.grid(row = 4, column = 1,pady=6)



            self.addCourseCategoryButton = Button(self.addCourseFrame, text = "Add Category",command= self.addCourseCategory)
            self.addCourseCategoryButton.grid(row = 5, column = 0)
            Label(self.addCourseFrame, text = "Estimated Number of Students:",background="gray").grid(row = 6, column = 0)
            self.courseEstNumOfStudents = Entry(self.addCourseFrame)
            self.courseEstNumOfStudents.grid(row = 6, column = 1,pady=6)

            self.courseBackButton = Button(self.addCourseFrame, text = "Back",width=15,command = self.addCourseToFunctionality)
            self.courseBackButton.grid(row = 7, column = 0,sticky=W,pady=6)
            self.courseSubmitButton = Button(self.addCourseFrame, text = "Submit",width=15, command = self.submitCourse)
            self.courseSubmitButton.grid(row = 7, column = 1,sticky=E,pady=6)

            cursor.close()
            db.close()

        except:
            messagebox.showerror(title = "Error",message = "Could not connect to database.")
            print("could not connect to database")


    def addCourseCategory(self):
        print('add category')
        self.categories.append(StringVar())
        self.categories[len(self.categories)-1].set(self.categoryList[0])
        self.numOfCategories += 1
        OptionMenu(self.addCourseFrame, self.categories[len(self.categories)-1], *self.categoryList).grid(row = 4, column = self.numOfCategories)

    def submitCourse(self):
        categories = []
        for i in self.categories:
            categories.append(i.get())
        categories = set(categories)
        courseNumber = self.courseNumberEntry.get()
        courseName = self.courseNameEntry.get()
        instructor = self.courseInstructorEntry.get()
        designation = self.designationVar.get()
        estNumofStudents = self.courseEstNumOfStudents.get()
        try:
        #connect to database
            db = pymysql.connect(host = "academic-mysql.cc.gatech.edu", user = "cs4400_Team_5", passwd = "2KZtbzKa", db = "cs4400_Team_5")
            print("connected")
            cursor = db.cursor()

            if(courseNumber != "" and courseName != "" and instructor != "" and estNumofStudents != ""):
                cursor.execute("INSERT INTO COURSE (Name, CourseNum, Instructor, EstNumofStud, Designation) VALUES (%s,%s,%s,%s,%s);",(courseName, courseNumber, instructor, estNumofStudents, designation))
                db.commit()
                print("inserted course")
            else:
                print("entries can not be empty")
                return

            for category in categories:
                cursor.execute("INSERT INTO COURSE_IS_CATEGORY (Name, Category_name) VALUES (%s, %s);",(courseName, category))
                db.commit()

            cursor.close()
            db.close()

        except:
            print("can not connect to database")


    def addProToFunctionality(self):
        self.addProjectWin.withdraw()
        self.chooseFunctionality()

    def addCourseToFunctionality(self):
        self.addCourseWin.withdraw()
        self.chooseFunctionality()




win = Tk()
app = cs4400Project(win)
win.mainloop()

