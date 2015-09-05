#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
photo_batch_resizing

Warning: It would modify the file itself, so plese backup first!

Author: Tang Xiaofei
Function: Batch resize photos, and also preserve original exif info.
Only for Python 3

照片缩放批处理

警告：会直接修改原文件本身，所以需要手动备份一下！

目的：数码相机拍摄的照片尺寸过大，存贮起来很不方便，所以缩小一下尺寸方便保存。
     用其他软件处理时会往往会丢失exif信息（相机拍摄时间等文件属性信息），本程序
     仅缩小图像尺寸，仍然保留exif信息。
前提：安装pillow和piexif库，仅支持python 3
功能：批处理缩放照片，同时保留原exif信息，希望保留照相机拍摄的时间和一些参数

'''

import sys
import os
import os.path
from PIL import Image
import piexif

class PhotoResizingError(Exception):
    '''
    PhotoResizingError
    '''
    pass

file_total = 0
jpgfile_total = 0
jpgfile_resize_total = 0

def __resize_single_photo(jpgfilepath, maxsize):
    '''
    resize single photo
    '''

    global file_total
    global jpgfile_total
    global jpgfile_resize_total

    _, ext = os.path.splitext(jpgfilepath)
    ext = ext.lower()
    hasResize = False

    file_total += 1

    if ext == ".jpg" or ext == ".jpeg":
        jpgfile_total += 1
        im = Image.open(jpgfilepath)
        w, h = im.size
        m = max(w, h)
        if m > maxsize:
            ratio = maxsize / m
            w, h = int(w*ratio), int(h*ratio)
            #im.thumbnail((w, h))
            im = im.resize((w, h), Image.LANCZOS);

            exif_dict = piexif.load(im.info["exif"])
            exif_bytes = piexif.dump(exif_dict)
            im.save(jpgfilepath, 'jpeg', exif=exif_bytes)
            #im.save(jpgfilePath, 'jpeg')
            #piexif.transplant(jpgfilePath, jpgfilePath)

            jpgfile_resize_total += 1


def batch_resize_photos(photoDirOrFilePath, maxsize=1920):
    '''
    Warning: It would modify the file itself, so plese backup first!

    Function: Batch resize photos, and also preserve original exif info.
    Author: Tang Xiaofei
    '''
    if not os.path.exists(photoDirOrFilePath):
        raise PhotoResizingError("photoDir does not exis!")

    global file_total
    global jpgfile_total
    global jpgfile_resize_total

    file_total = 0
    jpgfile_total = 0
    jpgfile_resize_total = 0

    print("batch_resize_photos start...")
    print("photoDirOrFilePath:", photoDirOrFilePath)

    photoDirOrFilePath = os.path.abspath(photoDirOrFilePath)
    print("photoDirOrFilePath: ", photoDirOrFilePath)

    photo_dir = None
    photo_filePath = None
    if os.path.isdir(photoDirOrFilePath):
        photo_dir = photoDirOrFilePath
    else:
        photo_filePath = photoDirOrFilePath

    if photo_filePath:
        __resize_single_photo(photo_filePath, maxsize)

    if photo_dir:
        for parent, dirnames, filenames in os.walk(photo_dir):
            #case 1:
            #for dirname in dirnames:
            #    print("parent folder is:" + parent)
            #    print("dirname is:" + dirname)
            #case 2
            for filename in filenames:
                filepath = os.path.join(parent, filename)
                __resize_single_photo(filepath, maxsize)

    print("batch_resize_photos end.")


if __name__ == '__main__':
    if len(sys.argv) == 2:
        batch_resize_photos(sys.argv[1])
    elif len(sys.argv) == 3:
        ms = int(sys.argv[2])
        if ms > 0:
            batch_resize_photos(sys.argv[1], ms)
        else:
            print("Arguments got error!")
    else:
        print("Invalid arguments!")
