import cv2
import numpy as np


__author__ = "Alexander Reynolds"
__email__ = "ar@reynoldsalexander.com"


"""Private helper functions"""


def _cspaceSwitch(img, cspaceLabel):
    """Coverts the colorspace of img from BGR to cspaceLabel

    Keyword arguments:
        img -- the image to convert
        cspaceLabel -- the colorspace to convert to

    Returns:
        img -- img with the converted colorspace
    """
    if cspaceLabel == 'BGR':
        return img

    convert_code = {
        'HSV': cv2.COLOR_BGR2HSV,
        'HLS': cv2.COLOR_BGR2HLS,
        'Lab': cv2.COLOR_BGR2Lab,
        'Luv': cv2.COLOR_BGR2Luv,
        'YCrCb': cv2.COLOR_BGR2YCrCb,
        'XYZ': cv2.COLOR_BGR2XYZ,
        'Grayscale': cv2.COLOR_BGR2GRAY}

    img = cv2.cvtColor(img, convert_code[cspaceLabel])

    return img


def _cspaceBounds(cspaceLabel, slider_pos):
    """Calculates the lower and upper bounds for thresholding a
    colorspace based on the thresholding slider positions.

    Keyword arguments:
        cspaceLabel -- the colorspace to find bounds of; see keys in main()
        slider_pos -- positions of the thresholding trackbars; length 6 list

    Returns:
        lowerb -- list containing the lower bounds for each channel threshold
        upperb -- list containing the upper bounds for each channel threshold
    """

    if cspaceLabel is 'Grayscale':
        lowerb, upperb = slider_pos[0], slider_pos[1]
    else:
        lowerb = np.array([slider_pos[0], slider_pos[2], slider_pos[4]])
        upperb = np.array([slider_pos[1], slider_pos[3], slider_pos[5]])

    return lowerb, upperb


def _cspaceRange(img, cspaceLabel, lowerb, upperb):
    """Thresholds img in cspaceLabel with lowerb and upperb

    Keyword arguments:
        img -- the image to be thresholded
        cspaceLabel -- the colorspace to threshold in

    Returns:
        mask -- a binary image that has been thresholded
    """
    img = _cspaceSwitch(img, cspaceLabel)
    mask = cv2.inRange(img, lowerb, upperb)

    return mask


def _applyMask(img, mask):
    """Applies a mask to an image

    Keyword arguments:
        img -- the image to be masked
        mask -- the mask (non-zero values are included, zero values excluded)

    Returns:
        masked_img -- the input img with mask applied
    """

    masked_img = cv2.bitwise_and(img, img, mask=mask)

    return masked_img


"""Main public function"""


def main(img, cspaceLabel, slider_pos):
    """Computes the colorspace thresholded image based on
    slider positions and selected colorspace.

    Inputs:
        img -- input image
        cspaceLabel -- colorspace to filter the image in
        slider_pos -- positions of the six sliders (6-long int list)

    returns
        mask -- mask created from thresholding the image
        masked_img -- masked image
    """
    lowerb, upperb = _cspaceBounds(cspaceLabel, slider_pos)
    mask = _cspaceRange(img, cspaceLabel, lowerb, upperb)
    masked_img = _applyMask(img, mask)

    return mask, masked_img
