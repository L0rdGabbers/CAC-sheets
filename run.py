import gspread
import time
from datetime import datetime
from dateutil import relativedelta
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('allergy_spreadsheet')


def get_patient_data():
    """
    Collects a range of data of varying types by calling a number of functions
    before appending them to the allergy spreadsheet althogether.
    """
    print("Collecting new patient data.\n")
    data = []

    id = determine_id_num()
    data.append(id)

    dob = get_date("patient's DoB")
    data.append(dob)

    referral_date = get_date("referral date")
    data.append(referral_date)

    age = determine_age(dob, referral_date)
    data.append(age)
    
    print(data)

def determine_id_num():
    """
    Counts the number of patients already in the data sheet and
    automatically assigns a new patient id number to the patient.
    """
    worksheet = SHEET.worksheet('patients')
    rows = len(worksheet.get_all_values()) #This counts the number of rows with data, including the headers. It already equals the number of the next patient.
    return rows

def get_date(date_type):
    """
    Requests patient's DoB information from the user.
    Runs a while loop to collect a valid string in the MM/DD/YYYY date format
    via the terminal.
    """
    while True:
        print(f"Please enter {date_type}.")
        print("Data should appear as follows MM/DD/YYYY")
        print("Example: 01/23/2020\n")

        dob_str = input(f"Enter {date_type} here: ")

        if validate_date(dob_str):
            print("Date is valid!\n")
            return dob_str
            break


def validate_date(date):
    """
    Inside the try, confirms whether string values follow the mm/dd/yyyy format.
    Raises ValueError, if string does not follow this format.
    """
    try:
        valid_date = time.strptime(date, '%m/%d/%Y')
    except ValueError:
        print(f'Invalid date: {date} does not match the MM/DD/YYYY format, please try again\n')
        return False
    
    return True


def determine_age(d1,d2):
    """
    Calculates the age of the child on the date of the referral in the 
    #y#m format.
    """
    date1 = datetime.strptime(str(d1), '%m/%d/%Y') #This code was able to be created thanks to Thayif Kabir on https://stackoverflow.com/questions/56911490/calculate-the-months-between-two-dates
    date2 = datetime.strptime(str(d2), '%m/%d/%Y')
    print (date2, date1)
    r = relativedelta.relativedelta(date2, date1)
    months = r.months
    years = r.years
    return f"{years}y{months}m"


def update_patient_data(data):
    """
    Updates patient worksheet, and adds new row with the data provided
    """
    print("Updating patient worksheet...")
    worksheet = SHEET.worksheet('patients')
    worksheet.append_row(date)


get_patient_data()