from tkinter import filedialog
from tkinter import *

def browse_button():
    # Allow user to select a directory and store it in global var
    # called folder_path
    global filename
    filename = filedialog.askdirectory()
    lbl1['text'] = filename


root = Tk()
folder_path = StringVar()
filename = 'Placeholder'
lbl1 = Label(master=root,text=filename)
lbl1.grid(row=0, column=1)
button2 = Button(text="Browse", command=browse_button)
button2.grid(row=0, column=3)

mainloop()