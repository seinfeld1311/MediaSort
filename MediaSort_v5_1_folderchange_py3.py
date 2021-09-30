# -*- coding: utf-8 -*-
__author__ = "Eric Fries"
__copyright__ = "Copyright 2018, Eric Fries"
__license__ = "GPL"
__version__ = "5.2"
__maintainer__ = "Eric Fries"
__email__ = "ich@ericfries.de"
__status__ = "Production"
__last_edited__ = "2019-03-10"

"""
The Script can be used to sort media Files (jpg/raw/mp4...) in a base folder
named after the file extension (picture/movie extension " jpg " )
with sub folders named after the exif Date/Created date of the corresponding media files.
For example: 
jpeg (base folder)
    - 2018-03-18 (sub folder)
mp4 (base fold)
    - 2018-03-18 (sub folder)
    

To use the script for other media files you must expand one of the dicts in the config_dict.py with the file extensions 
you need.


    
    BEWARE:
    https://pypi.python.org/pypi/ExifRead
    Exifread had to be changed in order to read the Lumix GX80 RW2 files 
    -> https://github.com/pypa/pypi-legacy/issues/734

TODO: log File and self created pictures without Exif creates Error "ExifError" -> must be fixed
TODO: Create FolderDepths/foldernames to choose from or better shortcut the elements in an dictonary and create the 
        possibility to make your own kind of folder (i.a. yy/mm or dd/yy) and so on.
        
Changelog v5.2:
    exif_time_sep -> Exif Time Seperator to find out which seperator is used in the Exif time (/ or -)
    and
    Endungen_problem dict in connection with a key Error for jpgs without Exif Information aka. S9 Collage to get sorted
Changelog v4 2019/03/07:
    No input at the point of folder creation returns standard folder y-m-d -> so, for the most times there is no input 
    necessary 
Changelog v4 2018/12/14:
    It is now possible to limit the folder depth from Year-Month-day to Year-Month
changelog v5 2021/09/30:
    This is a try to get the MediaSort programm in Python 3 Format
    TODO: it is not FINISHED !!!!

"""

import config_dict
import exifread
import os
import shutil
import sys
import time


# The *.lower() method, is used to ignore any casessnsitivity issues with the file extension. Another benefit is that
# the Dict (endungen) can be much shorter.
def sort(endungen_exif, endungen_created, in_folder, folder_create, endungen_problem):
    os.chdir(in_folder)
    direc = os.getcwd()
    delliste = []
    with open("log.txt", "w") as logfile:
        for i in filter(os.path.isfile, os.listdir(direc)):  # Searches for media files in folder
            try:
                imagepath = os.path.join(in_folder, i)  # create the path to the picture/media file
                endung = i.split(".")[1]  # get rid of the file extension
                if endung.lower() in endungen_exif:  # The if in part is looking for correspodent file extensions in
                    # folder and dictionary.
                    shtime = str(readexifdate(imagepath, folder_create))  # reading the EXIF date
                    print "shtime ", shtime
                    pfad = os.path.join("/", endungen_exif[endung.lower()], shtime)
                    print "pfad ", pfad
                    if not os.path.exists(pfad):
                        #os.makedirs(pfad)
                        os.system(sudo makedirs(pfad))
                    shutil.move(imagepath, pfad)
                elif endung.lower() in endungen_created:
                    shtime = mp4_date(i, folder_create)  # mp4 Created Date
                    pfad = os.path.join("/", endungen_created[endung.lower()], shtime)
                    print "pfad2 ", pfad
                    if not os.path.exists(pfad):
                        #os.makedirs(pfad)
                        os.system(sudo makedirs(pfad))
                    shutil.move(imagepath, pfad)
                else:
                    pass
                    print "passed"
            except shutil.Error:
                logfile.writelines("Datei {} existiert bereits\n".format(i))
                delliste.append(i)
                print "Datei {} existiert bereits".format(i)
                pass
            except RuntimeError:
                print sys.exc_info()
                logfile.writelines("\nRuntime Error: {0} - "
                                   "{1} bei Datei: {2}\n".format(sys.exc_info()[0], sys.exc_info()[1], i))
                print "Fehler: {} - {} \nbei Datei: {}".format(sys.exc_info()[0], sys.exc_info()[1], i)
            except KeyError:
                logfile.writelines("\nKeyError: {0} - "
                                   "{1} bei Datei: {2}\n".format(sys.exc_info()[0], sys.exc_info()[1], i))
                shtime = mp4_date(i, folder_create)  # mp4 Created Date
                pfad = os.path.join(in_folder, endungen_problem[endung.lower()], shtime)
                # pfad = os.path.join("./", endungen_problem[endung.lower()], shtime)
                print "pfad2 ", pfad
                print "pfad1 ", imagepath
                if not os.path.exists(pfad):
                    os.makedirs(pfad)
                try:
                    shutil.move(imagepath, pfad)
                except shutil.Error:
                    print "\nShutil.Error: {0} - {1} bei Datei: {2}\n".format(sys.exc_info()[0], sys.exc_info()[1], i)
                    logfile.writelines("\nShutil.Error: {0} - "
                                       "{1} bei Datei: {2}\n".format(sys.exc_info()[0], sys.exc_info()[1], i))
                    pass
    del_log("log.txt")
    # This part let the user decide if the unnecessary / second copies of the files can be erased or not
    if len(delliste) > 0:
        delfiles = raw_input("Sollen die doppelten Dateien geloescht werden (J/N) ?: ")
        if delfiles.lower() == "j":
            del_existingfiles(delliste)
    else:
        pass


# --------- Hier muss gebastelt werden

def readexifdate(imagepath, f_c):  # Function for getting the Exifdate from the pictures an create the folders
    f = open(imagepath, 'rb')
    tags = exifread.process_file(f)
    exif_time = str(tags["EXIF DateTimeDigitized"]).split(" ")[
        0]  # TODO To get the single parts of the Date, split it and name the parts an yy/mm/dd
    print "exif_time ", exif_time
    ymd = ("y", "m", "d")
    print ymd
    exif_time_sep = exif_time[-3]  # To find out which seperator is used in the Exif Time
    exif_split = exif_time.split(exif_time_sep)
    print exif_split
    fc_dict = dict()
    shoot_time = []
    print shoot_time
    for j, i in zip(ymd, exif_split):
        print j, i
        fc_dict[j] = i
    for i in f_c:
        print i
        if i in fc_dict:
            shoot_time.append(fc_dict[i])
        else:
            shoot_time.append(i)
    # return "".join(shoot_time) # das hier weg dafür das drunter hin ... !!
    return foldercreation(exif_split, f_c)  # -> statt return "".join(shoot_time) -> Das Gleiche in mp4_date


# exif_split as input has to be the splited time with y,m,d. It has to be in this particular order f.i. an as tuple
# an with zeros if there is only one digit
def foldercreation(exif_split, f_c):
    ymd = ("y", "m", "d")
    fc_dict = dict()
    shoot_time = []
    for j, i in zip(ymd, exif_split):
        print j, i
        fc_dict[j] = i
    for i in f_c:
        print i
        if i in fc_dict:
            shoot_time.append(fc_dict[i])
        else:
            shoot_time.append(i)
    return "".join(shoot_time)

    # Function for getting the creation Date from the video files (with this funct it is possible to
    # get the creation date of a random file, not only media).


# -> exifread gives back a string -> yyyy:mm:dd
# timedict =

def mp4_date(mp4, f_c):
    ctd = time.localtime(os.path.getmtime(mp4))
    year = str(ctd.tm_year)
    mon = str(ctd.tm_mon)
    day = str(ctd.tm_mday)
    if len(mon) < 2:  # to create a folder with a zero in front of a day which has only one number (i.a. 4 -> 04)
        mon = "0" + mon
    if len(day) < 2:
        day = "0" + day
    exif_split = (year, mon, day)
    return foldercreation(exif_split, f_c)
    # ordnername = year + "-" + mon + "-" + day  # Formatting the creation date


# TODO Retun folder as shoot:time from foldercreation to other
def del_log(logfile):  # This Function erases the logfile if it's empty
    if (os.stat(logfile).st_size == 0) is True:
        os.remove(logfile)


def del_existingfiles(delliste):
    for i in delliste:
        os.remove(i)


if __name__ == "__main__":
    # -> Media with readable exif files (raw/ Pictures) File extensions from the media files in front as key and
    # the folder to be created as value

    # -> Media without readable Exif Files / File extensions from the media files in front as key and the folder
    # to be created as value

    photo_folder = raw_input("Media folder: ")
    # folder_depth = input("Choose:\n\n"
    #                          "1 - Folder -> yyyy-mm-dd\n"
    #                          "2 - Folder -> yyyy-mm : ")
    foldertocreate = raw_input("Choose y=year, m=month, d=day with a seperator (_ : or more) f.i. y_m_d will create "
                               "(.../2018_12_30/...) \nbut / as a seperator is used to create a folder in a main folder"
                               "f.i."
                               "\na folder in the year_month folder ->  y_m/d will create ( .../2018_12/27/... )"
                               "\nleave input empty for creating standard folder y-m-d :")
    foldertocreate = foldertocreate if len(foldertocreate) > 0 else "y-m-d"
    print foldertocreate
    sort(config_dict.endungen_exif, config_dict.endungen_created, photo_folder, foldertocreate,
         config_dict.endungen_problem)

    # BEWARE:
    # https://pypi.python.org/pypi/ExifRead
    # Exifread had to be changed in order to read the Lumix GX80 RW2 files
    # -> https://github.com/pypa/pypi-legacy/issues/734
# TODO: Anzahl der geloeschten und Uebertragenen Dateien am Ende anzeigen
