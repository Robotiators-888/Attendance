# Attendance
Hour logging program

with Google sheets intergration and local storage to prevent data loss

﹀﹀ see bottom for common problems/issues ﹀﹀

## Running the Program

Run registering program with:
```
python3 registerGui.py
```

Run hour-logging program with: 
```
python3 authGui.py

python3 dataUploader.py

```

## Install all packages

``` 
pip install gspread oauth2client gspread_formatting pillow playsound
```


## Set up Google Sheets integrations

Download AttendanceKey from google drive into this folder

path: Robot(Students Mentors)/AttendanceInfo/New Attendance System/AttendanceKey.json

**Do not commit AttendanceKey.json to the repo! this is a private key!**


## Creating a new sheet:

Create a new google sheet and share with the following email: attendance@attendance-188719.iam.gserviceaccount.com

In dataUploader.py change varible sheetName to the name of the sheet you created

## Common Problems/Issues

### this sections shows common issues and how to fix them

``` FileNotFoundError: [Errno 2] No such file or directory: 'AttendanceKey.json' ```

- fix: see section Set up Google Sheets integrations

``` File blocked [Errno 2] No such file or directory: 'data/tempHour.pickle' ```

- fix: create a folder named "data", in this folder 


``` TypeError: can only concatenate str (not "PermissionError") to str ```

- fix: close any programs acessing "pins.csv", (on Windows only one program can view a file at a time)

``` FileNotFoundError: [WinError 2] The system cannot find the file specified: 'data/attendance.pickle' ```

- fix: try logging in a user (logging in creates "attendance.pickle")
