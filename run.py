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

def get_patient_data():
    """
    Adds new patient information to the allergy spreadsheet
    """
    print("Collecting new patient data.")
    print("Please enter date of birth.")
    print("Data should appear as follows MM/DD/YYYY")
    print("Example: 01/23/2020\n")

    dob_str = input("Enter DoB here: ")
    validate_date(dob_str)
    print(f"Patient's Date of Birth is {dob_str}")


def validate_date(date):
    """
    Inside the try, confirms whether string values follow the mm/dd/yyyy format.
    Raises ValueError, if string does not follow this format.
    """
    try:
        valid_date = time.strptime(date, '%m/%d/%Y')
    except ValueError as e:
        print(f'Invalid date: {e}, please try again\n')

get_patient_data()