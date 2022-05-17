import pythonClient
import time
import sheets
import os
sheetName = "AttendanceOffSeason2022Test" 
sheetObject = sheets.sheets(sheetName)

#console colors
BLUE = '\033[94m'
RED = '\033[91m'
ENDC = '\033[0m'

def mainLoop():
    """ main loop for uploading data """

    uploadIndex = 0
    tempUploadIndex = pythonClient.waitForReadPickle("data/UploadIndex.pickle")
    if (tempUploadIndex != []):
        uploadIndex = tempUploadIndex   
    data = None
    modifiedTime = 0

    # upload index is the pickle list index of the last user that was uploaded 



    while True:
        """ loop waits for new data in pickle list """
        """ then uploads data """
        """ increases upload index """
        """ if index of data is greater than upload index, upload data """

        """ pickle list is a file called "attendance.pickle"  containing a list of login/logout data """

        #check if new data is available
        # get modified time of data
        # if modified time is newer than the last modified time
        #   getData
        # FIRST CHECK IF attendance.pickle exists!?
        if (os.path.isfile("data/attendance.pickle")):
            currentModifiedTime = os.path.getmtime("data/attendance.pickle")
            if (currentModifiedTime > modifiedTime):
                modifiedTime = currentModifiedTime
                # get the data from the pickle
                data = getData()
                #if new data is available, update the sheet
                if (data != None or data != []):
                    while (uploadIndex < len(data)):
                        uploadData(data[uploadIndex])
                        print('uploadIndex',uploadIndex)
                        uploadIndex += 1
                        pythonClient.waitForWritePickle("data/UploadIndex.pickle",uploadIndex)
        else:
            print(BLUE+"no attendance.pickle (Try logging in a user)"+ENDC)
        time.sleep(1)

def getData() -> list:
    """ get data from pickle list """

    """ pickle list is a list of login/logout data """

    """ login/logout data object format shown below """

    return pythonClient.waitForReadPickle("data/attendance.pickle")

#user:
# [
#    name,
#   seconds logged in,
#   login time,
#   Logged in/logged out
# ]

    #example:
            # user,
            # 0,
            # tempHour[pin],
            # dt.datetime.now(),
            # "Logged in"

# userData is a single list from the pickle list
def uploadData(user):
    """ uploads data to the google sheet """


    userName = user[0]
    loginSeconds = user[1]
    loginTime = user[2]
    isLoggedIn = user[4]

    loginHours = round(loginSeconds/3600,2)

    print("uploading data",userName,loginHours,loginTime,isLoggedIn)
    if (len(user) > 0):
        if (isLoggedIn == "Logged in"):
            print('logged in')
            sheetObject.login(user[0])
        elif (isLoggedIn == "Logged out"):
            print('logged out')
            sheetObject.logout(userName)
            sheetObject.sendHours(userName, loginHours, loginTime)

mainLoop()
