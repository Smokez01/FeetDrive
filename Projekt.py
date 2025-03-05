from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk

f=Tk()
f.title("Füße")
f.geometry("200x400")
f. resizable(width=False, height=False)
f.configure(bg="dark violet")

upload = Image.open("upload.png")
uploadPhoto = ImageTk.PhotoImage(upload)

download = Image.open("download.png")
downloadPhoto = ImageTk.PhotoImage(download)

upload_Button=Button(f, image=uploadPhoto, bg="dark violet", relief=FLAT,activebackground="dark violet")
upload_Button.place(x=10, y=300)

download_Button = Button(f, image=downloadPhoto, bg="dark violet", relief=FLAT,activebackground="dark violet")
download_Button.place(x=150, y=300)

f.mainloop()