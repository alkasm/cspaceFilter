import argparse # command line inputs
import cspaceThresh2Img # running the algo
import cv2 # for checking the image
import json # for i/o
import os # for filewriting



__author__ = "Alexander Reynolds"
__email__ = "ar@reynoldsalexander.com"



"""Private validator functions"""



def __sanitize(filename):
    return "".join([c for c in filename
        if c.isalpha() or c.isdigit() or c in ['.', '_', '-', '/']]).rstrip()


def __checkimg(imgPath):
    img = cv2.imread(imgPath)
    if img is None:
         raise argparse.ArgumentTypeError("%s is an invalid image filename, did not load image." % imgPath)
    elif len(img.shape)==2:
        raise argparse.ArgumentTypeError("%s is an invalid image, must be a three-channel image." % imgPath)
    return img


def __checkcspace(cspaceLabel):
    validspaces = ['BGR', 'HSV', 'HLS', 'Lab', 'Luv', 'YCrCb', 'XYZ', 'Grayscale']
    if cspaceLabel not in validspaces:
         raise argparse.ArgumentTypeError("%s is an invalid colorspace, \
            must be one of: BGR, HSV, HLS, Lab, Luv, YCrCb, XYZ, or Grayscale." % cspace)
    cspace = {label:val for label,val in zip(validspaces,range(8))}[cspaceLabel]
    return cspace



"""Command line parsing"""



if __name__ == "__main__":
    """To be ran from command line

    Usage example: python3 cspace2IO.py '{"paths":{imgPath":"input/test.jpg","dstPath":"output/test.png","dstPath2":"output/test2.png"},"cspaceLabel":"BGR","sliderPos":[127,255,127,255,127,255]}'
    """

    parser = argparse.ArgumentParser(description='Color threshold an image in any colorspace \
        and save it to a file.')

    parser.add_argument('jsonIn',
        help='JSON containing imgPath (str), dstPath (str), dstPath2 (str), cspaceLabel (str), and sliderPos (6-long int list[])')

    args = parser.parse_args()

    # grab inputs from json
    jsonIn = json.loads(args.jsonIn)
    paths = jsonIn['paths']
    srcPath = paths['srcPath']
    dstPath = paths['dstPath']
    dstPath2 = paths['dstPath2']
    cspaceLabel = jsonIn['cspaceLabel']
    sliderPos = jsonIn['sliderPos']

    # check inputs
    cspace = __checkcspace(cspaceLabel)
    srcPath = __sanitize(srcPath)
    dstPath = __sanitize(dstPath)
    dstPath2 = __sanitize(dstPath2)
    img = __checkimg(srcPath)

    # run the colorspace thresh script
    mask, masked_img = cspaceThresh2Img.main(
        img, cspace, sliderPos)

    # write the output image
    cv2.imwrite(dstPath, mask)
    cv2.imwrite(dstPath2, masked_img)
