import os
import random

import torch
from torch import nn
import torchvision.transforms as T
from PIL import Image
from torch.utils import data
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


def rreplace(s, old, new, occurrence):
    li = s.rsplit(old, occurrence)
    return new.join(li)


def rreplace(s, old, new, occurrence):
    li = s.rsplit(old, occurrence)
    return new.join(li)


class ImageAttr(data.Dataset):
    """Dataset class for the ImageAttr dataset."""

    def __init__(self, image_dir, attr_path, transform, mode,
                 binary=False, n_style=4,
                 char_num=62, unsuper_num=968, train_num=120, val_num=28):
        """Initialize and preprocess the ImageAttr dataset."""
        self.image_dir = image_dir
        self.attr_path = attr_path
        self.n_style = n_style

        self.transform = transform
        self.mode = mode
        self.binary = binary

        self.super_train_dataset = []
        self.super_test_dataset = []
        self.unsuper_train_dataset = []

        self.attr2idx = {}
        self.idx2attr = {}

        self.char_num = char_num
        self.unsupervised_font_num = unsuper_num
        self.train_font_num = train_num
        self.val_font_num = val_num

        self.test_super_unsuper = {}
        for super_font in range(self.train_font_num+self.val_font_num):
            self.test_super_unsuper[super_font] = random.randint(
                0, self.unsupervised_font_num - 1)

        self.char_idx_offset = 0

        self.chars = [c for c in range(
            self.char_idx_offset, self.char_idx_offset+self.char_num)]

        self.preprocess()

        if mode == 'train':
            self.num_images = len(self.super_train_dataset) + \
                len(self.unsuper_train_dataset)
            # print(len(self.super_train_dataset))
            # print(len(self.unsuper_train_dataset))
        else:
            self.num_images = len(self.super_test_dataset)
            print(len(self.super_test_dataset))

    def preprocess(self):
        """Preprocess the font attribute file."""
        lines = [line.rstrip() for line in open(self.attr_path, 'r')]
        all_attr_names = lines[0].split()
        for i, attr_name in enumerate(all_attr_names):
            self.attr2idx[attr_name] = i
            self.idx2attr[i] = attr_name

        lines = lines[1:]

        train_size = self.char_num * self.train_font_num
        val_size = self.char_num * self.val_font_num

        for i, line in enumerate(lines):
            split = line.split()
            filename = split[0]
            values = split[1:]
            target_char = filename.split('/')[1].split('.')[0]
            char_class = int(target_char) - self.char_idx_offset
            font_class = int(i / self.char_num)

            attr_value = []
            for val in values:
                if self.binary:
                    attr_value.append(val == '1')
                else:
                    attr_value.append(eval(val) / 100.0)

            # print(filename, char_class, font_class)
            # print(f'i {i}')
            # print(f'train size {train_size}')
            # print(f'self.char_num {self.char_num} val_size {val_size}')
            # print(f'testdatasetlength {len(self.super_test_dataset)}')
            # print(f'usupertrain {len(self.unsuper_train_dataset)}')
            # print(f'supertrain {len(self.super_train_dataset)}')
            if i < train_size:
                self.super_train_dataset.append(
                    [filename, char_class, font_class, attr_value])
            elif i < train_size + val_size:
                self.super_test_dataset.append(
                    [filename, char_class, font_class, attr_value])
            else:
                self.unsuper_train_dataset.append(
                    [filename, char_class, font_class, attr_value])

        print('Finished preprocessing the Image Attribute (Explo) dataset...')

    def __getitem__(self, index):
        """Return one image and its corresponding attribute label."""
        # dataset = self.super_train_dataset if self.mode == 'train' else self.super_test_dataset

        # load the random one from unsupervise data as the reference aka A
        # unsuper to super
        font_index_super = index // self.char_num + self.train_font_num
        font_index_unsuper = self.test_super_unsuper[font_index_super]
        char_index_unsuper = index % self.char_num + self.char_num * font_index_unsuper
        filename_A, charclass_A, fontclass_A, attr_A = self.unsuper_train_dataset[
            char_index_unsuper]
        label_A = 0.0
        font_embed_A = fontclass_A - self.train_font_num - self.val_font_num  # convert to [0, 967]
        # Get style samples
        random.shuffle(self.chars)
        style_chars = self.chars[:self.n_style]
        styles_A = []
        if self.n_style == 1:
            styles_A.append(filename_A)
        else:
            for char in style_chars:
                styles_A.append(
                    rreplace(filename_A, str(charclass_A).zfill(2), str(char).zfill(2), 1))
                # print(rreplace(filename_A, str(charclass_A).zfill(2), str(char), 1))
                # print(f'this is {filename_A}')

        image_A = Image.open(os.path.join(
            self.image_dir, filename_A)).convert('RGB')
        # Open and transform style images
        style_imgs_A = []
        for style_A in styles_A:
            style_imgs_A.append(self.transform(Image.open(
                os.path.join(self.image_dir, style_A)).convert('RGB')))
        style_imgs_A = torch.cat(style_imgs_A)

        return {"img_A": self.transform(image_A), "charclass_A": torch.LongTensor([charclass_A]),
                "fontclass_A": torch.LongTensor([fontclass_A]), "attr_A": torch.FloatTensor(attr_A),
                "styles_A": style_imgs_A,
                "fontembed_A": torch.LongTensor([font_embed_A]),
                "label_A": torch.FloatTensor([label_A])}

    def __len__(self):
        """Return the number of images."""
        return self.num_images


def get_loader(image_dir, attr_path, image_size=256,
               batch_size=16, dataset_name='explor_all', mode='train', num_workers=8,
               binary=False, n_style=4,
               char_num=62, unsuper_num=968, train_num=120, val_num=28):
    """Build and return a data loader."""
    transform = []
    transform.append(T.Resize(image_size))
    transform.append(T.ToTensor())
    transform.append(T.Normalize(mean=(0.5, 0.5, 0.5), std=(0.5, 0.5, 0.5)))
    transform = T.Compose(transform)

    if dataset_name == 'explor_all':
        dataset = ImageAttr(image_dir, attr_path, transform,
                            mode, binary, n_style,
                            char_num=62, unsuper_num=968,
                            train_num=120, val_num=28)
    data_loader = data.DataLoader(dataset=dataset,
                                  drop_last=True,
                                  batch_size=batch_size,
                                  shuffle=(mode == 'train'),
                                  num_workers=num_workers)

    return data_loader


def get_test_data(image_dir, attr_path, font_name, image_size=256, experiment_name='explor_all', n_style=4,
                  char_num=62, unsuper_num=968, super_num = 148):
    transform = []
    transform.append(T.Resize(image_size))
    transform.append(T.ToTensor())
    transform.append(T.Normalize(mean=(0.5, 0.5, 0.5), std=(0.5, 0.5, 0.5)))
    transform = T.Compose(transform)

    with open(attr_path, 'r') as file:
        for line_num, line in enumerate(file, start=1):
            if font_name in line:
                print(line_num)
                break
    line_num -= 1
    font_num = line_num // char_num
    img = torch.empty(char_num, 3, image_size, image_size)
    img_folder_path = os.path.join(image_dir, font_name)
    index = 0
    for filename in sorted(os.listdir(img_folder_path)):
        print(filename)
        if filename.endswith('.png'):
            image = Image.open(os.path.join(img_folder_path, filename)).convert('RGB')
            img[index] = transform(image)
            
            index += 1

    source_style = torch.empty(char_num, 3 * n_style, image_size, image_size)
    index = 0
    for filename in os.listdir(img_folder_path):
        chars = [c for c in range(0, char_num)]
        random.shuffle(chars)
        styles = []
        style_chars = chars[:n_style]
        charclass = int(filename.split('.')[0])
        if n_style == 1:
                styles.append(filename)
        else:
            for char in style_chars:
                styles.append(
                    rreplace(filename, str(charclass).zfill(2), str(char).zfill(2), 1))

        style_imgs = []
        for style in styles:
            style_imgs.append(transform(Image.open(os.path.join(image_dir, font_name, style)).convert('RGB')))
        style_imgs = torch.cat(style_imgs)
        source_style[index] = style_imgs
        index += 1
    #User chooses a super_font
    if (font_num < super_num):
        print('super')
    #User chooses a unsuper_font
    else:
        print('unsuper')

    return font_num, img, source_style

def get_font_attr(attr_path, font_name, attr_unsuper_tolearn, char_num = 62):
    with open(attr_path, 'r') as file:
        for line_num, line in enumerate(file, start=1):
            if font_name in line:
                break
    line_num -= 1
    font_num = line_num // char_num
    print(font_num)
    if (line_num // char_num < 148): 
        values = line.strip().split()[1:]
        float_values = [eval(value)/100.0 for value in values]
        attr_values = torch.FloatTensor(float_values)
        attr_values = attr_values.repeat(62, 1)
        print(attr_values.shape)
    else:
        font_num -= 148
        font_embed = torch.LongTensor([font_num])
        font_embed = font_embed.repeat(62, 1)
        attr_values = attr_unsuper_tolearn(font_embed).to(device)
        print(attr_values.shape)
        attr_values = attr_values.view(attr_values.size(0), attr_values.size(2))  # noqa
        attr_values = torch.sigmoid(3*attr_values)  # convert to [0, 1]
        print(attr_values.shape)
    print(attr_values)
    return attr_values