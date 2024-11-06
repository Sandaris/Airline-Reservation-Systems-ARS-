import modules.file_manage as fm
import modules.ext_funcs as ext
import re
import datetime
import os

def clear():
    os.system('cls')
    print("\n")

def flight_verify(field, value):
    value = value.strip()
    if field == "Airline ID":
        if value not in ["MAS1709", "ZW1865", "ME2098", "APU8760"]:
            return False, "Invalid Airline ID, please input one of: 'MAS1709', 'ZW1865', 'ME2098', 'APU8760'."
        return True, "Valid Airline ID."
    elif field == "Flight No":
        if len(value) != 5:
            return False, "Invalid Flight No, please enter the flight no in XXNNN format (XX must be one of 'MH', 'AK', 'ME', 'AP')."
        pattern = r"(MH|AK|ME|AP)\d\d\d"
        match = re.match(pattern, value)
        if not match:
            return False, "Invalid Flight No, please enter the flight no in XXNNN format (XX must be one of 'MH', 'AK', 'ME', 'AP')."
        return True, "Valid Flight No."
    elif field == "Status":
        if value not in ["On-time", "Delayed", "Cancelled"]:
            return False, "Invalid Status, please enter either 'On-time', 'Delayed', or 'Cancelled'."
        return True, "Valid Status."
    elif field in ["Dep Date", "Arr Date"]:
        try:
            datetime.date.fromisoformat(value)
        except:
            return False, f"Invalid {field}, please enter the date in YYYY-MM-DD format (eg. 2023-09-04)."
        return True, f"Valid {field}."
    elif field in ["Dep Time", "Arr Time"]:
        time_format = "%H:%M:%S"
        try:
            datetime.datetime.strptime(value, time_format)
        except:
            return False, f"Invalid {field}, please enter the time HH:MM:SS format (eg.13:01:02)."
        return True, f"Valid {field}."
    elif field in ["Dep Airport", "Arr Airport"]:
        pattern = r"[A-Z][A-Z][A-Z]"
        match = re.match(pattern, value)
        if not match:
            return False, f"Invalid {field}, please enter the airport code in XXX (eg. KUL) format."
        return True, f"Valid {field}."
    elif field in ["Economy Seats", "Business Seats"]:
        try:
            int(value)
        except:
            return False, f"Invalid {field}, please enter an integer."
        return True, f"Valid {field}."
    elif field in ["In Flight Menu", "In Flight Services"]:
        if ";" in value:
            return False, f"Invalid {field}, value cannot contain ';'."
        return True, f"Valid {field}."
    elif field == "Gate":
        pattern = r"[A-Z]\d\d"
        match = re.match(pattern, value)
        if not match:
            return False, f"Invalid {field}, please enter the gate number in XNN format (eg. G10)."
        return True, f"Valid {field}."
    elif field in ["Economy Price", "Business Price"]:
        try:
            int(value)
        except:
            return False, f"Invalid {field}, please enter an integer."
        return True, f"Valid {field}."
        
    else:
        raise ValueError("Something's wrong, please check your code to make sure that the field passed in exists in flights.txt.")

def view_flights():
    field_names, entries = fm.read_file('flights')
    display_fields1, display_entries1 = ext.remove_fields(field_names, entries, ["Economy Seats", "Business Seats", "In Flight Menu", "In Flight Services", "Economy Price", "Business Price"])
    display_fields2, display_entries2 = ext.remove_fields(field_names, entries, ["Airline ID", "Flight No", "Status", "Dep Date", "Dep Time", "Arr Date", "Arr Time", "Dep Airport", "Arr Airport"])
    ext.view_table(display_fields1, display_entries1)
    input("\nPress Enter to continue ")
    print()
    ext.view_table(display_fields2, display_entries2)
    print()

def login_menu():
    print("Administration Login Portal. \nPlease Login. (Enter -1 at any point to quit)")
    user_name = input("Enter your user name: ")
    if user_name == "-1":
        return "-1"
    password = input("Enter your password: ")
    if password == "-1":
        return "-1"
    values = fm.query_key("admins", user_name)
    if values[0] != -1:
        if values[1][-1] == password:
            clear()
            print(f"Login successful. Welcome, {user_name}!")
            input("\nPress Enter to continue ")
            clear()
            return user_name
        else:
            clear()
            print("Wrong password, please try again.")
            input("\nPress Enter to continue ")
            clear()
            return ""
    else:
        clear()
        print("Couldn't find user, please try again.")
        input("\nPress Enter to continue ")
        clear()
        return ""

def update_flight():
    field_names, entries = fm.read_file('flights')
    view_flights()
    key = input("\nPlease enter the Schedule ID for the flight to update: ")
    if key == "-1":
        clear()
        print("Update flight cancelled, returning to flights page...\n")
        input("\nPress Enter to continue ")
        clear()
        return
    index, entry = fm.query_key('flights', key)

    if index == -1:
        clear()
        print("Couldn't find schedule, returning to flights page...")
        input("\nPress Enter to continue ")
        clear()
        return

    clear()
    
    # Get the field to be changed
    while True:
        print(f"\nThe details for schedule {key} is as follows: ")
        print("Enter -1 to cancel\n")
        option_header = ["No.", "Field", "Value"]
        options = []
        for i in range(1, len(field_names)):
            options.append([str(i), field_names[i], entry[i]])
        ext.view_table(option_header, options)
        try:
            field = int(input("\nPlease enter the field to be changed: "))
            if field == -1:
                clear()
                print("Update flight cancelled, returning to flights page...\n")
                input("\nPress Enter to continue ")
                clear()
                return
            if field in range(1, len(field_names)):
                break
            else:
                clear()
                print("Invalid field, please enter again!")
                input("\nPress Enter to continue ")
                clear()
        except:
            clear()
            print("Invalid field, please enter again!")
            input("\nPress Enter to continue ")
            clear()
            

    print(f"The original data for {field_names[field]} is {entry[field]}.")
    while True:
        new_data = input("Please enter the new data to be updated: ")
        if new_data == "-1":
            clear()
            print("Update flight cancelled, returning to flights page...\n")
            input("\nPress Enter to continue ")
            clear()
            return
        validated, message = flight_verify(field_names[field], new_data)
        if not validated:
            print("\n" + message)
        else:
            break
    entry[field] = new_data
    fm.update_file('flights', entry)

def add_flight():
    field_names, entries = fm.read_file('flights')
    
    # Generate key for the new schedule
    last_key = entries[-1][0]
    new_key = f"S{int(last_key[1:])+1}"

    new_entry = [new_key]

    airline_dict = {"MAS1709": "MH", "ZW1865": "AK", "ME2098": "ME", "APU8760": "AP"}
    format_guide = [
        "",
        "Format: 'MAS1709' or 'ZW1865' or 'ME2098' or 'APU8760'.",
        "",
        "Format: 'On-time' or 'Delayed' or 'Cancelled'.",
        "Format: YYYY-MM-DD (eg. 2023-09-04).",
        "Format: HH:MM:SS (eg. 13:02:01).",
        "Format: YYYY-MM-DD (eg. 2023-09-04).",
        "Format: HH:MM:SS (eg. 13:02:01).",
        "Format: XXX (eg. KUL).",
        "Format: XXX (eg. KUL).",
        "Format: Number (eg. 120).",
        "Format: Number (eg. 40).",
        "Format: Meals separated using commas (eg. Chicken Rice,Beef Rice,Noodles).",
        "Format: Services separated using commas (eg. WiFi,Entertainment,Blanket).",
        "Format: Number (eg. 250)",
        "Format: Number (eg. 400)"
    ]

    input_message = ""
    clear()
    
    for i in range(1, len(field_names)):
        while True:
            print("Enter -1 at anytime to cancel.\n")
            print(input_message)
            if i == 2:
                print(f"Format: {airline_dict[new_entry[1]]}NNN (eg. {airline_dict[new_entry[1]]}025).")
            else:
                print(format_guide[i])
            new_field = input(f"Enter the value for {field_names[i]}: ")
            print()
            if new_field == "-1":
                clear()
                print("Add flight cancelled, returning to flights page...\n")
                input("Press Enter to continue ")
                clear()
                return
            if i == 2:
                
                if len(new_field) != 5:
                    clear()
                    print(f"Invalid Flight No, please enter the flight no in {ext.bold(airline_dict[new_entry[1]])}NNN format.")
                    input("\nPress Enter to continue ")
                    clear()
                    continue
                else:
                    if new_field[:2] == airline_dict[new_entry[1]]:
                        input_message += f"{field_names[i]}{' '*(18-len(field_names[i]))}: {new_field}\n"
                        new_entry.append(new_field)
                        clear()
                        break
                    else:
                        clear()
                        print(f"Invalid Flight No, first two character must be {ext.bold(airline_dict[new_entry[1]])}.")
                        input("\nPress Enter to continue ")
                        clear()
                        continue
            validation, message = flight_verify(field_names[i], new_field)
            if validation:
                input_message += f"{field_names[i]}{' '*(18-len(field_names[i]))}: {new_field}\n"
                new_entry.append(new_field)
                clear()
                break
            else:
                clear()
                print(message, end="\n")
                input("\nPress Enter to continue ")
                clear()

    fm.append_file("flights", [new_entry])
    this_airline = fm.query_key('airlines', new_entry[1])
    this_airline[1][2] = str(int(this_airline[1][2]) + 1)
    fm.update_file('airlines', this_airline[1])
    print(input_message)
    input("Successfully added flight.\n\nPress Enter to continue ")
    clear()

def delete_flight():
    view_flights()

    key = input("\nPlease enter the Schedule ID for the flight to delete: ")
    if key == "-1":
        clear()
        print("Delete flight cancelled, returning to flights page...")
        input("\nPress Enter to continue ")
        clear()
        return
    
    deleted = fm.delete_entry('flights', key)
    if deleted:
        clear()
        print("Deleted successfully.")
        return
    else:
        clear()
        print("Couldn't find schedule, returning to flights page...")
        input("\nPress Enter to continue ")
        clear()
        return
    
def show_services(key):
    print(f"The services provided for the flight {key} is as shown:\n")
    index, entry = fm.query_key('flights', key)
    services = entry[13].split(",")
    for i in range(len(services)):
        services[i] = [str(i+1)] + [services[i]]
    services_header = ["No.", "Service"]
    
    ext.view_table(services_header, services)


def show_menu(key):
    print(f"The meals provided for the flight {ext.bold(key)} is as shown:\n")
    index, entry = fm.query_key('flights', key)
    meals = entry[12].split(",")
    for i in range(len(meals)):
        meals[i] = [str(i+1)] + [meals[i]]
    menu_header = ["No.", "Meal"]
    
    ext.view_table(menu_header, meals)

def services():
    clear()
    view_flights()
    key = input("\nPlease enter the schedule of the flight to modify the in flight services: ")
    if key == "-1":
        clear()
        print("Returning to In Flight Services and Meals page...")
        input("\nPress Enter to continue ")
        clear()
        return

    index, entry = fm.query_key('flights', key)
    
    if index == -1:
        clear()
        print("Couldn't find schedule, returning to services and meals page...")
        input("\nPress Enter to continue ")
        clear()
    else:
        while True:
            clear()
            service_list = entry[13].split(",")
            show_services(key)
            print()
            ext.show_menu("Actions", ["Add New Service", "Update Service", "Delete Service", "Back"])
            # print("\n1. Add New Service\n2. Update Service\n3. Delete Service\n4. Back\n")
            action = input("Please select: ")
            if action == "1":
                clear()
                show_services(key)
                service = input("\nEnter the new service to be added: ")
                if service == "-1":
                    clear()
                    print("Cancelled adding service. Returning to services menu...")
                    input("\nPress Enter to continue ")
                    clear()
                else:
                    pattern = r"\w+"
                    match = re.match(pattern, service)
                    if match:
                        entry[13] += f",{service}"
                        fm.update_file('flights', entry)
                        clear()
                        print("Successfully added service.")
                        input("\nPress Enter to continue ")
                        clear()
                    else:
                        clear()
                        print("Incorrect service input, please enter only words. Returning to services menu...")
                        input("\nPress Enter to continue ")
                        clear()
            elif action == "2":
                if len(service_list) == 0:
                    clear()
                    print("There isn't any service in this flight to be updated. Returning to services menu...")
                    input("\nPress Enter to continue ")
                    clear()
                else:
                    clear()
                    show_services(key)
                    quit_update = False
                    while True:
                        try:
                            service_index = int(input("Select the service to be updated: "))
                            if service_index == -1:
                                quit_update = True
                                break
                            if service_index in range(1, len(service_list)+1):
                                break
                            else:
                                print(f"Please enter a valid input from 1 to {len(service_list)}.")
                        except:
                            print(f"Please enter a valid input from 1 to {len(service_list)}.")
                    if not quit_update:
                        print(f"\nYou selected the service '{service_list[service_index-1]}' to update.")
                        new_service = input("\nEnter the updated service: ")
                        if new_service == "-1":
                            clear()
                            print("Cancelled update service. Returning to services menu...")
                            input("\nPress Enter to continue ")
                            clear()
                        else:
                            pattern = r"\w+"
                            match = re.match(pattern, new_service)
                            if match:
                                service_list[service_index-1] = new_service
                                entry[13] = ",".join(service_list)
                                fm.update_file('flights', entry)
                                clear()
                                print("Successfully updated service.")
                                input("\nPress Enter to continue ")
                                clear()
                            else:
                                clear()
                                print("Incorrect service input, please enter only words. Returning to services menu...")
                                input("\nPress Enter to continue ")
                                clear()
                    else:
                        clear()
                        print("Cancelled update service. Returning to services menu...")
                        input("\nPress Enter to continue ")
                        clear()
            elif action == "3":
                if len(service_list) == 0:
                    clear()
                    print("There isn't any service in this flight to be deleted.")
                    input("\nPress Enter to continue ")
                    clear()
                else:
                    clear()
                    show_services(key)
                    quit_delete = False
                    while True:
                        try:
                            service_index = int(input("Select the service to be deleted: "))
                            if service_index == -1:
                                quit_delete = True
                                break
                            if service_index in range(1, len(service_list)+1):
                                break
                            else:
                                print(f"Please enter a valid input from 1 to {len(service_list)}.")
                        except:
                            print(f"Please enter a valid input from 1 to {len(service_list)}.")
                    if not quit_delete:
                        print(f"You selected the service '{service_list[service_index-1]}' to delete.")
                        confirmation = input(f"Do you want to delete {service_list[service_index-1]} (Y/N) : ")
                        if confirmation.lower() in ["y", "yes"]:
                            service_list.pop(service_index-1)
                            entry[13] = ",".join(service_list)
                            fm.update_file('flights', entry)
                            clear()
                            print("Successfully deleted service.")
                            input("\nPress Enter to continue ")
                            clear()
                        else:
                            clear()
                            print("Delete service cancelled.")
                            input("\nPress Enter to continue ")
                            clear()
                    else:
                        clear()
                        print("Cancelled delete service. Returning to services menu...")
                        input("\nPress Enter to continue ")
                        clear()
            elif action in ["4", "-1"]:
                clear()
                break
            else:
                clear()
                print("Please enter a valid input!")
                input("\nPress Enter to continue ")
                clear()

def meals():
    clear()
    view_flights()
    key = input("\nPlease enter the schedule of the flight to modify the in flight menu: ")

    index, entry = fm.query_key('flights', key)
    
    if index == -1:
        clear()
        print("Couldn't find schedule, returning to services and meals page...")
        input("\nPress Enter to continue ")
        clear()
    else:
        while True:
            clear()
            meal_list = entry[12].split(",")
            show_menu(key)
            print("\n1. Add New Meal\n2. Update Meal\n3. Delete Meal\n4. Back\n")
            action = input("Please select: ")
            if action == "1":
                clear()
                show_menu(key)
                meal = input("Enter the new meal to be added: ")
                if meal == "-1":
                    clear()
                    print("Cancelled adding meal. Returning to meals menu...")
                    input("\nPress Enter to continue ")
                    clear()
                else:
                    pattern = r"\w+"
                    match = re.match(pattern, meal)
                    if match:
                        entry[12] += f",{meal}"
                        fm.update_file('flights', entry)
                        clear()
                        print("Successfully added meal.")
                        input("\nPress Enter to continue ")
                        clear()
                    else:
                        clear()
                        print("Incorrect meal input, please enter only words. Returning to meals menu...")
                        input("\nPress Enter to continue ")
                        clear()
            elif action == "2":
                if len(meal_list) == 0:
                    clear()
                    print("There isn't any meal in this flight to be updated. Returning to meal menu...")
                    input("\nPress Enter to continue ")
                    clear()
                else:
                    clear()
                    show_menu(key)
                    quit_update = False
                    while True:
                        try:
                            meal_index = int(input("Select the meal to be updated: "))
                            if meal_index == -1:
                                quit_update = True
                                break
                            if meal_index in range(1, len(meal_list)+1):
                                break
                            else:
                                print(f"Please enter a valid input from 1 to {len(meal_list)}.")
                        except:
                            print(f"Please enter a valid input from 1 to {len(meal_list)}.")
                    if not quit_update:
                        print(f"\nYou selected the meal '{meal_list[meal_index-1]}' to update.")
                        new_meal = input("\nEnter the updated meal: ")
                        if new_meal == "-1":
                            clear()
                            print("Cancelled update meal. Returning to meals menu...")
                            input("\nPress Enter to continue ")
                            clear()
                        else:
                            pattern = r"\w+"
                            match = re.match(pattern, new_meal)
                            if match:
                                meal_list[meal_index-1] = new_meal
                                entry[12] = ",".join(meal_list)
                                fm.update_file('flights', entry)
                                clear()
                                print("Successfully updated meal.")
                                input("\nPress Enter to continue ")
                                clear()
                            else:
                                clear()
                                print("Incorrect meal input, please enter only words. Returning to meals menu...")
                                input("\nPress Enter to continue ")
                                clear()
                    else:
                        clear()
                        print("Cancelled update meal. Returning to meals menu...")
                        input("\nPress Enter to continue ")
                        clear()
            elif action == "3":
                if len(meal_list) == 0:
                    clear()
                    print("There isn't any meal in this flight to be deleted.")
                    input("\nPress Enter to continue ")
                    clear()
                else:
                    clear()
                    show_menu(key)
                    quit_delete = False
                    while True:
                        try:
                            meal_index = int(input("Select the meal to be deleted: "))
                            if meal_index == -1:
                                quit_delete = True
                                break
                            if meal_index in range(1, len(meal_list)+1):
                                break
                            else:
                                print(f"Please enter a valid input from 1 to {len(meal_list)}.")
                        except:
                            print(f"Please enter a valid input from 1 to {len(meal_list)}.")
                    if not quit_delete:
                        print(f"You selected the meal '{meal_list[meal_index-1]}' to delete.")
                        confirmation = input(f"Do you want to delete {meal_list[meal_index-1]} (Y/N) : ")
                        if confirmation.lower() in ["y", "yes"]:
                            meal_list.pop(meal_index-1)
                            entry[12] = ",".join(meal_list)
                            fm.update_file('flights', entry)
                            clear()
                            print("Successfully deleted meal.")
                            input("\nPress Enter to continue ")
                            clear()
                        else:
                            clear()
                            print("Delete meal cancelled.")
                            input("\nPress Enter to continue ")
                            clear()
                    else:
                        clear()
                        print("Cancelled delete meal. Returning to meals menu...")
                        input("\nPress Enter to continue ")
                        clear()
            elif action in ["4", "-1"]:
                clear()
                break
            else:
                clear()
                print("Please enter a valid input!")
                input("\nPress Enter to continue ")
                clear()

def in_flight_service_meals_menu():
    while True:
        ext.show_menu("In Flight Services and Meals", ["Services", "Meals", "Back"])
        choice = input("Please select: ")
        if choice == "1":
            services()
        elif choice == "2":
            meals()
        if choice in ["3", "-1"]:
            clear()
            return

def flights_menu():
    while True:
        ext.show_menu("Flights", ["View Flights", "Add new Flight", "Update Flight", "Delete Flight", "Cancel Flight", "In Flight Services and Meals", "Back"])
        choice = input("Please select: ")
        if choice == "1":
            clear()
            view_flights()
            input("Press Enter to continue ")
            clear()
        elif choice == "2":
            clear()
            add_flight()
        elif choice == "3":
            clear()
            update_flight()
        elif choice == "4":
            clear()
            delete_flight()
        elif choice == "5":
            cancel_flight()
        elif choice == "6":
            clear()
            in_flight_service_meals_menu()
        elif choice in ["6", "-1"]:
            clear()
            return
        else:
            clear()
            print("Invalid option, please enter a valid option!")
            input("\nPress Enter to continue ")
            clear()
        
def airlines_menu():
    while True:
        ext.show_menu("Airlines", ["View Airlines", "View Most Flights", "Generate Airline Report", "Back"])
        choice = input("Please select: ")
        field_names, entries = fm.read_file('airlines')
        if choice == "1":
            clear()
            ext.view_table(field_names, entries)
            input("\nPress Enter to continue ")
            clear()
        elif choice == "2":
            field_names, entries = fm.read_file('airlines')
            sorted_entries = ext.sort_entries(entries, 2, True)
            clear()
            print("The sorted airlines according to the most flights: ")
            ext.view_table(field_names, sorted_entries)
            input("\nPress Enter to continue ")
            clear()
        elif choice == "3":
            generate_airline_report()
        elif choice in ["4", "-1"]:
            clear()
            return
        else:
            clear()
            print("Invalid option, please enter a valid option!")
            input("\nPress Enter to continue ")
            clear()

def bookings_menu():
    while True:
        ext.show_menu("Bookings", ["View Bookings", "Generate Booking Ticket", "Generate Bill", "Search Booking", "View Cancelled Boookings", "Back"])
        choice = input("Please select: ")
        if choice == "1":
            view_bookings()
        elif choice == "2":
            booking_ticket()
        elif choice == "3":
            generate_bill()
        elif choice == "4":
            search_booking()
        elif choice == "5":
            view_cancelled_bookings()
        elif choice in ["6", "-1"]:
            clear()
            return
        else:
            clear()
            print("Invalid option, please enter a valid option!")
            input("\nPress Enter to continue ")
            clear()


def main():
    clear()
    clear()
    user = login_menu()
    while True:
        if user == "-1":
            print("Exiting program.")
            break
        elif user == "":
            user = login_menu()
        else:
            ext.show_menu("Admin Portal", ["Flights", "Airlines", "Bookings", "Logout", "Exit Program"])
            choice = input("Please select: ")

            if choice == "1":
                clear()
                flights_menu()
            elif choice == "2":
                clear()
                airlines_menu()
            elif choice == "3":
                clear()
                bookings_menu()
            elif choice == "4":
                clear()
                print("Logging out...\n")
                user = ""
            elif choice in ["5", "-1"]:
                user = "-1"
            else:
                clear()
                print("Invalid option, please enter a valid option!")
                input("\nPress Enter to continue ")
                clear()


def view_bookings():

    booking_fields, booking_entries = fm.read_file('bookings')
    clear()
    ext.view_table(booking_fields,booking_entries)

    input("\nPress Enter to continue ")
    clear()

def cancel_flight():
    view_flights()
    key = input("Type in Flight Schedule ID: ")

    flight_index, flight_entry = fm.query_key('flights', key)
    if flight_index == -1:
        clear()
        print("Couldn't find flight, returning to flights page...")
        input("\nPress Enter to continue ")
        clear()
        return
    
    display_header = ["Field", "Value"]
    display_item = []
    flight_fields = fm.get_field_names("flights")
    for i in range(len(flight_entry)):
        display_item.append([flight_fields[i], flight_entry[i]])
    clear()
    ext.view_table(display_header, display_item)

    confirmation = input("Do you want to cancel this flight? (Yes/No) : ")

    if confirmation.lower() in ["yes", "y"]:
        flight_entry[3] = "Cancelled"
        fm.update_file('flights', flight_entry)
        clear()
        print("Successfully cancelled flight.")
        input("\nPress Enter to continue ")
        clear()
        return
    clear()
    print("Cancelled action, returning to flights menu...")
    input("\nPress Enter to continue ")
    clear()
    return

def booking_ticket():
    booking_fields, booking_entries = fm.read_file('bookings')
    clear()
    ext.view_table(booking_fields,booking_entries)
    flight_booking = input("Enter a Booking ID to generate the flight ticket: ")


    booking_fields, booking_entries = fm.read_file('bookings')
    search_index, booking_entry = fm.query_key('bookings', flight_booking)
    if search_index == -1:
        clear()
        print("Couldn't find booking, returning to bookings page...")
        input("\nPress Enter to continue ")
        clear()
        return

    # Receipt
    clear()
    ext.report("Boarding Pass", booking_fields, booking_entry)
    input("\nPress Enter to continue ")
    clear()
    return

def generate_bill():
    booking_fields, booking_entries = fm.read_file('bookings')
    clear()
    ext.view_table(booking_fields,booking_entries)
    flight_booking = input("Enter a Booking ID : ")

    search_index, bookings_gen = fm.query_key('bookings', flight_booking)
    if search_index == -1:
        clear()
        print("Couldn't find booking, returning to bookings page...")
        input("\nPress Enter to continue ")
        clear()
        return

    booking_fields, booking_entries = fm.read_file('bookings')

    clear()
    ext.receipt(booking_fields, bookings_gen)
    input("\nPress Enter to continue ")
    clear()
    return

def search_booking():
    clear()
    booking_fields, booking_entries = fm.read_file('bookings')

    booking_filter = []

    while True:
        ext.view_table(booking_fields, booking_entries)
        input("\nPress Enter to continue ")
        

        ext.show_menu("Search by: ", booking_fields + ["Back"])
        try:
            choice = int(input("Please select: "))
            if choice in [-1, 11]:
                clear()
                print("Returning to bookings menu...")
                input("\nPress Enter to continue ")
                clear()
                return
            if choice == 1:
                key = input("Please enter the key to be searched: ")
                index, entry = fm.query_key("bookings", key)
                if index == -1:
                    clear()
                    print("No bookings found, returning to bookings menu...")
                    input("\nPress Enter to continue ")
                    clear()
                    return
                ext.view_table(booking_fields, [entry])
                input("\nPress Enter to continue ")
                clear()

            if choice in range(2, len(booking_fields) + 1):
                value = input(f"Please enter the value you want to search for the field {booking_fields[choice-1]}: ")
                booking_entries = fm.query_entries_field(booking_fields, booking_entries, booking_fields[choice-1], value)
                if len(booking_entries) == 0:
                    clear()
                    print("No bookings found, returning to bookings menu...")
                    input("\nPress Enter to continue ")
                    clear()
                booking_filter.append(f"The value {ext.bold(value)} in the field {ext.bold(booking_fields[choice-1])}")
                clear()
                print(f"The following bookings shown are filtered according to: ")
                for item in booking_filter:
                    print(item)
                print()
            else:
                clear()
                print("Invalid input, please input a valid number!")
                input("\nPress Enter to continue ")
                clear()
        except:
            clear()
            print("Invalid input, please input a valid number!")
            input("\nPress Enter to continue ")
            clear()

def generate_airline_report():
    
    airlines = ["MAS1709", "ZW1865", "ME2098", "APU8760"]
    clear()
    ext.show_menu("Generate Report", airlines)
    while True:
        choice = input("Select Airline to generate report : ")
        if choice == "-1":
            clear()
            print("Cancelled generating report, returning to airlines menu...")
            input("\nPress Enter to continue ")
            clear()
            return
        if choice in ["1", "2", "3", "4"]:
            break
        else:
            clear()
            print("Please enter a valid input.")
            input("\nPress Enter to continue ")
            clear()
    
    
    flight_fields, flight_entries = fm.read_file('flights')
    mas_flights = fm.query_entries_field(flight_fields, flight_entries, 'Airline ID', airlines[int(choice)-1])
    on_time_flights = fm.query_entries_field_strict(flight_fields, mas_flights, 'Status', 'On-time')
    delayed_flights = fm.query_entries_field_strict(flight_fields, mas_flights, 'Status', 'Delayed')
    cancelled_flights = fm.query_entries_field_strict(flight_fields, mas_flights, 'Status', 'Cancelled')
    x = len(on_time_flights)
    y = len(delayed_flights)
    z = len(cancelled_flights)
    time_format = '%H:%M:%S'
    date_format = '%Y-%m-%d'

    c = datetime.datetime.now()

    current_time = c.strftime(time_format)
    current_date = c.strftime(date_format)

    fm.generate_report(current_date)
    fm.generate_report(current_time)

    report = "airlines[int(choice)-1]"
    fm.generate_report(report)
    fm.generate_on_time_report(x)
    fm.generate_delayed_report(y)
    fm.generate_cancelled_report(z)

    fm.generate_report('')

    print("Successfully generated report.")
    input("\nPress Enter to continue ")
    clear()

def view_cancelled_bookings():
    clear()
    bookings_field, booking_entries = fm.read_file('bookings')
    query_fields = fm.query_entries_field_strict(bookings_field, booking_entries, 'Booking Status', 'Cancelled')
    ext.view_table(bookings_field, query_fields)
    input("\nPress Enter to continue ")
    clear()

main()




