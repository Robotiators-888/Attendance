import pythonClient
import time
import sheets
import os
sheetName = "AttendanceOffSeason2022" 
sheetObject = sheets.sheets(sheetName)

def mainLoop():
    uploadIndex = 0
    tempUploadIndex = pythonClient.waitForReadPickle("data/UploadIndex.pickle")
    if (tempUploadIndex != []):
        uploadIndex = tempUploadIndex   
    data = None
    modifiedTime = 0
    while True:
        #check if new data is available
        # get modified time of data
        # if modified time is newer than the last modified time
        #   getData
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
        time.sleep(1)

def getData():
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