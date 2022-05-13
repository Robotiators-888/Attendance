import pythonClient

# print a pickle
def printPickle(pickleName):
    data = pythonClient.waitForReadPickle(pickleName)
    print(data)
    #print out in rows
    # for row in data:
    #     print(row)

printPickle("data/UploadIndex.pickle")