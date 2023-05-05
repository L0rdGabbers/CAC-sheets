import gspread
import time
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

def get_patient_dob():
    """
    Adds new patient information to the allergy spreadsheet
    """
    print("Collecting new patient data.\n")
    while True:
        print("Please enter patient's date of birth.")
        print("Data should appear as follows MM/DD/YYYY")
        print("Example: 01/23/2020\n")

        dob_str = input("Enter DoB here: ")

        if validate_date(dob_str):
            print("Date is valid!")
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

dob = get_patient_dob()