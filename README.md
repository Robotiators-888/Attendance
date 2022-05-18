# Attendance
Hour logging program

with Google sheets intergration and local storage to prevent data loss

made with python3

﹀﹀ see bottom for common problems/issues ﹀﹀

## Install all packages

``` 
pip install gspread oauth2client gspread_formatting pillow playsound
```

## Set up Google Sheets integrations

Download AttendanceKey from Google Drive into this folder

https://drive.google.com/file/d/1IGdCRpVJ-9u8LVIXyxxpkptcCYXX9_Oc/view?usp=sharing

**Do not commit AttendanceKey.json to the repo! this is a private key!**

**Google Drive Links to AttendanceKey.json must be Restricted!**


## Creating a new sheet:

Create a new google sheet and share with the following email: attendance@attendance-188719.iam.gserviceaccount.com

In dataUploader.py change varible sheetName to the name of the sheet you created

## Running the Program

Run hour-logging programs in seperate terminals with: 
```
python3 authGui.py
```
```
python3 dataUploader.py
```

To register a new user, click Open Register button and Registering form will open


## Common Problems/Issues

### This section shows common issues and how to fix them

``` FileNotFoundError: [Errno 2] No such file or directory: 'AttendanceKey.json' ```

- fix: see section Set up Google Sheets integrations

``` File blocked [Errno 2] No such file or directory: 'data/tempHour.pickle' ```

- fix: create a folder named "data", in the same folder as dataUploader.py 


``` (ON GUI) Error in registering: <class: 'PermissionError> ```

- fix: close any programs acessing "pins.csv", (on Windows only one program can view a file at a time)

``` FileNotFoundError: [WinError 2] The system cannot find the file specified: 'data/attendance.pickle' ```

- fix: try logging in a user (logging in creates "attendance.pickle")

## Updating the code

First, in Git BASH:
```git clone https://github.com/Robotiators-888/Attendance.git```

Second, make your changes. 
- pythonClient.py handles the "backend" of the program (login, logout, and register functionality)
- authGui.py and registerGui.py handle the "frontend" of the program (Tkinter GUI)
- dataUploader.py and sheets.py handle the uploading of data from the Python client to the Google sheet
- Streamlit website is on a different repo that can be viewed [here](https://github.com/KevinH45/AttendanceWebsite)
- **DO NOT PUSH AttendanceKey.json ONTO THE GITHUB REPO**

Finally, in Git BASH:

- cd into your directory
-  ``` git add -A ```
- ```git commit -m "your message"```
- ```git push origin main```
