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

def remove_from_cloud():
    selected_file_index = selected_file.curseselection()
    if selected_file_index:
        data.pop(selected_file_index[0])
        update_data()

upload = Image.open("upload.png")
uploadPhoto = ImageTk.PhotoImage(upload)

download = Image.open("download.png")
downloadPhoto = ImageTk.PhotoImage(download)

delete = Image.open("delete.png")
deletePhoto = ImageTk.PhotoImage(delete)

upload_Button=Button(f, image=uploadPhoto, command=add_file, bg="dark violet", relief=FLAT,activebackground="dark violet")
upload_Button.place(x=5, y=10)

download_Button = Button(f, image=downloadPhoto, bg="dark violet", relief=FLAT,activebackground="dark violet")
download_Button.place(x=90, y=10)

delete_Button=Button(f, image=deletePhoto, command=remove_from_cloud, bg="dark violet", relief=FLAT,activebackground="dark violet")
delete_Button.place(x=175, y=10)

f.mainloop()