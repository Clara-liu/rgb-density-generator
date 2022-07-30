import sys
import cv2
import argparse
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from os import path


def _get_rgb_df(img_path):
    """generate pixel value pandas data for plotting

    :param img_path: path to the image
    :type img_path: str
    :return: data of RGB pixel values from the image
    :rtype: pandas data frame
    """
    img = cv2.imread(img_path)
    blue = img[0, :, :].flatten()
    green = img[1, :, :].flatten()
    red = img[2, :, :].flatten()
    df = pd.DataFrame(np.concatenate([red, green, blue]), columns=['value'])
    df['channel'] = pd.Series(['r', 'g', 'b']).repeat(blue.shape).reset_index(drop=True)
    return df


def _plot(df, save_path, bw):
    """generates and save the rgb density plot

    :param df: rgb df
    :type df: pandas data frame
    :param save_path: path to save the figure
    :type save_path: str
    """
    my_pal = {'r': 'crimson', 'g': 'mediumseagreen', 'b': 'royalblue'}
    sns.displot(df, x='value', hue='channel', kind="kde", bw_adjust = bw, fill=True, palette=my_pal, alpha=0.35, legend=False, height=4.5, aspect=1.25)
    plt.axis('off')
    plt.tight_layout()
    plt.savefig(save_path, transparent=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--img-path', type=str, required=True, help='path to the image you want to use')
    parser.add_argument('--out-path', type=str, required=True, help='path to save the figure')
    parser.add_argument('--band-width', type=float, default=0.25, help='factor to adjust density band width')
    args = parser.parse_args()

    if path.exists(path.dirname(args.out_path)) and path.isfile(args.img_path):
        rgb_df = _get_rgb_df(args.img_path)
        _plot(rgb_df, args.out_path, args.band_width)
    else:
        sys.exit('Image file does not exist or out path is invalid.')
