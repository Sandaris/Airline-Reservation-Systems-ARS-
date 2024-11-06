import time

# General functions
def list_sum(li):
    total = 0
    for item in li:
        total += item
    return total

def sort_entries(entries: list, sort_column: int, reverse=False) -> list:
    # Using mergesort algorithm to sort
    if sort_column not in range(0, len(entries[0])):
        raise ValueError("The sort_column passed in does not match the number of fields in entries.\n Please check your code again to ensure the sort_column is correct.")
    n = len(entries)
    result = []
    if n > 1:
        midpoint = n // 2
        left = entries[:midpoint]
        right = entries[midpoint:]
        left = sort_entries(left, sort_column)
        right = sort_entries(right, sort_column)
        x = 0
        y = 0

        while x < len(left) and y < len(right):
            # print(left[x][sort_column], right[y][sort_column])
            if int(left[x][sort_column]) < int(right[y][sort_column]):
                result.append(left[x])
                x += 1
            else:
                result.append(right[y])
                y += 1
        
        while x < len(left):
            result.append(left[x])
            x += 1

        while y < len(right):
            result.append(right[y])
            y += 1
        
        if reverse:
            temp = []
            for i in range(len(result)-1, -1, -1):
                temp.append(result[i])
            result = temp
        return result
    else:
        return entries
    
def remove_fields(field_names: list, entries: list, remove_fields: list) -> tuple:
    '''Removes the fields in both `field_names` and `entries`.'''
    for entry in entries:
        if len(field_names) != len(entry):
            raise ValueError("The number of fields in field_names and entries are not the same.\nPlease check your code again to ensure that the fields of field_names and entries are the same.")

    remove_list = []
    for field in remove_fields:
        remove_list.append(field_names.index(field))

    updated_fields = []
    updated_entries = []
    for i in range(len(field_names)):
        if i in remove_list:
            continue
        updated_fields.append(field_names[i])

    for entry in entries:
        new_entry = []
        for i in range(len(entry)):
            if i in remove_list:
                continue
            new_entry.append(entry[i])
        updated_entries.append(new_entry)

    return updated_fields, updated_entries

# Functions for viewing and outputs

def bold(text: str) -> str:
    return f"\033[1m{text}\033[0m"

def view_table(field_names: list, data: list) -> None:
    for entry in data:
        if len(field_names) != len(entry):
            raise ValueError("The number of fields in field_names and data are not the same.\nPlease check your code again to sure that the number of fields in them are the same.")
    max_widths = []
    for field in field_names:
        max_widths.append(len(field))

    for entry in data:
        for i in range(len(entry)):
            if len(entry[i]) > max_widths[i]:
                max_widths[i] = len(entry[i])
    
    print(end="|")
    for i in range(len(field_names)):
        print(" " + bold(field_names[i]) + " "*(max_widths[i]-len(field_names[i])+1), end="|")
        
    total_len = list_sum(max_widths) + len(max_widths)*(3)+1
    print("\n"+"-"*total_len)
    for entry in data:
        print(end="|")
        for i in range(len(entry)):
            print(" " + entry[i] + " "*(max_widths[i]-len(entry[i])+1), end="|")
        print()
        time.sleep(0.02)

def show_menu(title: str, options: list) -> None:
    if title != "":
        print(f'\n\033[1m{title}\033[0m')
    max_index = len(options)//10+1
    for i in range(len(options)):
        print(f"  \033[1m{i+1}.\033[0m{' '*(max_index-((i+1)//10 + 1)+1)}{options[i]}")
    
def report(report_title, booking_fields, booking_entry):
    field_name_max = 0
    field_max = 0
    for i in range(len(booking_fields)):
        if field_name_max < len(booking_fields[i]):
            field_name_max = len(booking_fields[i])
        if field_max < len(booking_entry[i]):
            field_max = len(booking_entry[i])
    if (field_name_max + field_max + len(report_title))%2 == 0:
        field_max += 1
    print("-"*(field_name_max + field_max + 7))
    print("|"+" "*((field_name_max + field_max + 7 - len(report_title))//2 - 1) + bold(report_title) + " "*((field_name_max + field_max + 7 - len(report_title))//2 - 1) + "|")
    print("-"*(field_name_max + field_max + 7))
    for i in range(len(booking_fields)):
        print(f"| {booking_fields[i]} {' '*(field_name_max-len(booking_fields[i]))}: {booking_entry[i]}{' '*(field_max-len(booking_entry[i]))} |")
    print("-"*(field_name_max + field_max + 7))
    
def receipt(booking_fields, booking_entry):

    field_name_max = 0
    field_max = 0
    for i in range(len(booking_fields)):
        if field_name_max < len(booking_fields[i]):
            field_name_max = len(booking_fields[i])
        if field_max < len(booking_entry[i]):
            field_max = len(booking_entry[i])
    if (field_name_max + field_max + len("Receipt"))%2 == 0:
        field_max += 1
    print("-"*(field_name_max + field_max + 7))
    print("|"+" "*((field_name_max + field_max + 7 - len("Receipt"))//2 - 1) + bold("Receipt") + " "*((field_name_max + field_max + 7 - len("Receipt"))//2 - 1) + "|")
    print("-"*(field_name_max + field_max + 7))
    for i in range(0, 8):
        print(f"| {booking_fields[i]} {' '*(field_name_max-len(booking_fields[i]))}: {booking_entry[i]}{' '*(field_max-len(booking_entry[i]))} |")
    print(f"| {booking_fields[9]} {' '*(field_name_max-len(booking_fields[9]))}: {booking_entry[9]}{' '*(field_max-len(booking_entry[9]))} |")
    print("-"*(field_name_max + field_max + 7))
    print(f"| {booking_fields[8]} {' '*(field_name_max-len(booking_fields[8]))}: {booking_entry[8]}{' '*(field_max-len(booking_entry[8]))} |")
    print("-"*(field_name_max + field_max + 7))