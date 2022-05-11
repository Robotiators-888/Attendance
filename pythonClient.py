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
                return "Not logged out, you are not logged in"
            return "Logged out "+user+" at "+str(dt.datetime.now())


def register(name,pin):
    try:
        with open('pins.csv','a') as file:
            csv_writer = writer(file)
            csv_writer.writerow([pin,name])
        return "Registered "+name
    except Exception as e:
        print(e)
        return "Error in registering: "+e



