#photo_batch_resizing

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