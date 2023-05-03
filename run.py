import gspread
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
    print("Data should appear as follows MM/DD/YY")
    print("Example: 01/23/20\n")

    dob_str = input("Enter DoB here: ")
    print(f"Patient's Date of Birth is {dob_str}") 

get_patient_data()