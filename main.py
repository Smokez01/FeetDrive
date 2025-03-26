from tkinter import *
from tkinter import filedialog, simpledialog
import os
import shutil
import json
import subprocess
import webbrowser
from PIL import Image, ImageTk

class FeetDriveApp:
    # Definiert die Dateinamen für gespeicherte Daten und den Ordner, wo Dateien gespeichert werden
    DATA_FILE = "data.json"
    DATA_FOLDER = "data"

    def __init__(self, root):
        self.root = root
        self.root.title("FeetDrive")  # Titel des Fensters setzen
        self.root.geometry("200x140")  # Fenstergröße festlegen
        self.root.resizable(width=False, height=False)  # Größe nicht veränderbar
        self.root.configure(bg="Coral")  # Hintergrundfarbe setzen

        # Falls der Daten-Ordner nicht existiert, erstelle ihn
        if not os.path.exists(self.DATA_FOLDER):
            os.makedirs(self.DATA_FOLDER)

        self.data = self.load_data()  # Vorhandene Daten laden
        self.create_widgets()  # Buttons und UI-Elemente erstellen
        self.update_html()  # HTML-Datei aktualisieren

    def load_data(self):
        # Falls eine gespeicherte Datenliste existiert, lade sie
        if os.path.exists(self.DATA_FILE):
            with open(self.DATA_FILE, "r", encoding="utf-8") as file:
                return json.load(file)
        return []  # Falls nicht, gib eine leere Liste zurück

    def save_data(self):
        # Speichert die aktuelle Dateiliste in einer JSON-Datei
        with open(self.DATA_FILE, "w", encoding="utf-8") as file:
            json.dump(self.data, file, indent=4)

    def authenticate(self):
        # Fragt den Benutzer nach einem Passwort 
        entered_password = simpledialog.askstring("Passwort", "Passwort eingeben:", show="🦶🏿")

        # Passwort aus der Konfigurationsdatei laden
        with open('config.json') as f:
            config = json.load(f)

        # Überprüfen, ob das eingegebene Passwort korrekt ist
        return entered_password == config['password']

    def update_html(self):
        # Erstellt eine HTML-Datei mit einer Liste der hochgeladenen Dateien
        html_file = "cloud.html"

        # Falls eine alte Version existiert, löschen
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
        # Jede Datei in der Datenliste wird als Link hinzugefügt
        for file in self.data:
            file_name = os.path.basename(file)
            html_content += f'        <li><a href="https://github.com/Smokez01/Projekt/raw/main/data/{file_name}" target="_blank">{file_name}</a></li>\n'

        html_content += """    </ul>
</body>
</html>"""

        # HTML-Datei speichern
        with open(html_file, "w", encoding="utf-8") as file:
            file.write(html_content)

    def upload_to_github(self):
        # Versucht, die Daten auf GitHub hochzuladen
        try:
            subprocess.run(["git", "add", "data/"], check=True)
            subprocess.run(["git", "commit", "-m", "Update data"], check=True)
            subprocess.run(["git", "push"], check=True)
            print("Daten erfolgreich auf GitHub hochgeladen!")
        except subprocess.CalledProcessError as e:
            print(f"Fehler beim Hochladen: {e}")

    def add_file(self):
        # Datei vom PC auswählen
        file_path = filedialog.askopenfilename(title="Datei auswählen")
        if file_path:
            file_name = os.path.basename(file_path)
            dest_path = os.path.join(self.DATA_FOLDER, file_name)

            # Datei kopieren
            shutil.copy(file_path, dest_path)
            self.data.append(dest_path)
            self.save_data()
            self.upload_to_github()
            self.open_html()

    def remove_from_cloud(self):
        # Erst nach Passwort fragen
        if not self.authenticate():
            print("Falsches Passwort! Zugriff verweigert.")
            return
        
        # Dateinamen eingeben, der gelöscht werden soll
        file_to_remove = simpledialog.askstring("Datei entfernen", "Dateinamen eingeben, der gelöscht werden soll:")

        if file_to_remove:
            file_to_remove_path = os.path.join(self.DATA_FOLDER, file_to_remove)
            
            # Prüfen, ob die Datei in der Cloud existiert
            if file_to_remove_path.lower() in (file.lower() for file in self.data):
                # Datei aus der Liste entfernen und ggf. auch vom PC löschen
                self.data = [f for f in self.data if f.lower() != file_to_remove_path.lower()]
                if os.path.exists(file_to_remove_path):
                    os.remove(file_to_remove_path)
                    print(f"{file_to_remove} wurde gelöscht.")
                else:
                    print("Datei existiert nicht im Dateisystem.")
                self.save_data()
                self.upload_to_github()
                self.open_html()
            else:
                print("Datei nicht in der Liste gefunden.")

    def open_html(self):
        # HTML aktualisieren und im Browser öffnen
        self.update_html()
        webbrowser.open("cloud.html")

    def load_image(self, path, size=(40, 40)):
        # Bild laden, skalieren und für Tkinter umwandeln
        img = Image.open(path)
        img = img.resize(size, Image.Resampling.LANCZOS)
        return ImageTk.PhotoImage(img)

    def create_widgets(self):
        # Bilder für Buttons laden
        upload_img = self.load_image("images/upload.png")
        download_img = self.load_image("images/download.png")
        delete_img = self.load_image("images/delete.png")
        open_img = self.load_image("images/open.png")

        button_bg_color = "Coral"  # Gleiche Farbe wie der Hintergrund
        button_ab_color = "Aqua"   # Aktive Farbe

        # Buttons erstellen und platzieren
        Button(self.root, image=upload_img, command=self.add_file, bg=button_bg_color, relief=FLAT, activebackground=button_ab_color).place(x=10, y=80)
        Button(self.root, image=download_img, command=self.open_html, bg=button_bg_color, relief=FLAT, activebackground=button_ab_color).place(x=80, y=80)
        Button(self.root, image=delete_img, command=self.remove_from_cloud, bg=button_bg_color, relief=FLAT, activebackground=button_ab_color).place(x=150, y=80)
        Button(self.root, image=open_img, command=self.open_html, bg=button_bg_color, relief=FLAT, activebackground=button_ab_color).place(x=80, y=10)

        # Bilder speichern, damit sie nicht aus dem Speicher gelöscht werden
        self.upload_img = upload_img
        self.download_img = download_img
        self.delete_img = delete_img
        self.open_img = open_img


# Starte die App
if __name__ == "__main__":
    root = Tk()
    app = FeetDriveApp(root)
    root.mainloop()
