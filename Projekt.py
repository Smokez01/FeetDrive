from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk

Data = []

f=Tk()
f.title("FeetDrive")
f.geometry("250x100")
f. resizable(width=False, height=False)
f.configure(bg="dark violet")
f.iconbitmap("Feet.ico")

def add_file():
    file_path = filedialog.askopenfile(title="Datei auswählen")
    if file_path:
        Data.append(file_path)

upload = Image.open("upload.png")
uploadPhoto = ImageTk.PhotoImage(upload)

download = Image.open("download.png")
downloadPhoto = ImageTk.PhotoImage(download)

upload_Button=Button(f, image=uploadPhoto, command=add_file, bg="dark violet", relief=FLAT,activebackground="dark violet")
upload_Button.place(x=10, y=10)

download_Button = Button(f, image=downloadPhoto, bg="dark violet", relief=FLAT,activebackground="dark violet")
download_Button.place(x=180, y=10)

f.mainloop()