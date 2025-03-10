from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk
import webbrowser
import os

# Liste für Dateien
Data = []

# Hauptfenster erstellen
f = Tk()
f.title("FeetDrive")
f.geometry("200x140")
f.resizable(width=False, height=False)
f.configure(bg="dark violet")

# Icon setzen (optional)
icon_path = "images/Feet.ico"
if os.path.exists(icon_path):
    f.iconbitmap(icon_path)

# Funktion zur Aktualisierung der Cloud.html
def update_html():
    html_content = """<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>FeetDrive Cloud</title>
    <style>
        body { font-family: Arial, sans-serif; background-color: #222; color: white; text-align: center; }
        h1 { color: #ffcc00; }
        ul { list-style-type: none; padding: 0; }
        li { background: #444; margin: 5px; padding: 10px; border-radius: 5px; }
    </style>
</head>
<body>
    <h1>FeetDrive Cloud</h1>
    <ul>
"""
    for file in Data:
        file_name = os.path.basename(file)
        file_path = os.path.abspath(file)
        html_content += f'        <li><a href="file://{file_path}" target="_blank">{file_name}</a></li>\n'

    html_content += """    </ul>
</body>
</html>"""

    with open("Cloud.html", "w", encoding="utf-8") as file:
        file.write(html_content)

# Funktion zum Öffnen der Cloud.html
def open_html():
    update_html()  # HTML aktualisieren, bevor es geöffnet wird
    file_path = os.path.abspath("Cloud.html")
    webbrowser.open(f"file://{file_path}")

# Datei hinzufügen
def add_file():
    file_path = filedialog.askopenfilename(title="Datei auswählen")
    if file_path:
        Data.append(file_path)
        update_html()
        open_html()

# Datei entfernen
def remove_from_cloud():
    if Data:
        Data.pop()  # Entferne die zuletzt hinzugefügte Datei (kein GUI-Auswahl-Mechanismus)
        update_html()
        open_html()

# Datei herunterladen (Dummy-Funktion)
def download_file():
    open_html()

# Bilder laden
def load_image(path, size=(40, 40)):
    img = Image.open(path)
    img = img.resize(size, Image.Resampling.LANCZOS)
    return ImageTk.PhotoImage(img)

uploadPhoto = load_image("images/upload.png")
downloadPhoto = load_image("images/download.png")
deletePhoto = load_image("images/delete.png")
openPhoto = load_image("images/open.png")

# Buttons erstellen
upload_Button = Button(f, image=uploadPhoto, command=add_file, bg="dark violet", relief=FLAT, activebackground="dark violet")
upload_Button.place(x=10, y=80)

download_Button = Button(f, image=downloadPhoto, command=download_file, bg="dark violet", relief=FLAT, activebackground="dark violet")
download_Button.place(x=80, y=80)

delete_Button = Button(f, image=deletePhoto, command=remove_from_cloud, bg="dark violet", relief=FLAT, activebackground="dark violet")
delete_Button.place(x=150, y=80)

open_Button = Button(f, image=openPhoto, command=open_html, bg="dark violet", relief=FLAT, activebackground="dark violet")
open_Button.place(x=80, y=10)

# Tkinter-Hauptloop starten
f.mainloop()
