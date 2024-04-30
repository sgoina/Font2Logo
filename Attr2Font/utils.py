import re
import os
from dataloader import get_loader
from torchvision.utils import save_image

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
    font_folders.remove('Ubuntu-Bold')
    
    return font_folders
def create_attribute_picture(opts,switch):
    log_dir = os.path.join("experiments", opts.experiment_name)
    results_dir = os.path.join(log_dir, "results")
    image_dir = os.path.join(opts.data_root, opts.dataset_name, "image")
    attribute_path = os.path.join(
        opts.data_root, opts.dataset_name, "attributes2.txt")
    test_dataloader = get_loader(image_dir, attribute_path,
                                 dataset_name=opts.dataset_name,
                                 image_size=opts.img_size,
                                 n_style=opts.n_style, batch_size=62,
                                 mode='test', binary=False)
    for test_idx, test_batch in enumerate(test_dataloader):
        test_img_A = test_batch['img_A']
        test_img_B = test_batch['img_B']
        #generates current font A picture for you to use 
        if switch == 'a':
            img_sample = test_img_A.data
            save_file = os.path.join(results_dir, f"all_characters_a.png")
            save_image(img_sample,save_file , nrow=62, normalize=True)
        #generates current font B picture for you to use     
        elif switch == 'b':
            img_sample = test_img_B.data
            save_file = os.path.join(results_dir, f"all_characters_b.png")
            save_image(img_sample,save_file, nrow=62, normalize=True)
    
  