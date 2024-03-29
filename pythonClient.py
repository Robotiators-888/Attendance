import datetime as dt
from csv import writer, DictReader
from re import T
import sheets
import _thread as thread
import time
import pickle
import os
import subprocess







#waitForReadPickle: keeps trying until it reads a pickle file and returns the data, if no file found returns [] and creates a file
def waitForReadPickle(path):
    read = False
    data = None
    while (not read):
        try:
            # if file does not exist create one
            if not os.path.isfile(path):
                with open(path, "wb") as f:
                    print("created pickle")
                    pickle.dump([], f)
            with open(path, "rb") as f:
                print("opened pickle")
                data = pickle.load(f)
                print("loaded pickle", data)
            read = True
        except Exception as e:
            print("File blocked",e)
        time.sleep(0.1)
    return data

#waitForWritePickle: keeps trying until it writes a pickle file
def waitForWritePickle(path,data):
    written = False
    while (not written):
        try:
            with open(path, "wb") as f:
                pickle.dump(data, f)
            written = True
            print("pickle written")
        except Exception as e:
            print("File blocked:",e)
        time.sleep(0.1)



global tempHour
# tempHour = {
#     # 'pin': loginTime
# }
tempHourPickle = waitForReadPickle("data/tempHour.pickle") # [] if no file found
if (tempHourPickle == []):
    tempHour = {}
else:
    tempHour = tempHourPickle


def nameExits(name):
    '''
    Returns True if the name exists in the pins.csv file
    '''
    with open('pins.csv','r') as file:
        csv_reader = DictReader(file)
        for row in csv_reader:
            if row['name'] == name:
                return True
    return False

def getUserFromPin(pin):
    '''
    Returns the name of the user from the pin
    Returns None if the pin is not found
    '''

    with open('pins.csv','r') as file:
        csv_reader = DictReader(file)
        for row in csv_reader:
            if row['pin'] == pin:
                return row['name']

    return None

def login(pin):

    '''login(pin) logs in the user with the given pin. it updates the status of the user in the Google sheet

    Returns "Invalid Pin" if the pin is not found
    Returns "Logged in NAME at TIME" if the pin is found
    
    '''
    print("login")
    user = getUserFromPin(pin)

    if user is None:
        return "Invalid Pin"
    else:
        tempHour[pin] = dt.datetime.now()

        
        data = waitForReadPickle("data/attendance.pickle")
        data.append([
            user,
            0,
            tempHour[pin],
            dt.datetime.now(),
            "Logged in"
        ])
        waitForWritePickle("data/attendance.pickle",data)

        return "Logged in "+user+" at "+str(tempHour[pin])

def logout(pin, ignoreHours=False):
    '''logout(pin) logs out the user with the given pin. it updates the status+hours of the user in the Google sheet

    Returns "Invalid Pin" if the pin is not found
    Returns "Logged out NAME at TIME" if the pin is found
    Returns "(Try logging in again) error logging in" if the user is not logged in/error in system
    Returns "Forgot to logout, you get 2.5 hours" if the user forgets to logout

    
    '''
    forgotLogout = False
    print("logout")
    if ignoreHours:
        user = getUserFromPin(pin)

        if user is None:
            return ""
        else:
            tempHour.pop(pin)
            return ""
    else:
        user = getUserFromPin(pin)

        if user is None:
            return "Invalid Pin"
        else:
            try:
                currentSeconds = (dt.datetime.now() - tempHour[pin]).total_seconds()
                # check if login happened on a diferent day than today
                forgotLogout = False
                if (dt.datetime.now().date() != tempHour[pin].date()):
                    forgotLogout = True
                    #set hours to 2.5
                    currentSeconds = 2.5*60*60

                # test of read and write
                data = waitForReadPickle("data/attendance.pickle")
                data.append([
                    user,
                    currentSeconds,
                    tempHour[pin],
                    dt.datetime.now(),
                    "Logged out"

                ])
                waitForWritePickle("data/attendance.pickle",data)

                tempHour.pop(pin)
            except KeyError:
                return "(Try logging in again) error logging in"
            if forgotLogout:
                return "Forgot to logout, you get 2.5 hours"
            else:
                return "Logged out "+user+" at "+str(dt.datetime.now())


def register(name,pin):
    '''register(name,pin) registers the user and adds them on the Google sheet and pins.csv

    Returns "Registered NAME" if the user is registered successfully
    Returns "Error in registering ERROR" if the user is not registered successfully
    
    '''
    try:
        with open('pins.csv','a') as file:
            csv_writer = writer(file)
            csv_writer.writerow([pin,name])
        return "Registered "+name
    except Exception as e:
        print(e)
        return "Error in registering: "+ str(e)



