import re
import os

def update_file_except_png_numbers(file_path, new_name1, new_name2):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Identify the unique prefixes
    prefixes = sorted(set(line.split("/")[0] for line in lines if "/" in line))

    # Find the last two unique prefixes based on their position in the file
    last_prefix = None
    second_last_prefix = None
    for line in reversed(lines):
        if "/" in line:
            prefix = line.split("/")[0]
            if prefix != last_prefix:
                if last_prefix is None:
                    last_prefix = prefix
                else:
                    second_last_prefix = prefix
                    break

    # Update the lines with the new names and change all numbers except png numbers to 1
    updated_lines = []
    for line in lines:
        if line.startswith(last_prefix + "/"):
            line = line.replace(last_prefix, new_name1, 1)
        elif line.startswith(second_last_prefix + "/"):
            line = line.replace(second_last_prefix, new_name2, 1)

        # Replace all numbers except png numbers with 1
        line = re.sub(r'(?<!/)\\b\\d+\\b', '1', line)
        updated_lines.append(line)

    # Write the updated content back to the file
    with open(file_path, 'w') as file:
        file.writelines(updated_lines)

    return "File updated successfully."

def get_last_prefix(filename):
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()
            if not lines:
                return "No lines found in the file."

            last_line = lines[-1]
            last_prefix = last_line.split('/')[0]
            return last_prefix
    except FileNotFoundError:
        return "File not found."


def get_font_folder_names(directory_path):
    # List to store folder names
    font_folders = []

    # Loop through all items in the directory
    for item in os.listdir(directory_path):
        # Full path of the item
        item_path = os.path.join(directory_path, item)

        # Check if the item is a directory
        if os.path.isdir(item_path):
            font_folders.append(item)

    return font_folders
