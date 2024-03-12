# Import necessary modules
from PIL import Image as PIL_Image
import os
import sys
import glob

import threading
import concurrent.futures

from tkinter import filedialog
from tkinter import *

# Define where the images are saved
#imgDir = 'C:\\Users\\ichR PC-2022\\Desktop\\Tool for Gabe'

""" Global Variables """
SW_NAME = '3D Files Batch Processing Tool'
SW_VER  = 'v0.1'

FLAG_DeleteToggle = False

""" GUI Function Definitions (Commands) """
def toggleDelete():
    global FLAG_DeleteToggle

    if CHKBTN_DeleteToggle_status.get() == 1:
        FLAG_DeleteToggle = True
    else:
        FLAG_DeleteToggle = False

def open_directories():
    # Allow user to select a directory and store it in global var
    # called folder_path
    directory_path = filedialog.askdirectory()
    #path_label['text'] = directory_path
    os.chdir(directory_path)
    #print(os.getcwd())
    current_directory_lbl['text'] = "Current Directory: " + directory_path

def resize_and_convert_to_webp(source_path):
    resample_technique = None

    with PIL_Image.open(source_path) as img:
        fileName, fileExtension = os.path.splitext(source_path)
        img = img.resize((1024, 1024), resample=resample_technique)
        out_path = fileName + ".webp"
        img.save(out_path)
        # Remove original files (.jpg and .png)
        if FLAG_DeleteToggle:
            os.remove(source_path)

def process_files():
    # Find the 3D Object File
    threeD_object_file = glob.glob("*.gltf")

    # Replace all references containing '.jpg', '.jpeg' and '.png' in the 3D object file
    with open(threeD_object_file[0], 'r') as file:
        filedata = file.read()

    filedata = filedata.replace('jpg', 'webp')
    filedata = filedata.replace('jpeg', 'webp')
    filedata = filedata.replace('png', 'webp')

    with open(threeD_object_file[0], 'w') as file:
        file.write(filedata)

    # Find and remove all existing .webps
    all_images = glob.glob("**/*.webp", recursive=True)


    # Find all images that are .png and .jpg
    all_images = glob.glob("**/*.png", recursive=True) + glob.glob("**/*.jpg", recursive=True)

    '''
    # Multithreaded solution using threading.Thread()
    for image in all_images:
        thread = threading.Thread(target=resize_and_convert_to_webp)
    '''
    
    # Downsize all images to 1024 x 1024 and save as .webp

    with concurrent.futures.ThreadPoolExecutor() as threads:
        futures = [threads.submit(resize_and_convert_to_webp, image) for image in all_images]

        for future in futures:
            future.result()

    '''
    futures = []

    with concurrent.futures.ThreadPoolExecutor() as threads:
        for image in all_images:
            futures.append(threads.submit(resize_and_convert_to_webp, image))   

        for future in futures:
            future.result()
    '''

""" GUI Elements"""

root = Tk()
root.title(SW_NAME + " " + SW_VER)
root.bind_class("Button", "<Key-Return>", lambda event: event.widget.invoke())
root.bind_class("Checkbutton", "<Key-Return>", lambda event: event.widget.invoke())
root.geometry('400x100')

browse_files_btn = Button(master=root, text="Browse Directories", command=open_directories)
browse_files_btn.pack()

CHKBTN_DeleteToggle_status = IntVar()
delete_originals_chkbtn = Checkbutton(master=root, text="Delete Original Files", command=toggleDelete, variable=CHKBTN_DeleteToggle_status)
delete_originals_chkbtn.pack()

process_images_btn = Button(master=root, text="Process Images", command=process_files)
process_images_btn.pack()

current_directory_lbl = Label(master=root, text="Current Directory: No directory selected.")
current_directory_lbl.pack()

mainloop()