from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk

f=Tk()
f.title("Füße")
f.geometry("800x600")
f. resizable(width=False, height=False)
f.configure(bg="dark violet")

folder = Image.open("folder.png")
folderPhoto = ImageTk.PhotoImage(folder)

folder_Button=Button(f, image=folderPhoto, bg="dark violet", relief=FLAT)
folder_Button.place(x=400, y=300)
f.mainloop()