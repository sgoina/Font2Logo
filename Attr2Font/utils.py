import re
import os


def update_file_except_png_numbers(file_path, new_name1, new_name2):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Identify the last two unique prefixes
    prefixes = set(line.split("/")[0] for line in lines if "/" in line)
    last_two_prefixes = sorted(prefixes)[-2:]

    # Update the lines with the new names and change all numbers except png numbers to 1
    updated_lines = []
    for line in lines:
        for old_prefix, new_prefix in zip(last_two_prefixes, [new_name1, new_name2]):
            # Check if the line starts with the old prefix followed by '/'
            if line.startswith(old_prefix + "/"):
                line = line.replace(old_prefix, new_prefix, 1)
                break
        # Replace all numbers except png numbers with 1
        line = re.sub(r'(?<!/)\b\d+\b', '1', line)
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
