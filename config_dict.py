# -*- coding: utf-8 -*-
__author__ = "Eric Fries"
__copyright__ = "Copyright 2018, Eric Fries"
__license__ = "GPL"
__version__ = "2.0"
__maintainer__ = "Eric Fries"
__email__ = "ich@ericfries.de"
__status__ = "Production"


"""
This is the config file for the PictSort script.
endungen_exif -> Exif readable media files (Exifread)
endungen_cfreated -> Not Exif readble media files. It reades the created date from the file
-> key:value == file:folder

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
}