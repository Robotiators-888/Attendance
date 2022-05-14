from cgitb import text
from os.path import exists
import datetime
import gspread
import time
from oauth2client.service_account import ServiceAccountCredentials
import gspread_formatting

#console colors
BLUE = '\033[94m'
RED = '\033[91m'
ENDC = '\033[0m'


class sheets:
    def __init__(self, sheetName):
        self.sheet = self.getSpreadsheet(sheetName)
        self.setupSheet(self.sheet)
        self.names = self.getSheetNames(self.sheet)
        self.dates = self.getSheetDates(self.sheet)



        # def setupSheet(self, sheet):
        #     setupSheet(sheet)

        # def sendHours(self, name, hours,date=datetime.datetime.now()):
        #     sendHours(self.sheet, name, hours,date,self.names,self.dates)
        # def login(self, name):
        #     login(self.sheet, name)
        # def logout(self, name):
        #     logout(self.sheet, name)
        # def getSheetNames(self):
        #     return getSheetNames(self.sheet)
        # def getSheetDates(self):
        #     return getSheetDates(self.sheet)

    def getSpreadsheet(self,sheetName):
        scope = ['https://spreadsheets.google.com/feeds',
                'https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_name(
            'AttendanceKey.json', scope)
        client = gspread.authorize(creds)

        # check if sheet exists
        canOpenSheet = False
        try:
            client.open(sheetName).sheet1
            print('opened sheet', sheetName)
            canOpenSheet = True
        except Exception as e:
            print("could not open sheet", sheetName,e)

            print(RED+"(Check your internet connection!)"+ENDC)
            canOpenSheet = False

        # open and return sheet
        if (canOpenSheet):  # if the sheet exists
            sheet = client.open(sheetName).sheet1
            return sheet
        else:
            print(RED+"sheet does not exist or there is error accessing it"+ENDC)
            return None

    # first row is "names" second row is "total hours"


    def setupSheet(self,sheet):
        totalNumCols = sheet.col_count
        print("totalNumCols", totalNumCols)

        # insert many new colums until have 180!
        while (totalNumCols < 180):
            try:
                sheet.insert_cols(["","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","","",""],20)
            except:
                print("error inserting cols but it still works")
            # update col_count
            totalNumCols += 18
            print("totalNumCols", totalNumCols)



        # create header row
        headerRow = ["Name", "Total Hours","Logged In?"] # total hour summer:
        sheet.update_cell(1, 1, headerRow[0])
        sheet.update_cell(1, 2, headerRow[1])
        sheet.update_cell(1, 3, headerRow[2])

        headerFormat = gspread_formatting.cellFormat(
            backgroundColor=gspread_formatting.color(1, 0.9, 0.9),
            textFormat=gspread_formatting.textFormat(
                bold=True, foregroundColor=gspread_formatting.color(1, 0, 1)),
            horizontalAlignment='CENTER'
        )
        textFormat = gspread_formatting.cellFormat(
            horizontalAlignment='CENTER'
        )
        gspread_formatting.format_cell_range(sheet, '1:1', headerFormat)
        gspread_formatting.format_cell_range(sheet, '2:1000', textFormat)


    # row 1 names, row 2 hours

    # row 1 names, row 2 hours
    # uses index in names list to find row of name
    # offset is how many rows to skip
    def findName(self,name):
        offset = 2
        # check if name in names list
        if (name in self.names):
            print("found name index:", self.names.index(name))
            return self.names.index(name) + offset
        else:
            print("name not found")
            # if name not found add to list
            self.names.append(name)
            print("names list:", self.names, "length:", len(self.names))
            # sheetIndex
            sheetIndex =len(self.names) + offset-1

            # add name to sheet
            self.sheet.update_cell(sheetIndex, 1, name)
            #update total hours
            sumFunction = "=SUM(D" + str(sheetIndex) + ":EE" + str(sheetIndex) + ")"
            self.sheet.update_cell(sheetIndex, 2, sumFunction)

            return len(self.names) + offset - 1



    #todayDate is a string
    def findDate(self,todayDate):
        offset = 4
        # check if todayDate is in date list
        if (todayDate in self.dates):
            print("found date index:", self.dates.index(todayDate))
            return self.dates.index(todayDate) + offset
        else:
            print("date not found")
            # if date not found add to list
            self.dates.append(todayDate)
            print("dates list:", self.dates, "length:", len(self.dates))

            # add date to sheet
            self.sheet.update_cell(1, len(self.dates) + offset-1, todayDate)
            return len(self.dates) + offset - 1
        

    def sendHours(self, name, hours,date=datetime.datetime.now()):
        print("sending hours")

        todayDate = date.today().strftime("%m/%d/%Y")
        # search row 1 for name
        row = self.findName(name)
        col = self.findDate(todayDate)

        # 4th col onward are dates
        self.sheet.update_cell(row, col, str(hours))


    #row 3: is logged in
    def login(self,name):
        row = self.findName(name)
        self.sheet.update_cell(row, 3, "yes")
    def logout(self,name):
        row = self.findName(name)
        self.sheet.update_cell(row, 3, "no")

        # returns a list of all names in the sheet
        # names start (2,1) and go down to the end
    def getSheetNames(self,sheet):
            row = 2
            names = []
            while (True):
                cell = sheet.cell(row, 1).value
                if (cell == "" or cell == None):
                    break
                names.append(cell)
                row += 1
            return names

        # returns a list of all dates in the sheet
        # dates start (1,4) and go right to the end
    def getSheetDates(self,sheet):
        col = 4
        dates = []
        while (True):
            cell = sheet.cell(1, col).value
            if (cell == "" or cell == None):
                break
            dates.append(cell)
            col += 1
        return dates


# sheetName = "AttendanceOffSeason2022"
# sheetObject = sheets(sheetName)

# print("names", sheetObject.names)
# print("dates",  sheetObject.dates)

# print("find name will row:", sheetObject.findName("888"))


# # challenge the system with a bunch of diferent names
# sheetObject.sendHours("test", "1")
# sheetObject.sendHours("te232st", "2")
# sheetObject.sendHours("test", "3")
# sheetObject.sendHours("test", "4")
# sheetObject.sendHours("test", "5")
# sheetObject.sendHours("setup", "888")
# sheetObject.sendHours("setup-1", "1")
# sheetObject.sendHours("setup-2", "2")
# sheetObject.sendHours("setup-3", "3")
# sheetObject.sendHours("setup-4", "4")
# sheetObject.sendHours("setup-5", "5")
# sheetObject.sendHours("setup-6", "6")
# sheetObject.sendHours("setup-7", "7")
# sheetObject.sendHours("setup-8", "8")
# sheetObject.sendHours("setup-9", "9")
# sheetObject.sendHours("setup-10", "10")




