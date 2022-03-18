# -*- coding: utf-8 -*-
__author__ = "Eric Fries"
__copyright__ = "Copyright 2018, Eric Fries"
__license__ = "GPL"
__version__ = "1.0"
__maintainer__ = "Eric Fries"
__email__ = "ich@ericfries.de"
__status__ = "Production"


"""
This is the config file for the PictSort script.
endungen_exif -> Exif readable media files (Exifread)
endungen_cfreated -> Not Exif readble media files. It reades the created date from the file
-> key:value == file:folder
update 30_10_2021:
    -> there some problems with the file endings, so I had to add some "normal" endings to the dictionaries
"""

endungen_exif = {
    "jpeg": "jpeg",
    "jpg": "jpeg",
    "rw2": "raw",
}  # -> Media with readable exif files (raw/ Pictures) File extensions from the media files in front as key and the folder to be crated as value

endungen_created = {
    "mp4": "mov",
    "mov": "mov",
}  # -> Media without readable Exif Files / File extensions from the media files in front as key and the folder to be crated as value

endungen_problem = {
    "gif": "gif",
    "mp4": "mov", # this (mp4 and jpg) don't belong here, but there seems to be problems with mp4 and jpg in
    "gif": "gif",
    "jpg": "jpeg" # connection with camera and mobilphoen -> not with every but with a couple. I dont know why but this helbs
}