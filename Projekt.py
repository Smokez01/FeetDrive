from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk
import webbrowser
import os

Data = []

f=Tk()
f.title("FeetDrive")
f.geometry("250x100")
f. resizable(width=False, height=False)
f.configure(bg="dark violet")
f.iconbitmap("images/Feet.ico")

def open_html():
    html_file = "Cloud.html"
    file_path= os.path.abspath(html_file)
    webbrowser.open("C:\github\Projekt\Cloud.html")

def add_file():
    
    file_path = filedialog.askopenfile(title="Datei auswählen")
    if file_path:
        Data.append(file_path)

def remove_from_cloud():
    selected_file_index = selected_file.curseselection()
    if selected_file_index:
        data.pop(selected_file_index[0])
        update_data()

upload = Image.open("images/upload.png")
uploadPhoto = ImageTk.PhotoImage(upload)

download = Image.open("images/download.png")
downloadPhoto = ImageTk.PhotoImage(download)

delete = Image.open("images/delete.png")
deletePhoto = ImageTk.PhotoImage(delete)

Open = Image.open("image/open .png")
OpenPhoto = ImageTk.PhotoImage(Open)

upload_Button=Button(f, image=uploadPhoto, command=add_file, bg="dark violet", relief=FLAT,activebackground="dark violet")
upload_Button.place(x=5, y=50)

download_Button = Button(f, image=downloadPhoto, bg="dark violet", relief=FLAT,activebackground="dark violet")
download_Button.place(x=90, y=50)

delete_Button=Button(f, image=deletePhoto, command=remove_from_cloud, bg="dark violet", relief=FLAT,activebackground="dark violet")
delete_Button.place(x=175, y=50)

Open_Button=Button(f, image= OpenPhoto, command=open_html, bg= "dark violet", relief=Flat,activebackground="dark violet")
Open_Button.place(x=90, y=10)

f.mainloop()