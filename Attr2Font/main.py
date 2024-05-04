import datetime
import os
import time

import torch
from torch import nn
from torchvision.utils import save_image

from minidataloader import get_test_data, get_font_attr
from model import CXLoss, DiscriminatorWithClassifier, GeneratorStyle
from options import get_parser
from vgg_cx import VGG19_CX


device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


def test_one_epoch(opts, test_epoch, attribute_path,
                   image_dir, checkpoint_dir, results_dir,
                   generator, attribute_embed,
                   attr_unsuper_tolearn, new_attribute):
    print(f"Testing epoch: {test_epoch}")

    gen_file = os.path.join(checkpoint_dir, f"G_{test_epoch}.pth")
    attribute_embed_file = os.path.join(
        checkpoint_dir, f"attribute_embed_{test_epoch}.pth")
    attr_unsuper_file = os.path.join(
        checkpoint_dir, f"attr_unsuper_embed_{test_epoch}.pth")

    generator.load_state_dict(torch.load(gen_file))
    attribute_embed.load_state_dict(torch.load(attribute_embed_file))
    attr_unsuper_tolearn.load_state_dict(torch.load(attr_unsuper_file))

    with torch.no_grad():
        test_attrid = torch.tensor(
            [i for i in range(opts.attr_channel)]).to(device)
        test_attrid = test_attrid.repeat(62, 1)
        # test_l1_loss = torch.zeros(1).to(device)

        _,test_img, test_styles =  get_test_data(image_dir, attribute_path, opts.font_name, n_style= opts.n_style, image_size=opts.img_size)
        test_img = test_img.to(device)
        test_styles = test_styles.to(device)

        #來源字體的attribute
        test_attr_A_intensity = get_font_attr(attribute_path, opts.font_name, attr_unsuper_tolearn).to(device)

        test_attr_B_intensity = new_attribute.to(device)
        print(test_attr_B_intensity.shape)

        test_attr_raw_A = attribute_embed(test_attrid)
        test_attr_raw_B = attribute_embed(test_attrid)

        test_intensity_A_u = test_attr_A_intensity.unsqueeze(-1)
        test_intensity_B_u = test_attr_B_intensity.unsqueeze(-1)

        test_attr_A = test_intensity_A_u * test_attr_raw_A
        test_attr_B = test_intensity_B_u * test_attr_raw_B

        test_intensity = test_attr_B_intensity - test_attr_A_intensity
        test_attr = test_attr_B - test_attr_A

        test_fake_B, _ = generator(
            test_img, test_styles, test_intensity, test_attr)
        # test_l1_loss += criterion_pixel(test_fake_B, test_img_B)

        i = 0
        for character in test_fake_B:
            save_file = os.path.join(results_dir, f"{str(i).zfill(2)}.png")
            second_save_file = os.path.join(
                "../Logo_Generator/text_image", f"{str(i).zfill(2)}.png")
            save_image(255-character, save_file, nrow=1, normalize=True)
            i += 1
            save_image(255-character, second_save_file,
                        nrow=1, normalize=True)
        # img_sample = torch.cat((test_img_A.data, test_fake_B.data, test_img_B.data), -2)
        img_sample =  test_fake_B.data
        save_file = os.path.join(results_dir, f"all_characters.png")
        save_image(img_sample, save_file, nrow=62, normalize=True)

        # test_l1_loss = test_l1_loss / len(test_dataloader)
        # test_msg = (
        #     f"Epoch: {test_epoch}/{opts.n_epochs}, "
        #     f"L1: {test_l1_loss.item(): .6f}"
        # )
        # print(test_msg)
        # test_logfile.write(test_msg + "\n")
        # test_logfile.flush()


def test(opts):
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
            test_one_epoch(opts, test_epoch, attribute_path,
                           image_dir, checkpoint_dir, results_dir,
                           generator, attribute_embed, attr_unsuper_tolearn,
                           new_attribute)
    else:
        test_one_epoch(opts, opts.test_epoch, attribute_path,
                       image_dir, checkpoint_dir, results_dir,
                       generator, attribute_embed, attr_unsuper_tolearn,
                       new_attribute)


def main():
    parser = get_parser()
    opts = parser.parse_args()
    opts.unsuper_num = 968
    os.makedirs("experiments", exist_ok=True)
    if opts.phase == 'test':
        print(f"Testing on experiment {opts.experiment_name}...")
        test(opts)
    else:
        raise NotImplementedError


if __name__ == "__main__":
    main()