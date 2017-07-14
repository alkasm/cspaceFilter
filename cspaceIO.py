import argparse # command line inputs
import cspaceThreshImg # running the algo
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

    Usage example: 
    python3 cspaceIO.py '{"paths":{"srcPath":"input/test.jpg","maskPath":"output/test.png","maskedPath":"output/test2.png"},"cspaceLabel":"BGR","sliderPos":[50,100,50,100,50,100]}'
    """

    parser = argparse.ArgumentParser(description='Color threshold an image in any colorspace \
        and save it to a file.')

    parser.add_argument('jsonIn',
        help='JSON containing imgPath (str), maskPath (str), maskedPath (str), cspaceLabel (str), and sliderPos (6-long int list[])')

    args = parser.parse_args()

    # grab inputs from json
    jsonIn = json.loads(args.jsonIn)
    paths = jsonIn['paths']
    srcPath = paths['srcPath']
    maskPath = paths['maskPath']
    maskedPath = paths['maskedPath']
    cspaceLabel = jsonIn['cspaceLabel']
    sliderPos = jsonIn['sliderPos']

    # check inputs
    cspace = __checkcspace(cspaceLabel)
    srcPath = __sanitize(srcPath)
    maskPath = __sanitize(maskPath)
    maskedPath = __sanitize(maskedPath)
    img = __checkimg(srcPath)

    # run the colorspace thresh script
    mask, masked_img = cspaceThreshImg.main(
        img, cspace, sliderPos)

    # write the output image
    cv2.imwrite(maskPath, mask)
    cv2.imwrite(maskedPath, masked_img)
