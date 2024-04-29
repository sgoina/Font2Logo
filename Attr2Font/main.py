import datetime
import os
import time

import torch
from torch import nn
from torchvision.utils import save_image

from dataloader import get_loader
from model import CXLoss, DiscriminatorWithClassifier, GeneratorStyle
from options import get_parser
from vgg_cx import VGG19_CX

from dotenv import load_dotenv
load_dotenv()
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


def test_one_epoch(opts, test_logfile, test_epoch,
                   checkpoint_dir, results_dir,
                   generator, attribute_embed,
                   attr_unsuper_tolearn, test_dataloader,
                   criterion_pixel):
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
        test_l1_loss = torch.zeros(1).to(device)

        for test_idx, test_batch in enumerate(test_dataloader):
            test_img_A = test_batch['img_A'].to(device)
            test_fontembed_A = test_batch['fontembed_A'].to(device)
            test_styles_A = test_batch['styles_A'].to(device)

            test_img_B = test_batch['img_B'].to(device)

            test_attr_A_intensity = attr_unsuper_tolearn(test_fontembed_A)
            test_attr_A_intensity = test_attr_A_intensity.view(test_attr_A_intensity.size(0), test_attr_A_intensity.size(2))  # noqa
            test_attr_A_intensity = torch.sigmoid(
                3*test_attr_A_intensity)  # convert to [0, 1]

            test_attr_B_intensity = test_batch['attr_B'].to(device)

            test_attr_raw_A = attribute_embed(test_attrid)
            test_attr_raw_B = attribute_embed(test_attrid)

            test_intensity_A_u = test_attr_A_intensity.unsqueeze(-1)
            test_intensity_B_u = test_attr_B_intensity.unsqueeze(-1)

            test_attr_A = test_intensity_A_u * test_attr_raw_A
            test_attr_B = test_intensity_B_u * test_attr_raw_B

            test_intensity = test_attr_B_intensity - test_attr_A_intensity
            test_attr = test_attr_B - test_attr_A

            test_fake_B, _ = generator(
                test_img_A, test_styles_A, test_intensity, test_attr)
            test_l1_loss += criterion_pixel(test_fake_B, test_img_B)

            i = 0
            for character in test_fake_B:
                save_file = os.path.join(results_dir, f"{str(i).zfill(2)}.png")
                second_save_file = os.path.join(
                    "../Logo_Generator/text_image", f"{str(i).zfill(2)}.png")
                save_image(255-character, save_file, nrow=1, normalize=True)
                i += 1
                save_image(255-character, second_save_file,
                           nrow=1, normalize=True)
            img_sample = torch.cat((test_img_A.data, test_fake_B.data, test_img_B.data), -2)
            save_file = os.path.join(results_dir, f"all_characters.png")
            save_image(img_sample, save_file, nrow=62, normalize=True)

        test_l1_loss = test_l1_loss / len(test_dataloader)
        test_msg = (
            f"Epoch: {test_epoch}/{opts.n_epochs}, "
            f"L1: {test_l1_loss.item(): .6f}"
        )
        print(test_msg)
        test_logfile.write(test_msg + "\n")
        test_logfile.flush()


def test(opts):
    # Dirs
    log_dir = os.path.join("experiments", opts.experiment_name)
    checkpoint_dir = os.path.join(log_dir, "checkpoint")
    results_dir = os.path.join(log_dir, "results")

    # Path to data
    image_dir = os.path.join(opts.data_root, opts.dataset_name, "image")
    attribute_path = os.path.join(
        opts.data_root, opts.dataset_name, "attributes2.txt")

    test_dataloader = get_loader(image_dir, attribute_path,
                                 dataset_name=opts.dataset_name,
                                 image_size=opts.img_size,
                                 n_style=opts.n_style, batch_size=62,
                                 mode='test', binary=False)

    # Model
    criterion_pixel = torch.nn.L1Loss().to(device)
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

    test_logfile = open(os.path.join(
        log_dir, f"test_loss_log_{opts.test_epoch}.txt"), 'w')

    if opts.test_epoch == 0:
        for test_epoch in range(opts.check_freq, opts.n_epochs+1, opts.check_freq):
            test_one_epoch(opts, test_logfile, test_epoch,
                           checkpoint_dir, results_dir,
                           generator, attribute_embed, attr_unsuper_tolearn,
                           test_dataloader, criterion_pixel)
    else:
        test_one_epoch(opts, test_logfile, opts.test_epoch,
                       checkpoint_dir, results_dir,
                       generator, attribute_embed, attr_unsuper_tolearn,
                       test_dataloader, criterion_pixel)


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
