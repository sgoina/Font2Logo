import re
import os
from dataloader import get_loader
from torchvision.utils import save_image
import torch
from torch import nn
from model import  GeneratorStyle
from minidataloader import get_font_attr
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
def parse_attributes_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    # Assuming the first line contains attribute names
    attribute_names = lines[0].strip().split()
    data = {}
    for line in lines[1:]:
        parts = line.strip().split()
        filename = parts[0]
        attribute_values = list(map(int, parts[1:]))
        data[filename] = attribute_values
    return attribute_names, data


def load_attribute_from_font(opts):
    # Dirs
    log_dir = os.path.join("experiments", opts.experiment_name)
    checkpoint_dir = os.path.join(log_dir, "checkpoint")
    results_dir = os.path.join(log_dir, "results")

    # Path to data
    image_dir = os.path.join(opts.data_root, opts.dataset_name, "image")
    attribute_path = os.path.join(
        opts.data_root, opts.dataset_name, "attributes.txt")
    
    new_attribute_path = os.path.join(
        opts.data_root, opts.dataset_name, "new_attributes.txt")
    
    with open(new_attribute_path, 'r') as file:
        data = file.readline().strip().split()
        new_attribute_array = [float(x) for x in data]

    new_attribute = []
    for attr in new_attribute_array:
        new_attribute.append(attr / 100.0)

    new_attribute = torch.FloatTensor(new_attribute)
    new_attribute = new_attribute.repeat(62, 1)

    # test_dataloader = get_loader(image_dir, attribute_path,
    #                              dataset_name=opts.dataset_name,
    #                              image_size=opts.img_size,
    #                              n_style=opts.n_style, batch_size=62,
    #                              mode='test', binary=False)

    # Model
    # 檢查loss的model
    # criterion_pixel = torch.nn.L1Loss().to(device)
    generator = GeneratorStyle(n_style=opts.n_style, attr_channel=opts.attr_channel,
                               style_out_channel=opts.style_out_channel,
                               n_res_blocks=opts.n_res_blocks,
                               attention=opts.attention)
    # Attrbute embedding
    # attribute: N x 37 -> N x 37 x 64
    attribute_embed = nn.Embedding(opts.attr_channel, opts.attr_embed)
    # unsupervise font num + 1 dummy id (for supervise)
    attr_unsuper_tolearn = nn.Embedding(
        opts.unsuper_num+1, opts.attr_channel)  # attribute intensity

    if opts.multi_gpu:
        generator = nn.DataParallel(generator)
        attribute_embed = nn.DataParallel(attribute_embed)
        attr_unsuper_tolearn = nn.DataParallel(attr_unsuper_tolearn)

    generator = generator.to(device)
    attribute_embed = attribute_embed.to(device)
    attr_unsuper_tolearn = attr_unsuper_tolearn.to(device)
    
    if opts.test_epoch == 0:
        #這邊只需要跑一次，test_epoch要對應使用者用到的epoch
        for test_epoch in range(opts.check_freq, opts.n_epochs+1, opts.check_freq):
            load(opts, test_epoch, attribute_path,
                           image_dir, checkpoint_dir, results_dir,
                           generator, attribute_embed, attr_unsuper_tolearn,
                           new_attribute)
    else:
        load(opts, opts.test_epoch, attribute_path,
                       image_dir, checkpoint_dir, results_dir,
                       generator, attribute_embed, attr_unsuper_tolearn,
                       new_attribute)


    
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
    
def load(opts, test_epoch, attribute_path,
                   image_dir, checkpoint_dir, results_dir,
                   generator, attribute_embed,
                   attr_unsuper_tolearn, new_attribute):
    print(f"Testing epoch: {test_epoch}")
    with torch.no_grad():
        gen_file = os.path.join(checkpoint_dir, f"G_{test_epoch}.pth")
        attribute_embed_file = os.path.join(
            checkpoint_dir, f"attribute_embed_{test_epoch}.pth")
        attr_unsuper_file = os.path.join(
            checkpoint_dir, f"attr_unsuper_embed_{test_epoch}.pth")

        generator.load_state_dict(torch.load(gen_file))
        attribute_embed.load_state_dict(torch.load(attribute_embed_file))
        attr_unsuper_tolearn.load_state_dict(torch.load(attr_unsuper_file))
        a = get_font_attr(attribute_path, opts.font_name, attr_unsuper_tolearn)
        new_attribute_path = os.path.join(
            opts.data_root, opts.dataset_name, "new_attributes.txt")
        # Clear the contents of new_attributes.txt file
        with open(new_attribute_path, 'w') as file:
            file.write('')
        print(a[0])
        # Write the values from a[0][0] to new_attributes.txt file
        with open(new_attribute_path, 'a') as file:
            for x in a[0]:
                x=x*100
                file.write(str(int(x.item())) + ' ')