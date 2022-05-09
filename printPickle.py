import pythonClient

# print a pickle
def printPickle(pickleName):
    data = pythonClient.waitForReadPickle(pickleName)
    #print out in rows
    for row in data:
        print(row)

printPickle("data/LoggedIn.pickle")