from tkinter import *
from pythonClient import login,logout, waitForWritePickle
from PIL import Image, ImageTk
import pythonClient
import registerGui


class LogHourForm:

    def __init__(self):
        self.loggedIn = pythonClient.waitForReadPickle("data/loggedIn.pickle") # if no file found returns []

        # Make a tkinter form for registering users using username and pin
        # Display a sucess message if the user is registered else display failure message
        self.window = Tk()
        self.window.title("Log Hours")
        self.window.geometry("500x500")
        self.window.bind("<Return>",lambda x: self.chooser())


        # Make a label for pin
        lbl_pin = Label(self.window, text="Pin")
        lbl_pin.pack(anchor='center')


        # Make a textbox for pin
        self.pin = Entry(self.window, width=10)
        self.pin.pack(anchor='center')


        btn_submit = Button(self.window, text="Submit", command=self.chooser)
        btn_submit.pack(anchor='center')

        # Register button
        btn_register = Button(self.window, text="Open Register", command=self.registerForm)
        btn_register.pack(anchor='ne')

        self.msg = Label(self.window)
        self.msg.pack(anchor='center')


        # Image stuff
        image888 = Image.open("888logo2.png")
        image888 = image888.resize((400,400), Image.ANTIALIAS)
        test = ImageTk.PhotoImage(image888)

        imageLabel = Label(self.window,image=test)
        imageLabel.image = test

        imageLabel.pack(anchor='center', side=BOTTOM)

        self.window.after(1000, self.logOutForgotLogin) 
        self.window.mainloop()

    def registerForm(self):
        registerGui.RegisterForm()
        

    def loginUser(self,pin):
        self.msg.configure(text=login(pin))

    def logOutUser(self,pin,ignoreHours=False):
        self.msg.configure(text=logout(pin, ignoreHours))

    def chooser(self):

        pinLog = self.pin.get()

        if pinLog in self.loggedIn:
            self.logOutUser(pinLog)
            self.pin.delete(0,END)
            self.loggedIn.remove(pinLog)
        else:
            self.loginUser(pinLog)
            self.loggedIn.append(pinLog)
            self.pin.delete(0,END)
        #INFO: invalid pins will be sent to LoggedIn.pickle, but not to attendance.pickle
        # so data for invalid pins will not be uploaded, but can be found as logged in pins
        print(self.loggedIn)
        waitForWritePickle("data/loggedIn.pickle",self.loggedIn)
        waitForWritePickle("data/tempHour.pickle",pythonClient.tempHour)
    

        



# Start the application
LogHourForm()


