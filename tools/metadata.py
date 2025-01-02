# THIS FILE DOES NOT WORK WHEN EXECUTED ALONE.

def set_metadata(file, metadata_name, metadata_value):
    """
    Update or add a metadata entry in the specified Python file.

    Parameters:
        file (str): The path to the Python file to edit.
        metadata_name (str): The name of the metadata variable to set.
        metadata_value (str): The value to assign to the metadata variable.
    """
    # Read the contents of the file
    with open(file, 'r') as f:
        lines = f.readlines()

    # Initialize variables
    in_metadata_section = False
    new_lines = []
    updated = False
    if metadata_value == "true":
        metadata_value = True
    elif metadata_value == "false":
        metadata_value = False

    for line in lines:
        # Check for the start of the metadata section
        if line.strip() == '# METADATA':
            in_metadata_section = True
            new_lines.append(line)
            continue
        
        # Check for the end of the metadata section
        if line.strip() == '# METADATA ENDS':
            in_metadata_section = False
            new_lines.append(line)
            continue
        
        if in_metadata_section:
            # Check if we need to update an existing metadata entry
            if line.startswith(metadata_name + ' ='):
                new_lines.append(f"{metadata_name} = {repr(metadata_value)}\n")
                updated = True
            else:
                new_lines.append(line)
        else:
            new_lines.append(line)

    # If the metadata entry was not found, add it at the end of the section
    if not updated and in_metadata_section:
        new_lines.insert(-1, f"{metadata_name} = {repr(metadata_value)}\n")

    # Write back to the file
    with open(file, 'w') as f:
        f.writelines(new_lines)
