import json
from string import Formatter

def read_json(file):
    file_name = file if file.endswith('.json') else file + '.json'
    with open(file_name, 'r') as f:
        return json.load(f)
    
def write_json(file, content):
    file_name = file if file.endswith('.json') else file + '.json'
    with open(file_name, 'w') as f:
        try:
            json.dump(content, f)
            return True
        except:
            return False
        
def fstring_keys(fstring):
    keys = [part[1] for part in Formatter().parse(fstring) if part[1] is not None]
    return keys

def format_xpath(fstring, vals):
    # Get the number of placeholders in the format string
    fstring_len = len(fstring_keys(fstring))
    
    # Check if the provided values are a string, list, or tuple
    if isinstance(vals, (str, list, tuple)):
        
        # If the values are a string or less than the number of placeholders
        if isinstance(vals, str) or len(vals) < fstring_len :
            # Convert the string to a list or unpack the values into a list
            list_of_vals = [vals] if isinstance(vals, str) else [*vals]
            
            # Calculate the difference between the number of placeholders and the number of values
            difference = fstring_len - len(list_of_vals)
            
            # Append empty strings to the list of values to match the number of placeholders
            values = list_of_vals + ['' for _ in range(difference)]
        
        # If the number of values is more than the number of placeholders
        elif len(vals) > fstring_len:
            # Trim the list of values to match the number of placeholders
            values = [*vals][:fstring_len]
        
        # If the number of values matches the number of placeholders
        else:
            # Unpack the values into a list
            values = [*vals]
        
        # Return the format string with the placeholders replaced by the values
        return fstring.format(*values)
    
    # If the provided values are not a string, list, or tuple, raise a TypeError
    else:
        raise TypeError('Must be a string, a list or a tuple')