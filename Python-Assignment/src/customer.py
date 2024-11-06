
import modules.file_manage as fm
import modules.ext_funcs as ext
import datetime
from datetime import date
import time
import os
import re

def clear():
    os.system('cls')
    print("\n")

def assign_seat_business(n):
    letters = "ABCD"
    seat = f"{(n-1)//4 + 1}{letters[(n-1)%4]}"
    return seat

def show_meal_menu(key):
    print(f"The meals provided for the flight {ext.bold(key)} is as shown:\n")
    index, entry = fm.query_key('flights', key)
    meals = entry[12].split(",")
    for i in range(len(meals)):
        meals[i] = [str(i+1)] + [meals[i]]
    menu_header = ["No.", "Meal"]
    
    ext.view_table(menu_header, meals)
    return meals

def assign_seat_economy(n):
    letters = "ABCDEF"
    seat = f"{(n-1)//6 + 1}{letters[(n-1)%6]}"
    return seat

def compare_datetime(input_datetime_str):
    print(input_datetime_str)
    current_datetime = datetime.datetime.now()
    input_datetime = datetime.datetime.strptime(input_datetime_str, "%Y-%m-%d %H:%M:%S")
    if input_datetime > current_datetime:
        return True
    elif input_datetime < current_datetime:
        return False
    else:
        return True

def show_seat(chosen_scheduleID):
    index, entry = fm.query_key("flights",chosen_scheduleID)
    display_fields = ["Flight No", "Economy Seats", "Business Seats"]
    display_entries = [[entry[2], entry[10], entry[11]]]
    return display_fields, display_entries

def show_flight(chosen_dest,field_names):
    relative_flights = fm.query_field_strict("flights", "Arr Airport",chosen_dest)
    
    field_names = ["Option"] + field_names

    for i in range(len(relative_flights)):
        relative_flights[i] = [str(i+1)] + relative_flights[i]

    display_fields1, display_entries1 = ext.remove_fields(field_names,  relative_flights, ["Schedule ID","Airline ID","Status", "In Flight Menu", "In Flight Services",])
    return display_fields1, display_entries1, relative_flights

def view_flight():
    field_names, entries = fm.read_file('flights')
    display_fields1, display_entries1 = ext.remove_fields(field_names, entries, ["Schedule ID","Airline ID", "Economy Seats", "Business Seats", "In Flight Menu", "In Flight Services",])

    ext.view_table(display_fields1, display_entries1)
    print()
  
def generate_random_code():
    seed = int(time.time() * 1000)
    code = ""

    for _ in range(5):
        random_num = (seed % 36)

        if random_num < 10:
            code += chr(random_num + ord('0'))
        else:
            code += chr(random_num - 10 + ord('A'))
        seed = seed // 36

    return code

def validate_email(email):
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    match = re.match(pattern, email)
    if match:
        return True
    else:
        return False

def validate_passport(ID):
    pattern = r'^[A-Z0-9]+$' 

    match = re.match(pattern, ID)

    if match:
        return True
    else:
        return False

def validate_contact_number(phone_number):
    pattern = r'^[+\-0-9]+$' 

    match = re.match(pattern, phone_number)

    if match:   
        return True
    else:
        return False
    
def validate_date(value):
    try:
        date.fromisoformat(value)
    except:
        return False
    return True

def book_flight(user_name):

    #get data from the files
    field_names, all_flights = fm.read_file('flights')
    b_field_names, b_entries = fm.read_file('bookings')
    file_index, customer_details = fm.query_key("customers", user_name)
    choice = sorted_flight(all_flights)
    
    display_choice = []
    for i in range(len(choice)):
        display_choice.append([str(i+1), choice[i]])
    
    """SHOW MENU"""
    #get and validate choosen destination
    while True:
        clear()
        print(ext.bold("Flights Booking"))
        ext.view_table(["No.", "Destination"], display_choice)
        
        try:
            destination = int(input("Please choose your destination: "))
            if destination in range(1, len(choice) + 1):
                break
            else:
                clear()
                print("\nPlease enter a proper destination!\n")
                input("Press Enter to continue ")
                clear()
        except:
            clear()
            print("\nPlease enter a proper destination!\n")
            input("Press Enter to continue ")
            clear()
            

    #Choose Flights to the destination
    display_fields1, display_entries1, relative_flights= show_flight(choice[destination-1],field_names)
    while True:
        try:
            clear()
            ext.view_table(display_fields1, display_entries1)
            select_flight = int(input("\nEnter flight of interest: "))
            if select_flight in range(1, len(display_entries1)+1):
                break
            else:
                clear()
                print("Please enter a proper option!!!!!!!!!!!!!!")
                input("\nPress Enter to continue ")
                clear()
        except:
            clear()
            print("Please enter a proper option!!!!!!!!!!!!!!")
            input("\nPress Enter to continue ")
            clear()
    #Chosen Flights data
    selected_flight = relative_flights[select_flight-1]
    selected_flight_key = relative_flights[select_flight-1][1]
    
    #Seat Selection
    display_class, display_no_of_seat = show_seat(selected_flight_key)
    view_seats_fields = ["No.", "Seat Type", "Ticket Price"]
    view_seats = [["1", "Economy", selected_flight[15]], ["2", "Business", selected_flight[16]]]
    
    while True:
        clear()
        print(f"The seats available for the flight {ext.bold(selected_flight_key)} from {ext.bold(selected_flight[9])} to {ext.bold(selected_flight[10])} is as shown:\n")
        ext.view_table(view_seats_fields, view_seats)
        select_class = input("\nPlease select: ")
        
        if select_class == "1":
            selected_seat = "Economy"
            ticket_price = selected_flight[15]
            seat_number = assign_seat_economy(int(display_no_of_seat[0][1]))
            selected_flight[11] = str(int(selected_flight[11]) - 1)
            break
        elif select_class == "2":
            selected_seat = "Business"
            ticket_price = selected_flight[16]
            seat_number = assign_seat_business(int(display_no_of_seat[0][2]))
            selected_flight[12] = str(int(selected_flight[12]) - 1)
            break
        else:   
            clear()
            print("Invalid Response! Please choose between 1 and 2.")
            input("\nPress Enter to contiue ")
            clear()
    
    #Select Meal
    while True:
        clear()
        meals = show_meal_menu(selected_flight_key)

        try:
            select_meal = int(input("Choose meal: "))
            if select_meal in range(1, len(meals) + 1):
                break
            else:
                clear()
                print("Please Enter a valid option!")
                input("\nPress Enter to continue ")
                clear()
        except:
            clear()
            print("Please Enter a valid option!")
            input("\nPress Enter to continue ")
            clear()
    selected_meal = meals[select_meal-1][1]


    #Customer detials
    passenger_name = customer_details[1]
    booking_date = str(date.today())

    #Generate New Booking ID
    last_booking_ID = b_entries[-1][0]
    booking_ID = f"B{int(last_booking_ID[1:])+1}"

    #Schedule ID;Airline ID;Flight No;Status;Dep Date;Dep Time;Arr Date;Arr Time;Dep Airport;Arr Airport;Economy Seats;Business Seats;In Flight Menu;In Flight Services;Gate
    
    new_booking = [[booking_ID, user_name, selected_flight_key, booking_date, passenger_name, selected_seat, seat_number, selected_meal, ticket_price]]
    display_confirm_list = []
    display_confirm_fields = ["Itineraries", "Details"]
    for i in range(len(new_booking[0])):
        display_confirm_list.append([b_field_names[i], new_booking[0][i]])
    
    #Final Comfirmation and are you robot?
    new_booking = [[booking_ID, user_name, selected_flight_key, booking_date, passenger_name, selected_seat, seat_number, selected_meal, ticket_price, "Confirmed"]]
    while True:    
        clear()
        code = str(generate_random_code())
        print(f"For flight {ext.bold(selected_flight_key)} from {ext.bold(selected_flight[9])} to {ext.bold(selected_flight[10])}: \n")
        ext.view_table(display_confirm_fields, display_confirm_list)
        
        print( "\nAre you a robot?")
        print(f'\nInsert {code} to comfirm booking, Insert "cancel" to cancel booking')
        comfirmation = input("Your reply: ")
        
        
        if comfirmation == code:
            clear()
            fm.append_file('bookings', new_booking)
            fm.update_file('flights', selected_flight[1:])
            print(f"Booking Succesful! Your Booking ID is :{booking_ID}") 
            input("\nEnjoy Your Flight! Press Enter to continue ")
            clear()
            return
        
        elif comfirmation == "cancel":
            clear()
            print("Booking Cancelled... \ntoo bad :(")
            input("\nPress Enter to continue ")
            clear()
            return
        else:
            clear()
            print("You seems like a Robot :/\nPlease enter a valid response!!")
            input("\nPress Enter to continue ")
            clear()

def sort_duplicates_flights(all_available_flights):
    destination = []
    #remove duplication
    for flight in all_available_flights:
        if flight not in destination:
            destination.append(flight)
    return destination    

def sorted_flight(all_flights):
    #Put all flights data into one huge tuple
    all_available_flights = []
    for destination in all_flights:
       all_available_flights.append(destination[9])
    
    #remove duplication 
    choices = sort_duplicates_flights(all_available_flights)
    return choices

def view_profile(user_name):
    index, user = fm.query_key("customers", user_name)
    field_names = fm.get_field_names("customers")
    display_header = ["No.", "Field", "Value"]
    display_user = []
    for i in range(len(user)):
        display_user.append([str(i+1), field_names[i], user[i]])
    ext.view_table(display_header, display_user)

def update_profile(user_name):
    user_index, user = fm.query_key("customers", user_name)
    while True:
        try:
            view_profile(user_name)
            choice = int(input("\nPlease select detail to update: "))
            if choice in range(1, len(user)+1):
                break
            else:
                clear()
                print(f"Please enter a valid number between {1} and {len(user)}.")
                input("\nPress Enter to continue ")
                clear()
        except:
            clear()
            print(f"Please enter a valid number between {1} and {len(user)}.")
            input("\nPress Enter to continue ")
            clear()
    if choice == 1: # Username
        new_username = input(f"Your original username is {user_name}, please enter the new username: ")
        # Check if username exists
        index, check_user = fm.query_key("customers", new_username)
        if index == -1:
            confirm = input(f"The username is not taken, are you sure you want to change your username from {user_name} to {new_username}? (Yes/No) ")
            if confirm.lower() in ["yes", "y"]:
                user[0] = new_username
                fm.delete_entry('customers', user_name)
                fm.append_file('customers', [user])

                # Change all booking username from original to changed
                bookings = fm.query_field_strict("bookings", "User ID", user_name)
                for index in range(len(bookings)):
                    bookings[index][1] = new_username
                    fm.update_file('bookings', bookings[index])
                
                clear()
                print("Successfully updated username.")
                input("\nPress Enter to continue ")
                clear()
                return
        else:
            clear()
            print("This username is already taken, returning to profile menu.")
            input("\nPress Enter to continue ")
            clear()
            return
    if choice == 2: # Name
        new_name = input(f"Your name is {user[1]}, please enter the new name: ")
        user[1] = new_name
        fm.update_file('customers', user)
        clear()
        print("Successfully updated name.")
        input("\nPress Enter to continue ")
        clear()
        return
    if choice == 3: # Address
        new_address = input(f"Your original address is {user[2]}, please enter the new address: ")
        user[2] = new_address
        fm.update_file('customers', user)
        clear()
        print("Successfully updated address.")
        input("\nPress Enter to continue ")
        clear()
    if choice == 4: # Email
        new_email = input(f"Your original email is {user[3]}, please enter the new email: ")
        if validate_email(new_email):

            user[3] = new_email
            fm.update_file('customers', user)
            clear()
            print("Successfully updated email.")
            input("\nPress Enter to continue ")
            clear()
            return
        else:
            clear()
            print("Invalid email format, returning to profile menu...")
            input("\nPress Enter to continue ")
            clear()
            return
    if choice == 5: # passport
        new_password = input(f"Your original passport is {user[4]}, please enter the new passport: ")
        if validate_passport(new_password):

            user[4] = new_password
            fm.update_file('customers', user)
            clear()
            print("Successfully updated passport.")
            input("\nPress Enter to continue ")
            clear()
            return
        else:
            clear()
            print("Invalid password format, returning to profile menu...")
            input("\nPress Enter to continue ")
            clear()
            return
    if choice == 6: # Contact Number
        new_contact = input(f"Your original contact number is {user[5]}, please enter the new contact number: ")
        if validate_passport(new_contact):

            user[4] = new_contact
            fm.update_file('customers', user)
            clear()
            print("Successfully updated contact number.")
            input("\nPress Enter to continue ")
            clear()
            return
        else:
            clear()
            print("Invalid contact number format, returning to profile menu...")
            input("\nPress Enter to continue ")
            clear()
            return
    if choice == 7: # Gender
        new_gender = input(f"Your original gender is {user[6]}, please enter the new gender (Male/Female/Others): ")
        if new_gender in ["Male", "Female", "Others"]:

            user[6] = new_gender
            fm.update_file('customers', user)
            clear()
            print("Successfully updated gender.")
            input("\nPress Enter to continue ")
            clear()
            return
        else:
            clear()
            print("Invalid gender input, returning to profile menu...")
            input("\nPress Enter to continue ")
            clear()
            return
    if choice == 8: # Date of birth
        new_dob = input(f"Your original date of birth is {user[7]}, please enter the new date of birth in YYYY-MM-DD format: ")

        if new_dob in ["Male", "Female", "Others"]:

            user[7] = new_dob
            fm.update_file('customers', user)
            clear()
            print("Successfully updated date of birth.")
            input("\nPress Enter to continue ")
            clear()
            return
        else:
            clear()
            print("Invalid date of birth format, returning to profile menu...")
            input("\nPress Enter to continue ")
            clear()
            return
    if choice == 9: # Password
        new_password = input(f"Your original password is {user[8]}, please enter the password: ")
        confirm_password = input("Please enter your password again: ")
        if new_password == confirm_password:
            clear()
            print("Successfully updated password.")
            input("\nPress Enter to continue ")
            clear()
            return
        else:
            clear()
            print("Incorrect confirmation, returning to profile menu...")
            input("\nPress Enter to continue ")
            clear()
            return
    
def delete_account(user_name):
    clear()
    code = str(generate_random_code())
    confirmation = input(f"Are you sure you want to delete your account with username {ext.bold(user_name)}? This action is {ext.bold('NOT REVERSABLE')} (Yes/No): ")
    if confirmation.lower() not in ["yes", "y"]:
        clear()
        print("Canceled deleting account, returning to profile menu...")
        input("\nPress Enter to continue ")
        clear()
        return
    password = input(f"Please enter the password for the user {user_name}: ")
    index, entry = fm.query_key("customers", user_name)
    if index == -1:
        clear()
        print("Something wrong happened! Please log out and login again!")
        input("\nPress Enter to continue ")
        clear()
        return
    if entry[8] != password:
        clear()
        print("Password incorrect, returning to profile menu...")
        input("\nPress Enter to continue ")
        clear()
        return
    confirmation = input(f"{ext.bold('Last warning')}, are you sure you want to delete your account with username {ext.bold(user_name)}? Enter {ext.bold(code)} to comfirm delete account, No to return to previous menu.\nYour reply:")
    if confirmation not in code :
        clear()
        print("Canceled deleting account, returning to profile menu...")
        input("\nPress Enter to continue ")
        clear()
        return
    if fm.delete_entry("customers", user_name):
        print("Successfully deleted account. Thank you for using this program, exiting program.")
        exit()
    else:
        clear()
        print("Something wrong happened! Please log out and login again!")
        input("\nPress Enter to continue ")
        clear()
        return

def profile(user_name):
    while True:
        ext.show_menu("Profile Menu", ["View Profile", "Update Profile", "Delete Account", "Back"])
        choice = input("\nPlease select: ")
        if choice in ["4", "-1"]:
            clear()
            return
        elif choice == "1":
            view_profile(user_name)
        elif choice == "2":
            update_profile(user_name)
        elif choice == "3":
            delete_account(user_name)
        elif choice in ["4", "-1"]:
            clear()
            return
        else:
            clear()
            print("Invalid choice. Please select a valid option.")
            input("\nPress Enter to continue ")
            clear()
            
def view_booking(user_name):
    print("Shown are all the bookings you made: \n")
    bookings = fm.query_field_strict("bookings", "User ID", user_name)
    for index in range(len(bookings)):
        schedule_id = bookings[index][2]
        search_index, schedule = fm.query_key("flights", schedule_id)
        bookings[index] = bookings[index] + [schedule[8], schedule[9]]
    booking_fields = fm.get_field_names("bookings") + ["Dep Airport", "Arr Airport"]
    ext.view_table(booking_fields, bookings)

def update_bookings(user_name):
    bookings = fm.query_field_strict("bookings", "User ID", user_name)
    if len(bookings) == 0 :
        clear()
        print("No available bookings, returning to manage bookings menu...")
        input("\nPress Enter to continue ")
        clear()
        return
    booking_fields = fm.get_field_names("bookings")
    for i in range(len(bookings)):
        bookings[i] = [str(i+1)] + bookings[i]
    booking_fields = ["No."] + booking_fields
    while True:
        try:
            clear()
            print("Shown are all the bookings you made: \n")
            ext.view_table(booking_fields, bookings)
            choice = int(input("\nPlease select: "))
            if choice in range(1, len(bookings)+1):
                break
            else:
                clear()
                print(f"Please enter a valid input between 1 to {len(bookings)}")
                input("\nPress Enter to continue ")
                clear()
        except:
            clear()
            print(f"Please enter a valid input between 1 to {len(bookings)}")
            input("\nPress Enter to continue ")
            clear()
    
    booking = bookings[choice-1][1:]
    display_booking_header = ["No.", "Field", "Value"]
    display_booking = [["1", "Seat Type", booking[5]], ["2", "Meal", booking[7]]]
    

    while True:
        try:
            clear()
            print("The fields to be updated to ")
            ext.view_table(display_booking_header, display_booking)
            choice = int(input("\nPlease select: "))
            if choice in [1,2]:
                break
            else:
                clear()
                print(f"Please enter a valid input between 1 to 2.")
                input("\nPress Enter to continue ")
                clear()
        except:
            clear()
            print(f"Please enter a valid input between 1 to 2.")
            input("\nPress Enter to continue ")
            clear()

    if choice == 1:
        if booking[5] == "Economy":
            change = input("The current Seat Type is Economy.\nDo you want to change it into Business? (Yes/No): ")
            if change.lower() in ["yes", "y"]:
                index, flight = fm.query_key('flights', booking[2])
                flight[10] = str(int(flight[10]) + 1)
                flight[11] = str(int(flight[11]) - 1)
                booking[5] = "Business"
                fm.update_file('bookings', booking)
                fm.update_file('flights', flight)
                clear()
                print("Successfully changed from Economy to Business.")
                input("\nPress Enter to continue ")
                clear()
                return
            else:
                clear()
                print("Cancelled update bookings.")
                input("\nPress Enter to continue ")
                clear()
                return
        else:
            change = input("The current Seat Type is Business.\nDo you want to change it into Economy? (Yes/No): ")
            if change.lower() in ["yes", "y"]:
                index, flight = fm.query_key('flights', booking[2])
                flight[11] = str(int(flight[11]) + 1)
                flight[10] = str(int(flight[10]) - 1)
                booking[5] = "Economy"
                fm.update_file('bookings', booking)
                fm.update_file('flights', flight)
                clear()
                print("Successfully changed from Business to Economy.")
                input("\nPress Enter to continue ")
                clear()
                return
            else:
                clear()
                print("Cancelled update bookings.")
                input("\nPress Enter to continue ")
                clear()
                return

    elif choice == 2:
        while True:
            clear()
            meals = show_meal_menu(booking[2])

            try:
                select_meal = int(input("Choose meal: "))
                if select_meal in range(1, len(meals) + 1):
                    break
                else:
                    clear()
                    print("Please Enter a valid option!")
                    input("\nPress Enter to continue ")
                    clear()
            except:
                clear()
                print("Please Enter a valid option!")
                input("\nPress Enter to continue ")
                clear()
        selected_meal = meals[select_meal-1][1]
        booking[7] = selected_meal
        fm.update_file("bookings", booking)
        clear()
        print("Successfully updated bookings.")
        input("\nPress Enter to continue ")
        clear()
        return

def cancel_booking(user_name):
    bookings = fm.query_field_strict("bookings", "User ID", user_name)
    if len(bookings) == 0 :
        clear()
        print("No available bookings, returning to manage bookings menu...")
        input("\nPress Enter to continue ")
        clear()
        return
    booking_fields = fm.get_field_names("bookings")
    for i in range(len(bookings)):
        bookings[i] = [str(i+1)] + bookings[i]
    booking_fields = ["No."] + booking_fields
    while True:
        try:
            clear()
            print("Shown are all the bookings you made: \n")
            ext.view_table(booking_fields, bookings)
            choice = int(input("\nPlease select: "))
            if choice in range(1, len(bookings)+1):
                break
            else:
                clear()
                print(f"Please enter a valid input between 1 to {len(bookings)}")
                input("\nPress Enter to continue ")
                clear()
        except:
            clear()
            print(f"Please enter a valid input between 1 to {len(bookings)}")
            input("\nPress Enter to continue ")
            clear()
    booking = bookings[choice-1][1:]

    choice = input("Are you sure you want to delete the chosen booking? (Yes/No) ")
    if choice.lower() in ["y", "yes"]:
        fm.delete_entry("bookings", booking[0])
        clear()
        print("Selected booking deleted successfully.")
        input("\nPress Enter to continue ")
        clear()
        return
    else:
        clear()
        print("Delete booking cancelled.")
        input("\nPress Enter to continue ")
        clear()
        return
    
def check_in(user_name):
    # Get bookings by user
    user_bookings = fm.query_field_strict("bookings", "User ID", user_name)

    # Get booking field names
    booking_fields = fm.get_field_names('bookings')
    
    if len(user_bookings) == 0:
        clear()
        print("No bookings to be checked in, returning manage bookings menu...")
        input("\nPress Enter to continue ")
        clear()
        return

    # Filter out flights that already happened
    new_bookings = []
    display_booking = []
    for i in range(len(user_bookings)):
        index, flight_entry = fm.query_key("flights", user_bookings[i][2])
        if index != 1:
            if compare_datetime(f"{flight_entry[4]} {flight_entry[5]}"):
                new_bookings.append(user_bookings[i])
                display_booking.append([str(len(new_bookings))] + user_bookings[i])
    display_booking_fields = ["Index"] + booking_fields

    if len(new_bookings) == 0:
        clear()
        print("No bookings to be checked in, all the flights you booked has already flew, returning manage bookings menu...")
        input("\nPress Enter to continue ")
        clear()
        return


    # Display booking
    while True:
        try:
            clear()
            ext.view_table(display_booking_fields, display_booking)
            choice = int(input("\nPlease select booking to check in: "))
            if choice == -1:
                clear()
                print("Cancelling check in, returning to manage booking menu...")
                input("\nPress Enter to continue ")
                clear()
                return
            if choice in range(1, len(new_bookings)+1):
                break
            else:
                clear()
                print("Invalid input, please enter a valid input!")
                input("\nPress Enter to continue ")
                clear()
        except:
            clear()
            print("Invalid input, please enter a valid input!")
            input("\nPress Enter to continue ")
            clear()

    clear()
    print(f"Here is your {ext.bold('Check In')} ticket: \n")
    ext.report("Check In", booking_fields, new_bookings[choice-1])
    input("\nPress Enter to continue ")
    clear()
    
def manage_booking(user_name):
    clear()
    while True:
        ext.show_menu("Manage Booking", ["View Bookings", "Update Booking", "Cancel Booking", "Check In", "Back"])
        choice = input("\nPlease select: ")

        if choice in ["-1", "5"]:
            clear()
            return
        elif choice == "1":
            clear()
            view_booking(user_name)
            input("\nPress Enter to continue ")
            clear()
        elif choice == "2":
            clear()
            update_bookings(user_name)
        elif choice == "3":
            clear()
            cancel_booking(user_name)
        elif choice == "4":
            check_in(user_name)
        else: 
            clear()
            print("Invalid choice. Please select a valid option.")
            input("\nPress Enter to continue ")
            clear()

def menu_for_booking(user_name):
    while True:
        clear()
        ext.show_menu("What can I help?", ["Book a new Flight", "Manage Bookings", "Profile", "Back"])
        choice = input("\nPlease select: ")

        if choice in ["4", "-1"]:
            return

        if choice == "1": 
            book_flight(user_name)

        elif choice == "2":
            manage_booking(user_name)
        elif choice == "3":
            profile(user_name)
        else: 
            clear()
            print("Invalid choice. Please select a valid option.")
            input("\nPress Enter to continue ")
            clear()

def main_menu():
    clear()
    clear()
    while True:
        ext.show_menu("Main Menu", ["Login", "Sign-up", "View all Flights", "Exit"])

        choice = input("Please select function: ")

        if choice == "1":
            login()
            clear()
        elif choice == "2":
            signup()
            print("Registration successful.")
            input("Press Enter to continue ")
            clear()
        elif choice == "3":
            view_flight()
            input("Press Enter to continue ")
            clear()
        elif choice in ["4", "-1"]:
            print("Goodbye!")
            break
        else:
            clear()
            print("Invalid choice. Please select a valid option.")
            input("Press Enter to continue ")
            clear()

def login():
    
    while True: 
        clear()
        print(ext.bold("Login") + "\n")
        user_name = input("User ID: ")
        
        if user_name == "-1":
            clear()
            print("Returning to main menu...")
            input("\nPress Enter to continue ")
            clear()
            return

        file_index,customer_details = fm.query_key("customers", user_name)
         #customer_details: User ID;Name;Address;Email;Passport Number;Contact Number;Gender;Date Of Birth;Password
        
        if file_index == -1:
            clear()
            print("User not found!")
            input("\nPress Enter to continue ")
            clear()

        
        else:
            password = input("Password: ")

            if customer_details[8] == password:
                clear()
                print(f"Login successful! Welcome {user_name}!")    
                input("\nPress Enter to continue ")
                menu_for_booking(user_name)
                return
            else:  
                clear()
                print("Wrong password, please try again.")
                input("\nPress Enter to continue ")
                clear()

#Details: UserID ; Name ; Address ; Email ; PassportNumber ; ContactNumber ; Gender ; DateOfBirth ; Password
def signup():
    clear()
    output_string = f"{ext.bold('Sign-up')}\n"
    print(output_string)
    while True:
        clear()
        print(output_string)
        userID = input("Please create an user ID: ")  
        query_result = fm.query_key('customers', userID)
        if query_result[0] == -1:
            output_string += f"\nPlease create an user ID: {userID}"
            break
        elif not userID:
            clear()
            print("Don't leave it blank like your school test paper!!! You should be thankful that there's a second chance here!!!")
            input("\nPress Enter to continue ")
            clear()
        else:
            clear()
            print("This user ID is taken, please enter a valid user ID!")
            input("\nPress Enter to continue ")
            clear()

    while True:
        clear()
        print(output_string)
        name = input("Please enter your name: ")
        if name:
            output_string += f"\nPlease enter your name: {name}"
            break
        else:
            clear()
            print("Don't leave it blank like your school test paper!!! You should be thankful that there's a second chance here!!!")
            input("\nPress Enter to continue ")
            clear()
    #Insert address 
    while True:
        clear()
        print(output_string)
        address = input("Please enter your home address: ")
        if address:
            output_string += f"\nPlease enter your home address: {address}"
            break
        else:
            clear()
            print("Don't leave it blank like your exam paper!!! You should be thankful that there's a second chance here!!!")
            input("\nPress Enter to continue ")
            clear()

    #insert and validate email address
    while True:
        clear()
        print(output_string)
        email = input("Please enter your email address: ")
        if validate_email(email):
            output_string += f"\nPlease enter your email address: {email}"
            break
        else:
            clear()
            print("Invalid email address! Please enter a valid email.")
            input("\nPress Enter to continue ")
            clear()

    #insert and validate passport number
    while True:
        clear()
        print(output_string)
        passport = input("Please enter your passport number: ")
        if validate_passport(passport):
            output_string += f"\nPlease enter your passport number: {passport}"
            break
        else:
            clear()
            print("Invalid ID format! Please enter a valid passport number.")
            input("\nPress Enter to continue ")
            clear()
    #insert and validate phone number
    while True:
        clear()
        print(output_string)
        contact_number = input("Please enter your contact number: ")
        if validate_contact_number(contact_number):
            output_string += f"\nPlease enter your contact number: {contact_number}"
            break
        else:
            clear()
            print("Invalid phone number format!")
            input("\nPress Enter to continue ")
            clear()

    # Gender selection
    while True:
        clear()
        print(output_string)
        gender = input("Please enter your gender (Male/Female/Others): ")
        if gender in ["Male", "Female", "Others"]:
            output_string += f"\nPlease enter your gender (Male/Female/Others): {gender}"
            break
        else:
            clear()
            print("Invalid choice!!! Please select a valid option.")
            input("\nPress Enter to continue ")
            clear()

    #Insert and validate birthday
    while True:
        clear()
        print(output_string)
        date_of_birth = input("Please insert your date of birth in YYYY-MM-DD format: ")
        if validate_date(date_of_birth):
            output_string += f"\nPlease insert your date of birth in YYYY-MM-DD format: {date_of_birth}"
            break
        else:
            clear()
            print("Invalid date format!")
            input("\nPress Enter to continue ")
            clear()

    #Creating password
    clear()
    print(output_string)
    password = input("Create your password: ")


    new_user = [[userID, name, address, email,passport,contact_number, gender , date_of_birth, password]]
    fm.append_file('customers', new_user)

main_menu()