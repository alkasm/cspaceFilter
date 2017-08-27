import argparse  # command line inputs
import cspaceFilter  # running the algo
import cv2  # for checking the image
import json  # for i/o


__author__ = "Alexander Reynolds"
__email__ = "ar@reynoldsalexander.com"


"""Private validator functions"""


def _sanitize(filename):

    sanitized = "".join(
        [c for c in filename
         if c.isalpha() or c.isdigit() or c in ['.', '_', '-', '/']]).rstrip()

    return sanitized


def _checkimg(imgPath):

    img = cv2.imread(imgPath)

    if img is None:
        invalidmsg = ("%s is an invalid image filename, "
                      "did not load image." % imgPath)
        raise argparse.ArgumentTypeError(invalidmsg)

    return img


def _checkcspace(cspaceLabel):

    validLabels = ['BGR', 'HSV', 'HLS', 'Lab',
                   'Luv', 'YCrCb', 'XYZ', 'Grayscale']

    if cspaceLabel not in validLabels:

        invalidmsg = ("{0} is an invalid colorspace, must be one of: "
                      "{1}, {2}, {3}, {4}, {5}, {6}, {7}, or {8}."
                      ).format(cspaceLabel, *validLabels)

        raise argparse.ArgumentTypeError(invalidmsg)


"""Command line parsing"""


if __name__ == "__main__":
    """To be ran from command line

    Usage example:
        python3 cspaceIO.py '{
            "paths":
            {
                "srcPath":"input/test.png",
                "maskPath":"output/test.png",
                "maskedPath":"output/test2.png"
            },
            "cspaceLabel":"BGR",
            "sliderPos":[127,255,127,255,127,255]
        }'
    """

    parser = argparse.ArgumentParser(
        description='Color threshold an image in any colorspace \
                     and save it to a file.')

    parser.add_argument('jsonIn', help='JSON containing paths \
        (dict {imgPath (str), maskPath (str), maskedPath (str)}), \
        cspaceLabel (str), and sliderPos (6-long int list[])')

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
    _checkcspace(cspaceLabel)
    srcPath = _sanitize(srcPath)
    maskPath = _sanitize(maskPath)
    maskedPath = _sanitize(maskedPath)
    img = _checkimg(srcPath)

    # run the colorspace filter script
    mask, masked_img = cspaceFilter.main(img, cspaceLabel, sliderPos)

    # write the output image
    cv2.imwrite(maskPath, mask)
    cv2.imwrite(maskedPath, masked_img)
