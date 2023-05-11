import gspread
import time
from datetime import datetime
from dateutil import relativedelta
from google.oauth2.service_account import Credentials
import numpy

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('allergy_spreadsheet').worksheet("patients")


def get_patient_data():
    """
    Collects a range of data of varying types by calling a number of functions
    before appending them to a list called data to be appended to the spreadsheet.
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

    device_after_review = get_device("after")
    data.append(device_after_review)

    outcome = get_outcome()
    data.append(outcome)
    comment = ""
    if outcome == "Alternative diagnosis":
        while True:
            comment = input("Please detail alternative diagnosis here: ")
            if comment == "":
                print("You haven't entered anything, and an alternative diagnosis is required.\n")
            else:
                break
    data.append(comment)

    medication = get_medication()
    data.append(medication)

    device_before_review = get_device("before")
    data.append(device_before_review)

    test = get_test()
    data.append(test)

    reason = get_reason()
    data.append(reason)

    note = get_note()
    data.append(note)

    return data

def determine_id_num():
    """
    Counts the number of patients already in the data sheet and
    automatically assigns a new patient id number to the patient.
    """
    worksheet = SHEET
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




def get_device(review):
    """
    Requests patient's inhaler device before/after review
    by providing a number of options selected by a number.
    Once entered, the input is then validated.
    """
    print(f"Please provide patient's inhaler device {review} review by entering matching number\n")
    while True:
        if review == "after":
            print("1: Nil")
            print("2: DPI")
            print("3: Mouthpiece")
            print("4: Mask - APPROPRIATE\n")
        elif review == "before":
            print("1: Not on treatment")
            print("2: DPI")
            print("3: Mouthpiece")
            print("4: Mask - APPROPRIATE")
            print("5: Mask - INAPPROPRIATE")
            print("6: Breath actuated")
            print("7: No spacer")
            print("8: Other\n")



        user_input = input("Enter here: ")
        try:
            value = int(user_input)
        except ValueError:
            print('Please enter a number, as suggested.\n')
            continue
        if value == 1 and review == "after":
            return "Nil"
            break
        elif value == 2 and review == "after":
            return "DPI"
            break
        elif value == 3 and review == "after":
            return "Mouthpiece"
            break
        elif value == 4 and review == "after":
            return "Mask - APPROPRIATE"
            break
        elif value == 1 and review == "before":
            return "Not on treatment"
            break
        elif value == 2 and review == "before":
            return "DPI"
            break
        elif value == 3 and review == "before":
            return "Mouthpiece"
            break
        elif value == 4 and review == "before":
            return "Mask - APPROPRIATE"
            break
        elif value == 5 and review == "before":
            return "Mask - INAPPROPRIATE"
            break
        elif value == 6 and review == "before":
            return "Breath actuated"
            break
        elif value == 7 and review == "before":
            return "No spacer"
            break
        elif value == 8 and review == "before":
            return input("Please detail inhaler device here: ")
            break
        else:
            print(f'{user_input} is not one of the available options, please try again.\n')



def get_outcome():
    """
    Requests patient outcome by providing a number of options 
    selected by a number. Once entered, the input is then validated.
    Should the answer require a comment, this option will be provided
    and the outcome and the comment will be returned together as one cell.
    """
    outcome = ""
    comment = ""
    print("Please provide patient outcome by entering matching number\n")
    while True:
        print("1: Commence treatment")
        print("2: Increased")
        print("3: Optimised")
        print("4: Continue")
        print("5: Alternative Diagnosis")
        print("6: Discontinue treatment\n")

        user_input = input("Enter here: ")
        try:
            value = int(user_input)
        except ValueError:
            print('Please enter a number, as suggested.\n')
            continue
        if value == 1:
            outcome = "Commence treatment"
            break
        elif value == 2:
            outcome = "Increased"
            break
        elif value == 3:
            outcome = "Optimised"
            break
        elif value == 4:
            outcome = "Continue"
            break
        elif value == 5:
            outcome = "Alternative diagnosis"
            break
        elif value == 6:
            outcome = "Discontinue treatment"
            break
        else:
            print(f'{user_input} is not one of the available options, please try again.\n')
    return (f'{outcome}' + f'{comment}')



def get_medication():
    """
    Requests patient's medication after review
    by providing a number of options selected by a number.
    Once entered, the input is then validated.
    """
    medication = ""
    print("Please provide patient's medication after review by entering matching number\n")
    while True:
        print("1: Nil")
        print("2: Clenil")
        print("3: Flixotide")
        print("4: Relvar")
        print("5: Seretide")
        print("6: Symbicort")
        print("7: Qvar\n")


        drug = input("Enter here: ")
        try:
            value = int(drug)
        except ValueError:
            print('Please enter a number, as suggested.\n')
            continue
        if value == 1:
            return "Nil"
            break
        elif value == 2:
            while True:
                print("Clenil has been selected.")
                print("1: Clenil 50mcg 2pbd")
                print("2: Clenil 100mcg 1pbd")
                print("3: 8 weeks of Clenil\n")

                plan = input("Enter here: ")
                try:
                    value2 = int(plan)
                except ValueError:
                    print('Please enter a number, as suggested.\n')
                    continue
                if value2 == 1:
                    medication = "Clenil 50mcg 2pbd"
                    break
                if value2 == 2:
                    medication = "Clenil 100mcg 1pbd"
                    break
                if value2 == 3:
                    medication = "8 weeks of Clenil"
                    break
            break
        elif value == 3:
            while True:
                print("Flixotide has been selected.\n")
                print("1: Flixotide 50mcg 1pbd")
                print("2: Flixotide 50mcg 2pbd")
                print("3: Flixotide 125mcg 2pbd\n")

                plan = input("Enter here: ")
                try:
                    value2 = int(plan)
                except ValueError:
                    print('Please enter a number, as suggested.\n')
                    continue
                if value2 == 1:
                    medication = "Flixotide 50mcg 1pbd"
                    break
                if value2 == 2:
                    medication = "Flixotide 50mcg 2pbd"
                    break
                if value2 == 3:
                    medication = "Flixotide 125mcg 2pbd"
                    break
            break
        elif value == 4:
            while True:
                print("Relvar has been selected.\n")
                print("1: Relvar 92mcg")
                print("2: Relvar 184mcg\n")

                plan = input("Enter here: ")
                try:
                    value2 = int(plan)
                except ValueError:
                    print('Please enter a number, as suggested.\n')
                    continue
                if value2 == 1:
                    medication = "Relvar 92mcg"
                    break
                if value2 == 2:
                    medication = "Relvar 184mcg"
                    break
            break
        elif value == 5:
            while True:
                print("Seretide has been selected.\n")
                print("1: Seretide 50mcg 2pbd")
                print("2: Seretide 100mcg 1pbd")
                print("3: Seretide 125mcg 2pbd\n")

                plan = input("Enter here: ")
                try:
                    value2 = int(plan)
                except ValueError:
                    print('Please enter a number, as suggested.\n')
                    continue
                if value2 == 1:
                    medication = "Seretide 50mcg 2pbd"
                    break
                if value2 == 2:
                    medication = "Seretide 100mcg 1pbd"
                    break
                if value2 == 3:
                    medication = "Seretide 125mcg 2pbd"
                    break
            break
        elif value == 6:
            while True:
                print("Symbicort has been selected.\n")
                print("1: Symbicort MART 100mcg")
                print("2: Symbicort MART 200mcg")
                print("3: Symbicort 100 SMART")
                print("4: Symbicort 100mcg 2pbd\n")


                plan = input("Enter here: ")
                try:
                    value2 = int(plan)
                except ValueError:
                    print('Please enter a number, as suggested.\n')
                    continue
                if value2 == 1:
                    medication = "Symbicort MART 100mcg"
                    break
                if value2 == 2:
                    medication = "Symbicort MART 200mcg"
                    break
                if value2 == 3:
                    medication = "Symbicort 100 SMART"
                    break
                if value2 == 4:
                    medication = "Symbicort 100mcg 2pbd"
                    break
            break
        elif value == 7:
            medication = "Qvar 50mcg 2pbd"
            break
        else:
            print(f'{user_input} is not one of the available options, please try again.\n')
    return medication


def get_test():
    """
    Requests information on whether allergy testing was performed on the patient.
    """
    while True:
        print("Was allergy testing performed on the patient?\n")
        print("1: Yes")
        print("2: Yes - Adverse reaction")
        print("3: No\n")
        option = input("Enter here: ")
        if option == "1":
            test = "Yes"
            break
        elif option == "2":
            test = "Yes - Adverse reaction"
            break
        elif option == "3":
            test = "No"
            break
        else:
            print(f'{option} is not one of the available options, please enter y or n\n')
    return test


def get_reason():
    """
    Requests referral reason from the user
    by providing a number of options selected by a number.
    """
    while True:
        print("What was the reason for referral?\n")
        print("For Poor control, enter: 1")
        print("For Diagnostic testing, enter: 2\n")

        user_input = input("Enter here: ")
        try:
            value = int(user_input)
        except ValueError:
            print('Please enter a number, as suggested.\n')
            continue
        if value == 1:
            reason = "Poor control"
            break
        elif value == 2:
            reason = "Diagnostic testing"
            break
        else:
            print(f'{user_input} is not one of the available options, please try again.\n')
    return reason


def get_note():
    """
    Asks if the user wants to add any final notes regarding the patient,
    if they reply yes, they can add a comment and it will be ammended.
    """
    note = ""
    while True:
        print("Are there any general notes you would like to add?\n")
        option = input("enter y or n here: ")
        if option == "y":
            note = input("Please detail your notes here: ")
            break
        elif option == "n":
            break
        else:
            print(f'{option} is not one of the available options, please enter y or n\n')
        break
    return note


def update_patient_data(data):
    """
    Updates patient worksheet, and adds new row with the data provided
    """
    print("Updating patient worksheet...")
    patient_worksheet = SHEET
    patient_worksheet.append_row(data)
    print("Patient worksheet updated successfully.\n")
    go_back = input("To return to the main menu, press enter here: ")
    if isinstance(go_back, str):
        main()

def get_numbers(col_num):
    """
    Provides a list of the number of children referred from each practice.
    """
    print("Calculating number of patients from each practice...\n")
    columns = SHEET.col_values(col_num)
    columns.pop(0)
    columns = [x for x in columns if x != ""]
    a = numpy.array(columns)
    unique, counts = numpy.unique(a, return_counts=True)
    my_dict = (dict(zip(unique, counts))) # This code was able to be created thanks to Ozgur Vatansever and Mateen Ulhaq on https://stackoverflow.com/questions/28663856/how-do-i-count-the-occurrence-of-a-certain-item-in-an-ndarray
    for key,value in my_dict.items():
        print("{}: {}\n".format(key,value))
    print("Data complete!")
    go_back = input("To return to the main menu, press enter here: ")
    if isinstance(go_back, str):
        main()



def main():
    """
    Opens main menu which provides access to all program functions
    """
    print("Please request a task by selecting the correct number.\n")
    while True:
        print("1: File new data")
        print("2: Retrieve whole data")
        print("3: Retrieve data from specific GP surgery")
        print("4: Retrieve medicine data or average ages")
        print("5: Exit program\n")

        user_input = input("Enter here: ")
        try:
            value = int(user_input)
        except ValueError:
            print('Please enter a number, as suggested.\n')
            continue
        if value == 1:
            patient_data = get_patient_data()
            update_patient_data(patient_data)
            break
        elif value == 2:
            data_menu()
            break
        elif value == 3:
            data_menu(input("Enter GP surgery here: "))
            break
        elif value == 4:
            outcome = "Continue"
            break
        elif value == 5:
            print("Goodbye")
            break
        else:
            print(f'{user_input} is not one of the available options, please try again.\n')


def data_menu():
    """
    Opens a new menu which provides access to worksheet-wide data.
    """
    
    print("Please specify required data.\n")
    while True:
        print("1: Retreive number of children from each practice")
        print("2: Retrieve number of reasons for referrals")
        print("3: Retrieve number of children per outcome group")
        print("4: Retrieve number of children per inhalation device at referral")
        print("5: Retrieve number of children per inhalation device after review")
        print("6: Retrieve number of children: who had recieved allergy testing")
        print("7: Retreive number of children with an alternative diagnosis\n")

        user_input = input("Enter here: ")
        try:
            value = int(user_input)
        except ValueError:
            print('Please enter a number, as suggested.\n')
            continue
        if value == 1:
            get_numbers(5)
            break
        elif value == 2:
            get_numbers(13)
            break
        elif value == 3:
            get_numbers(8)
            break
        elif value == 4:
            get_numbers(11)
            break
        elif value == 5:
            get_numbers(7)
            break
        elif value == 6:
            get_numbers(12)
            break
        elif value == 7:
            get_numbers(9)
            break
        else:
            print(f'{user_input} is not one of the available options, please try again.\n')



print("Welcome to CAC data automation.\n")
main()


