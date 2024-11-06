"""
# File Manage Module
This module provides the functionalities that a database would have. 

## Basic Features:
- `read_file` - reads the file
- `write_file` - overwrites the file with new data
- `append_file` - appends new entries to the file
- `query_key` - queries for an entry based on the key given
- `update_file` - updates an entry based on the key and data given
- `delete_entry` - deletes the entry based on the key given

## Additional Features:
- `query_field` - gets the entries that are similar to the value in the field.
- `query_field_strict` - gets the entries that matches the value in the field.
- `get_field_names` - gets the field names in the specified file.

"""


def read_file(filename : str) -> tuple:
    """
    Reads the data in `filename`.

    # Parameters
    `filename` : `str`
        The name of the file to be read. Do not include the file extension in `filename`.

    # Returns
    A tuple with two elements:
        `(field_names, values)`

    - `field_names` : `list`\\
        The name of the different fields in the text file
    - `values` : `list`\\
        A list of `entry` in the text file
        - `entry` : `list`\\
            A list of fields of an entry

    # Raises
    ### FileNotFoundError
    - If the specified file `filename` is not found.

    # Usage
    ### Reading the file
    >>> value = read_file('airlines')
    >>> value
    (['AirlineID', 'AirlineName', 'TotalFlights'], [['ZW1865', 'Air Asia', '50'], ['MAS1709', 'Malaysia Airline', '109']])
    >>> value[0]
    ['AirlineID', 'AirlineName', 'TotalFlights']
    >>> value[1]
    [['ZW1865', 'Air Asia', '50'], ['MAS1709', 'Malaysia Airline', '109']]
    >>> value[1][0]
    ['ZW1865', 'Air Asia', '50']
    """
    # Get data from file, and storing it into the variable `data`
    try:
        with open(f'data/{filename}.txt', 'r') as f:
            data = f.readlines()
    except FileNotFoundError as e:
        raise FileNotFoundError(f"'data/{filename}.txt' is not found, please check your code again.")

    # Get field names
    field_names = data[0].strip().split(';')
    data.pop(0)

    values = []
    for item in data:
        values.append(item.strip().split(';'))

    return (field_names, values)

def write_file(filename : str, new_data : list) -> tuple:
    """
    Completely writes `new_data` into `filename` and returns the updated data.

    # Parameters
    ### `filename` : `str`
    The name of the file to be written. Do not include the file extension in `filename`.
    
    ### `new_data` : `list`
    The list of entries to be written into `filename`. No semicolons `;` should be present in any item in each entry.

    # Returns
    A tuple with two elements:
        `(field_names, values)`

    - `field_names` : `list`\\
        The name of the different fields in the text file
    - `values` : `list`\\
        A list of `entry` in the text file
        - `entry` : `list`\\
            A list of fields of an entry

    # Raises
    ### FileNotFoundError
    - If the specified file (`filename`) is not found.

    ### ValueError
    - If there contains a semicolon in any item in any entry.
    - If the number of fields in `new_data` does not match the expected number of fields in the file.
    - If there are duplicate key in the data.

    # Usage
    ### Writing data into file:
    >>> new_data = [['ZW1865', 'Air Asia', '1000'], ['MAS1709', 'Airline', '109']]
    >>> write_file('airlines', new_data)
    (['AirlineID', 'AirlineName', 'TotalFlights'], [['ZW1865', 'Air Asia', '1000'], ['MAS1709', 'Airline', '109']])
    """
    # Check if items have semicolon
    for entry_index in range(len(new_data)):
        for item in new_data[entry_index]:
            if ';' in item:
                raise ValueError(f"It seems that there exists a semicolon in the item '{item}' in entry number {entry_index} with value {new_data[entry_index]}. \nPlease check your code again to ensure that there are no semicolons in every item.\n")

    # Check if items have duplicate key
    for entry_index in range(len(new_data)):
        for compared_index in range(entry_index+1, len(new_data)):
            if new_data[entry_index][0] == new_data[compared_index][0]:
                raise ValueError(f"There are duplicates of the same key in your data. \nPlease check your code again to ensure that the key inserted is unique.")

    for index in range(len(new_data)):
        new_data[index] = ';'.join(new_data[index]) + "\n"
    
    try:
        with open(f"data/{filename}.txt", "r") as f:
            data = f.readlines()

        new_data = [data[0]] + new_data
        write_string = "".join(new_data)
        field_names = new_data[0].strip().split(';')

        values = []
        for item in new_data[1:]:
            values.append(item.strip().split(';'))
        
        # Check if same number of fields
        for entry_index in range(len(values)):
            if len(values[entry_index]) != len(field_names):
                raise ValueError(f"Wanted field is {len(field_names)}, {len(values[entry_index])} fields is received at entry number {entry_index}.\nPlease check your code again to ensure that the number of fields matches.")

        with open(f"data/{filename}.txt", "w") as f:
            f.write(write_string)
        return (field_names, values)
    except FileNotFoundError:
        raise FileNotFoundError(f"'data/{filename}.txt' is not found, please check your code again.")

def append_file(filename : str, values : list) -> tuple:
    """
    Appends a single or multiple `entry` into `filename`.

    # Parameters
    ### `filename` : `str`
    The name of the file to be written. Do not include the file extension in `filename`.
    
    ### `values` : `list`
    The list of entries to be appended into `filename`. No semicolons `;` should be present in any item in each entry.

    # Returns
    A tuple with two elements:
        `(field_names, values)`

    - `field_names` : `list`\\
        The name of the different fields in the text file
    - `values` : `list`\\
        A list of `entry` in the text file
        - `entry` : `list`\\
            A list of fields of an entry

    # Raises
    ### FileNotFoundError
    - If the specified file (`filename`) is not found.

    ### ValueError
    - If there contains a semicolon in any item in any entry.
    - If the number of fields in `new_data` does not match the expected number of fields in the file.
    - If there are duplicate key in the data.

    # Usage
    ### Append one entry into file:
    >>> entry = [['AK','AK Airlines','2000']]
    >>> append_file('airlines', entry)
    (['AirlineID', 'AirlineName', 'TotalFlights'], [['ZW1865', 'Air Asia', '50'], ['MAS1709', 'Malaysia Airlines', '109'], ['AK', 'AK Airlines', '2000']])
    
    ### Append multiple entries into file:
    >>> entry = [['AK', 'AK Airlines', '2000'], ['HSF', 'Hosef Airlines', '99']]
    >>> append_file('airlines', entry)
    (['AirlineID', 'AirlineName', 'TotalFlights'], [['ZW1865', 'Air Asia', '50'], ['MAS1709', 'Malaysia Airlines', '109'], ['AK', 'AK Airlines', '2000'], ['HSF', 'Hosef Airlines', '99']])
    """
    # Check if items have semicolon
    for entry_index in range(len(values)):
        for item in values[entry_index]:
            if ';' in item:
                raise ValueError(f"It seems that there exists a semicolon in the item '{item}' in entry number {entry_index} with value {values[entry_index]}. \nPlease check your code again to ensure that there are no semicolons in every item.\n")
    
    new_data = []

    for index in range(len(values)):
        new_data.append(';'.join(values[index]) + "\n")
    
    try:
        with open(f"data/{filename}.txt", "r") as f:
            data = f.readlines()

        # Checks for unneccesary newlines in file and removes it
        for index in range(len(data)-1,-1,-1):
            if data[index] == "\n":
                data.pop(index)

        # Check if last item has newline and fixes if not
        if len(data) != 1:
            data[-1] = data[-1].strip()
            data[-1] += "\n"
        new_data = data + new_data
        
        write_string = "".join(new_data)
        field_names = new_data[0].strip().split(';')
        
        return_values = []
        for item in new_data[1:]:
            return_values.append(item.strip().split(';'))

        # Check if items have duplicate key
        for entry_index in range(len(return_values)):
            for compared_index in range(entry_index+1, len(return_values)):
                if return_values[entry_index][0] == return_values[compared_index][0]:
                    raise ValueError(f"There are duplicates of the same key in your data. \nPlease check your code again to ensure that the key inserted is unique.")

        # Check if same number of fields
        for entry_index in range(len(values)):
            if len(values[entry_index]) != len(field_names):
                raise ValueError(f"Wanted field is {len(field_names)}, {len(values[entry_index])} fields is received at entry number {entry_index}.\nPlease check your code again to ensure that the number of fields matches.")
        
        with open(f"data/{filename}.txt", "w") as f:
            f.write(write_string)
            return (field_names, return_values)
    except FileNotFoundError:
        raise FileNotFoundError(f"'data/{filename}.txt' is not found, please check your code again.")

def query_key(filename : str, key : str) -> tuple:
    """
    Gets the entry for the `key` in `filename`.

    # Parameters
    ### `filename` : `str`
    The name of the file to be searched. Do not include the file extension in `filename`.

    ### `key` : `str`
    The key to search the entry in the file.

    # Returns
    A tuple with two elements:
        `(index, entry)`

    - `index` : `int`\\
        The index of the entry found in `filename`. Returns -1 if no entry is found.
    - `entry` : `list`\\
        The list that contains information about the queried entry. Returns an empty list if no entry is found.

    # Raises
    ### FileNotFoundError
    - If the specified file `filename` is not found.

    # Usage
    ### Querying the file (entry found)
    >>> key = 'ZW1865'
    >>> query_key('airlines', key)
    (0, ['ZW1865,', 'Air Asia', '1000'])
    
    ### Querying the file (entry not found)
    >>> key = 'testkey!'
    >>> query_key('airlines', key)
    (-1, [])
    """
    # Get data from file, and storing it into the variable `data`
    try:
        with open(f'data/{filename}.txt', 'r') as f:
            data = f.readlines()
    except FileNotFoundError as e:
        raise FileNotFoundError(f"'data/{filename}.txt' is not found, please check your code again.")
    
    for index in range(len(data[1:])):
        entry = (data[1:])[index].strip().split(';')
        if entry[0] == key:
            return (index, entry)
    return (-1,[])

def update_file(filename : str, new_entry : list) -> bool:
    """
    Updates a particular entry with `new_entry` that matches `key` as its unique key.

    # Parameters
    ### `filename` : `str`
    The name of the file to be updated. Do not include the file extension in `filename`.

    ### `new_entry` : `list`
    The new entry to be written in the searched entry.

    # Returns
    A bool that returns `True` if the entry is successfully updated, `False` if the entry is not successfully updated.

    # Raises
    ### FileNotFoundError
    - If the specified file `filename` is not found.

    ### ValueError
    - If there contains a semicolon in any item.
    - If the number of fields in `new_entry` does not match the expected number of fields in the file.

    # Usage
    ### Update an entry in the file (entry found):
    Note: We are updating a particular entry according to what the unique key in `new_entry` is, therefore the unique key is very important.
    >>> new_entry = ['ZW1865', 'Air Asia', '1000']
    >>> update_file('airlines', new_entry)
    True

    ### Update an entry in the file (entry not found):
    >>> new_entry = ['ZW1864', 'Air Asia', '1000']
    >>> update_file('airlines', new_entry)
    False
    """
    # Check if items have semicolon
    for item in new_entry:
        if ';' in item:
            raise ValueError(f"It seems that there exists a semicolon in the item '{item}'. \nPlease check your code again to ensure that there are no semicolons in every item.\n")

    key = new_entry[0]
    index, entry = query_key(filename, key)
    
    if index == -1:
        return False

    # Check if same number of fields
    if len(new_entry) != len(entry):
        raise ValueError(f"Wanted field is {len(entry)}, {len(new_entry)} fields is received.\nPlease check your code again to ensure that the number of fields matches.")

    field_names, values = read_file(filename)
    values[index] = new_entry
    write_file(filename, values)
    return True

def delete_entry(filename : str, key : str) -> bool:
    """
    Deletes a particular entry that matches `key` as its unique key.

    # Parameters
    ### `filename` : `str`
    The name of the file to be accessed. Do not include the file extension in `filename`.

    ### `key` : `str`
    The key to be deleted

    # Returns
    A bool that returns `True` if the entry is successfully deleted, `False` if the entry is not successfully deleted.

    # Raises
    ### FileNotFoundError
    - If the specified file `filename` is not found.

    # Usage
    ### Delete an entry in the file (entry found)
    >>> key = 'ZW1865'
    >>> delete_entry('airlines', key)
    True

    ### Delete an entry in the file (entry not found)
    >>> key = 'ZW1965'
    >>> delete_entry('airlines', key)
    False
    """
    index, entry = query_key(filename, key)
    
    if index == -1:
        return False
    
    field_names, values = read_file(filename)
    values.pop(index)
    write_file(filename, values)
    return True

def query_entries_field(field_names: list, entries: list, field: str, value: str) -> list:
    """
    Gets the entries that are similar to the `value` in the `field` in the `entries` passed in.

    # Parameters
    ### `field_names` : `list`
    The list of field names for the given entries.

    ### `entries` : `list`
    The list of entries to be filtered.

    ### `field` : `str`
    The name of the field to be searched.

    ### `value` : `str`
    The value to be searched for in the field.

    # Returns
    A list of entries that are found similar

    - `values` : `list`\\
        A list of `entry` in the text file
        - `entry` : `list`\\
            A list of fields of an entry

    # Raises
    ### ValueError
    - If `field` is the same as the key in the file.
    - If `field` is not one of the field in the file.
    """

    # Check if field length and entries are same length
    for entry in entries:
        if len(entry) != len(field_names):
            raise ValueError("The length of the field and entries are not the same length. \nPlease check your code again to ensure that the length of them are the same.")

    # Check if field is key
    if field_names[0] == field:
        raise ValueError("The field is the same as the unique key.\nPlease check your code again to ensure that the field passed in is not the unique key.")

    # Get field number
    index = field_names.index(field)
    if index == -1:
        raise ValueError("The field given is not found in the entries.\nPlease check your code again to ensure that the field passed in is correct.")
    
    return_entries = []
    for entry in entries:
        if value.lower() in entry[index].lower():
            return_entries.append(entry)
    return return_entries

def query_entries_field_strict(field_names, entries, field, value):
    """
    Gets the entries that matches `value` in the `field` in the `entries` passed in.

    # Parameters
    ### `field_names` : `list`
    The list of field names for the given entries.

    ### `entries` : `list`
    The list of entries to be filtered.

    ### `field` : `str`
    The name of the field to be searched.

    ### `value` : `str`
    The value to be searched for in the field.

    # Returns
    A list of entries that matched

    - `values` : `list`\\
        A list of `entry` in the text file
        - `entry` : `list`\\
            A list of fields of an entry

    # Raises
    ### ValueError
    - If `field` is the same as the key in the file.
    - If `field` is not one of the field in the file.
    """

    # Check if field length and entries are same length
    for entry in entries:
        if len(entry) != len(field_names):
            raise ValueError("The length of the field and entries are not the same length. \nPlease check your code again to ensure that the length of them are the same.")

    # Check if field is key
    if field_names[0] == field:
        raise ValueError("The field is the same as the unique key.\nPlease check your code again to ensure that the field passed in is not the unique key.")

    # Get field number
    index = field_names.index(field)
    if index == -1:
        raise ValueError("The field given is not found in the file.\nPlease check your code again to ensure that the field passed in is correct.")
    
    return_entries = []
    for entry in entries:
        if value == entry[index]:
            return_entries.append(entry)
    return return_entries

def query_field(filename: str, field: str, value: str) -> list:
    """
    Gets the entries that are similar to the `value` in the `field` in the file.

    # Parameters
    ### `filename` : `str`
    The name of the file to be searched. Do not include the file extension in `filename`.

    ### `field` : `str`
    The name of the field to be searched.

    ### `value` : `str`
    The value to be searched for in the field.

    # Returns
    A list of entries that are found similar

    - `values` : `list`\\
        A list of `entry` in the text file
        - `entry` : `list`\\
            A list of fields of an entry

    # Raises
    ### FileNotFoundError
    - If the specified file `filename` is not found.

    ### ValueError
    - If `field` is the same as the key in the file.
    - If `field` is not one of the field in the file.
    """
    field_names, data = read_file(filename)

    return query_entries_field(field_names, data, field, value)

def query_field_strict(filename: str, field: str, value: str) -> list:
    """
    Gets the entries that matches `value` in the `field` in the file.

    # Parameters
    ### `filename` : `str`
    The name of the file to be searched. Do not include the file extension in `filename`.

    ### `field` : `str`
    The name of the field to be searched.

    ### `value` : `str`
    The value to be searched for in the field.

    # Returns
    A list of entries that matched

    - `values` : `list`\\
        A list of `entry` in the text file
        - `entry` : `list`\\
            A list of fields of an entry

    # Raises
    ### FileNotFoundError
    - If the specified file `filename` is not found.

    ### ValueError
    - If `field` is the same as the key in the file.
    - If `field` is not one of the field in the file.
    """
    field_names, data = read_file(filename)

    return query_entries_field_strict(field_names, data, field, value)

def get_field_names(filename: str) -> list:
    try:
        with open(f'data/{filename}.txt', 'r') as f:
            data = f.readlines()
    except FileNotFoundError as e:
        raise FileNotFoundError(f"'data/{filename}.txt' is not found, please check your code again.")
    return data[0].strip().split(";")

def generate_on_time_report(report):
    with open('data/reports.txt', 'a') as f:
        f.write(f"On-time: {report}\n")

def generate_cancelled_report(report):
    with open('data/reports.txt', 'a') as f:
        f.write(f"Cancelled: {report}\n")

def generate_delayed_report(report):
    with open('data/reports.txt', 'a') as f:
        f.write(f"Delayed: {report}\n")

def generate_report(report):
    with open('data/reports.txt', 'a') as f:
        f.write(str(report) + "\n")

