from tkinter import *
from tkinter import filedialog, simpledialog  # für Passwortabfrage
import os
import shutil
import json
import subprocess
import webbrowser
from PIL import Image, ImageTk

DATA_FILE = "data.json"
DATA_FOLDER = "data"

if not os.path.exists(DATA_FOLDER):
    os.makedirs(DATA_FOLDER)

f = Tk()
f.title("FeetDrive")
f.geometry("200x140")
f.resizable(width=False, height=False)
f.configure(bg="Coral")

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    return []

def save_data():
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(Data, file, indent=4)

Data = load_data()

def authenticate():
    entered_password = simpledialog.askstring("Passwort", "Passwort eingeben:", show="*")
    with open('config.json') as f:
        config = json.load(f)

    correct_password = config['password']
    return entered_password == correct_password

def update_html():
    html_file = "cloud.html"
    
    if os.path.exists(html_file):
        os.remove(html_file)
    
    html_content = """<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <title>FeetDrive Cloud</title>
    <style>
        body { font-family: Comic Sans MS, sans-serif; background-color: Navy; color: PaleVioletRed; text-align: center; }
        h1 { color: Lavender; }
        ul { list-style-type: none; padding: 0; }
        li { margin: 5px; padding: 10px; }
        a { color: PaleVioletRed; text-decoration: none; }
        a:hover { text-decoration: underline; }
    </style>
</head>
<body>
    <img src="images/feetdrive.png" alt="FeetDrive Logo" width="1000">
    <ul>
"""
    for file in Data:
        file_name = os.path.basename(file)
        html_content += f'        <li><a href="https://github.com/Smokez01/Projekt/raw/main/data/{file_name}" target="_blank">{file_name}</a></li>\n'
    
    html_content += """    </ul>
</body>
</html>"""
    
    with open(html_file, "w", encoding="utf-8") as file:
        file.write(html_content)

def upload_to_github():
    try:
        subprocess.run(["git", "add", "data/"], check=True)
        subprocess.run(["git", "commit", "-m", "Update data"], check=True)
        subprocess.run(["git", "push"], check=True)
        print("Daten erfolgreich auf GitHub hochgeladen!")
    except subprocess.CalledProcessError as e:
        print(f"Fehler beim Hochladen: {e}")

def add_file():
    file_path = filedialog.askopenfilename(title="Datei auswählen")
    if file_path:
        file_name = os.path.basename(file_path)
        dest_path = os.path.join(DATA_FOLDER, file_name)
        shutil.copy(file_path, dest_path)
        Data.append(dest_path)
        save_data()
        upload_to_github()
        open_html()

def remove_from_cloud():
    if not authenticate():
        print("Falsches Passwort! Zugriff verweigert.")
        return
    
    file_to_remove = simpledialog.askstring("Datei entfernen", "Dateinamen eingeben, der gelöscht werden soll:")
    
    if file_to_remove:
        file_to_remove_path = os.path.join(DATA_FOLDER, file_to_remove)
        
        if file_to_remove_path.lower() in (file.lower() for file in Data):
            # Datei existiert in der Liste
            Data.remove(file_to_remove_path)
            if os.path.exists(file_to_remove_path):
                os.remove(file_to_remove_path)
                print(f"{file_to_remove} wurde gelöscht.")
            else:
                print("Datei existiert nicht im Dateisystem.")
            save_data()
            upload_to_github()
            open_html()
        else:
            print("Datei nicht in der Liste gefunden.")

def open_html():
    update_html()
    webbrowser.open("cloud.html")

# Bilder laden
def load_image(path, size=(40, 40)):
    img = Image.open(path)
    img = img.resize(size, Image.Resampling.LANCZOS)
    return ImageTk.PhotoImage(img)

uploadPhoto = load_image("images/upload.png")
downloadPhoto = load_image("images/download.png")
deletePhoto = load_image("images/delete.png")
openPhoto = load_image("images/open.png")

button_bg_color = "Coral"
button_ab_color = "Aqua"

upload_Button = Button(f, image=uploadPhoto, command=add_file, bg=button_bg_color, relief=FLAT, activebackground=button_ab_color)
upload_Button.place(x=10, y=80)

download_Button = Button(f, image=downloadPhoto, command=open_html, bg=button_bg_color, relief=FLAT, activebackground=button_ab_color)
download_Button.place(x=80, y=80)

delete_Button = Button(f, image=deletePhoto, command=remove_from_cloud, bg=button_bg_color, relief=FLAT, activebackground=button_ab_color)
delete_Button.place(x=150, y=80)

open_Button = Button(f, image=openPhoto, command=open_html, bg=button_bg_color, relief=FLAT, activebackground=button_ab_color)
open_Button.place(x=80, y=10)

update_html()

f.mainloop()