
# coding: utf-8

# In[63]:

# pydicom_PIL.py
"""View DICOM images using Python image Library (PIL)

Usage:
>>> import dicom
>>> from dicom.contrib.pydicom_PIL import show_PIL
>>> ds = dicom.read_file("filename")
>>> show_PIL(ds)

Requires Numpy:  http://numpy.scipy.org/
and Python Imaging Library:   http://www.pythonware.com/products/pil/

"""
# Copyright (c) 2009 Darcy Mason, Adit Panchal
# This file is part of pydicom, relased under an MIT license.
#    See the file license.txt included with this distribution, also
#    available at http://pydicom.googlecode.com

# Based on image.py from pydicom version 0.9.3,
#    LUT code added by Adit Panchal
# Tested on Python 2.5.4 (32-bit) on Mac OS X 10.6
#    using numpy 1.3.0 and PIL 1.1.7b1
# RescaleSlope and RescaleIntercept added by ejoonie

have_PIL = True
try:
    import PIL.Image
except:
    have_PIL = False

have_numpy = True
try:
    import numpy as np
except:
    have_numpy = False


def get_LUT_value(data, window, level, rescale_slope, rescale_intercept):
    """Apply the RGB Look-Up Table for the given data and window/level value."""
    if not have_numpy:
        raise ImportError("Numpy is not available. See http://numpy.scipy.org/ to download and install")


    # rescale slope and rescale intercept
    data = np.piecewise(data, [data == data], [lambda data: data * rescale_slope + rescale_intercept])
    
    # lut
    ret = np.piecewise(data,
                        [data <= (level - 0.5 - (window - 1) / 2),
                         data > (level - 0.5 + (window - 1) / 2)],
                        [0, 255, lambda data: ((data - (level - 0.5)) / (window - 1) + 0.5) * (255 - 0)])

    return ret


# Display an image using the Python Imaging Library (PIL)
def show_PIL(dataset):
    if not have_PIL:
        raise ImportError("Python Imaging Library is not available. See http://www.pythonware.com/products/pil/ to download and install")
    if ('PixelData' not in dataset):
        raise TypeError("Cannot show image -- DICOM dataset does not have pixel data")
    if ('WindowWidth' not in dataset) or ('WindowCenter' not in dataset):  # can only apply LUT if these values exist
        bits = dataset.BitsAllocated
        samples = dataset.SamplesPerPixel
        if bits == 8 and samples == 1:
            mode = "L"
        elif bits == 8 and samples == 3:
            mode = "RGB"
        elif bits == 16:
            mode = "I;16"  # not sure about this -- PIL source says is 'experimental' and no documentation. Also, should bytes swap depending on endian of file and system??
        else:
            raise TypeError("Don't know PIL mode for %d BitsAllocated and %d SamplesPerPixel" % (bits, samples))

        # PIL size = (width, height)
        size = (dataset.Columns, dataset.Rows)

        im = PIL.Image.frombuffer(mode, size, dataset.PixelData, "raw", mode, 0, 1)  # Recommended to specify all details by http://www.pythonware.com/library/pil/handbook/image.htm

    else:
        image = get_LUT_value(dataset.pixel_array, dataset.WindowWidth, dataset.WindowCenter, dataset.RescaleSlope, dataset.RescaleIntercept)
        im = PIL.Image.fromarray(image).convert('L')  # Convert mode to L since LUT has only 256 values: http://www.pythonware.com/library/pil/handbook/image.htm

    im.show()



# Put your own directory path to image_root_dir
# 
# It will iterate the dir and render all the dcm files

# In[64]:

import dicom
import os


#
# checking current dir
#
print(os.getcwd())


#
# study root dir
#
image_root_dir = '/Users/ejoonie/Downloads/1.3.6.1.4.1.14519.5.2.1.6279.6001.212697393127299815450339637649___a81a948096f99e069646bf749c80475f60fb1524/'
image_output_dir = os.path.join(image_root_dir, 'output')
dcm_files = []



for dirpath, dirnames, filenames in os.walk(image_root_dir):
    # checking study root dir
    print(dirpath)
    
    # merge filenames to dcm_files
    dcm_files.extend(filenames)

# iterate and extract bmp files    
for dcm_file in dcm_files:
    print(dcm_file)
    ds = dicom.read_file(os.path.join(image_root_dir, dcm_file))
    print(int(ds.InstanceNumber))
    print('level: {0} window: {1}'.format(ds.WindowCenter, ds.WindowWidth))
    print('rescale slope: {0} rescale intercept: {1}'.format(ds.RescaleSlope, ds.RescaleIntercept))
    
    show_PIL(ds)

    


# TODO
# ---
# - order by InstanceNumber
# - 3d render
# - extract jpeg
# 
# 
# ### IDEA
# - determine xray(ct) image or not -> guess modality
# - categorize coronal, axial, sagital
# - matching location (similar image with the highest possibility)
# - report auto generation
# - ocr in ultrasound and erase
# - stethoscope sound
# 
# ### QUESTION
# - what is feature

# In[ ]:




# In[ ]:



