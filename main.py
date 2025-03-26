from tkinter import *
from tkinter import filedialog, simpledialog
import os
import shutil
import json
import subprocess
import webbrowser
from PIL import Image, ImageTk

class FeetDriveApp:
    DATA_FILE = "data.json"
    DATA_FOLDER = "data"

    def __init__(self, root):
        self.root = root
        self.root.title("FeetDrive")
        self.root.geometry("200x140")
        self.root.resizable(width=False, height=False)
        self.root.configure(bg="Coral")

        # wenn der ordner nicht existiert, erstelle ihn
        if not os.path.exists(self.DATA_FOLDER):
            os.makedirs(self.DATA_FOLDER)

        self.data = self.load_data()  # daten laden
        self.create_widgets()  # ui elemente erstellen
        self.update_html()  # html datei aktualisieren

    def load_data(self):
        # lade daten aus json datei oder gib eine leere liste zurück
        if os.path.exists(self.DATA_FILE):
            with open(self.DATA_FILE, "r", encoding="utf-8") as file:
                return json.load(file)
        return []

    def save_data(self):
        # speichere daten in json datei
        with open(self.DATA_FILE, "w", encoding="utf-8") as file:
            json.dump(self.data, file, indent=4)

    def authenticate(self):
        # passwortabfrage
        entered_password = simpledialog.askstring("passwort", "passwort eingeben:", show="🦶🏿")
        with open('config.json') as f:
            config = json.load(f)

        # überprüfe ob passwort korrekt ist
        return entered_password == config['password']

    def update_html(self):
        # html datei mit dateiliste aktualisieren
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
        # erstelle link liste für hochgeladene dateien
        for file in self.data:
            file_name = os.path.basename(file)
            html_content += f'        <li><a href="https://github.com/Smokez01/Projekt/raw/main/data/{file_name}" target="_blank">{file_name}</a></li>\n'

        html_content += """    </ul>
</body>
</html>"""

        with open(html_file, "w", encoding="utf-8") as file:
            file.write(html_content)

    def upload_to_github(self):
        # versuche daten auf github hochzuladen
        try:
            subprocess.run(["git", "add", "data/"], check=True)
            subprocess.run(["git", "commit", "-m", "update data"], check=True)
            subprocess.run(["git", "push"], check=True)
            print("daten erfolgreich auf github hochgeladen!")
        except subprocess.CalledProcessError as e:
            print(f"fehler beim hochladen: {e}")

    def add_file(self):
        # datei auswählen und kopieren
        file_path = filedialog.askopenfilename(title="datei auswählen")
        if file_path:
            file_name = os.path.basename(file_path)
            dest_path = os.path.join(self.DATA_FOLDER, file_name)

            shutil.copy(file_path, dest_path)
            self.data.append(dest_path)
            self.save_data()
            self.upload_to_github()
            self.open_html()

    def remove_from_cloud(self):
        # erst passwort abfragen
        if not self.authenticate():
            print("falsches passwort! zugriff verweigert.")
            return

        # dateinamen eingeben zum löschen
        file_to_remove = simpledialog.askstring("datei entfernen", "dateinamen eingeben:")

        if file_to_remove:
            file_to_remove_path = os.path.join(self.DATA_FOLDER, file_to_remove)

            # prüfen ob datei existiert
            if file_to_remove_path.lower() in (file.lower() for file in self.data):
                self.data = [f for f in self.data if f.lower() != file_to_remove_path.lower()]
                if os.path.exists(file_to_remove_path):
                    os.remove(file_to_remove_path)
                    print(f"{file_to_remove} wurde gelöscht.")
                else:
                    print("datei existiert nicht.")
                self.save_data()
                self.upload_to_github()
                self.open_html()
            else:
                print("datei nicht gefunden.")

    def open_html(self):
        # öffnet die html datei im browser
        self.update_html()
        webbrowser.open("cloud.html")

    def load_image(self, path, size=(40, 40)):
        # bild laden und skalieren
        img = Image.open(path)
        img = img.resize(size, Image.Resampling.LANCZOS)
        return ImageTk.PhotoImage(img)

    def create_widgets(self):
        # bilder für buttons laden
        upload_img = self.load_image("images/upload.png")
        download_img = self.load_image("images/download.png")
        delete_img = self.load_image("images/delete.png")
        open_img = self.load_image("images/open.png")

        button_bg_color = "coral"
        button_ab_color = "aqua"

        # buttons erstellen und platzieren
        Button(self.root, image=open_img, command=self.open_html, bg=button_bg_color, relief=FLAT, activebackground=button_ab_color).place(x=80, y=10)
        Button(self.root, image=upload_img, command=self.add_file, bg=button_bg_color, relief=FLAT, activebackground=button_ab_color).place(x=10, y=80)
        Button(self.root, image=download_img, command=self.open_html, bg=button_bg_color, relief=FLAT, activebackground=button_ab_color).place(x=80, y=80)
        Button(self.root, image=delete_img, command=self.remove_from_cloud, bg=button_bg_color, relief=FLAT, activebackground=button_ab_color).place(x=150, y=80)
        

        # bilder speichern, damit sie nicht aus dem speicher gelöscht werden
        self.upload_img = upload_img
        self.download_img = download_img
        self.delete_img = delete_img
        self.open_img = open_img


# startet die app
if __name__ == "__main__":
    root = Tk()
    app = FeetDriveApp(root)
    root.mainloop()