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

    surgery = get_surgery()
    data.append(surgery)

    referrer = get_referrer()
    data.append(referrer)

    device_after_review = get_device()
    data.append(device_after_review)

    outcome = get_outcome()
    data.append(outcome)

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
    Requests date information from the user.
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
    r = relativedelta.relativedelta(date2, date1)
    months = r.months
    years = r.years
    return f"{years}y{months}m"


def get_surgery():
    """
    Requests patient's referring surgery information from the user,
    and capitalises all words in the entered string.
    """
    print("Please enter patient's referring GP surgery\n")
    user_input = input("Enter referring surgery here: ")
    return user_input.title()


def get_referrer():
    """
    Requests's patients referrer from the user
    """
    print("Please enter patient's referrer")
    print("Example: For John Smith, enter JS\n")
    user_input = input("Enter referrer here: ")
    return user_input.upper()




def get_device():
    """
    Requests patient's inhaler device after review
    by providing a number of options selected by a number.
    Once entered, the input is then validated.
    """
    print("Please provide patient's inhaler device after review by entering matching number\n")
    while True:
        print("For Nil, enter: 0")
        print("For DPI, enter: 1")
        print("For Mouthpiece, enter: 2")
        print("For Mask - APPROPRIATE, enter: 3\n")

        user_input = input("Enter here: ")
        try:
            value = int(user_input)
        except ValueError:
            print('Please enter a number, as suggested.')
            continue
        if value == 0:
            return "Nil"
            break
        elif value == 1:
            return "DPI"
            break
        elif value == 2:
            return "Mouthpiece"
            break
        elif value == 3:
            return "Mask - APPROPRIATE"
            break
        else:
            print(f'{user_input} is not one of the available options, please try again.\n')



def get_outcome():
    """
    Requests patient outcome by providing a number of options 
    selected by a number. Once entered, the input is then validated.
    """
    outcome = ""
    comment = ""
    print("Please provide patient outcome by entering matching number\n")
    while True:
        print("For 'Commence treatment', enter: 1")
        print("For 'Increased', enter: 2")
        print("For 'Optimised', enter: 3")
        print("For 'Continue', enter: 4")
        print("For 'Alternative diagnosis', enter: 5")
        print("For 'Discontinue treatment', enter: 6\n")

        user_input = input("Enter here: ")
        try:
            value = int(user_input)
        except ValueError:
            print('Please enter a number, as suggested.')
            continue
        if value == 1:
            outcome = "Commence treatment"
            break
        elif value == 2:
            outcome = "Increased"
            option = ""
            while True:
                print("Would you like to add a comment to this outcome?\n")
                option = input("enter y or n here: ")
                if option == "y":
                    comment = input("Please detail your comment here: ")
                    break
                elif option == "n":
                    break
                else:
                    print(f'{option} is not one of the available options, please enter y or n\n')
            break
        elif value == 3:
            outcome = "Optimised"
            break
        elif value == 4:
            outcome = "Continue"
            break
        elif value == 5:
            outcome = "Alternative Diagnosis;"
            comment = input("Please detail alternative diagnosis here: ")
        else:
            print(f'{user_input} is not one of the available options, please try again.\n')



def update_patient_data(data):
    """
    Updates patient worksheet, and adds new row with the data provided
    """
    print("Updating patient worksheet...")
    worksheet = SHEET.worksheet('patients')
    worksheet.append_row(date)


# get_patient_data()
get_outcome()