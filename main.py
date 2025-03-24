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

        if not os.path.exists(self.DATA_FOLDER):
            os.makedirs(self.DATA_FOLDER)

        self.data = self.load_data()
        self.create_widgets()
        self.update_html()

    def load_data(self):
        if os.path.exists(self.DATA_FILE):
            with open(self.DATA_FILE, "r", encoding="utf-8") as file:
                return json.load(file)
        return []

    def save_data(self):
        with open(self.DATA_FILE, "w", encoding="utf-8") as file:
            json.dump(self.data, file, indent=4)

    def authenticate(self):
        entered_password = simpledialog.askstring("Passwort", "Passwort eingeben:", show="🦶")
        with open('config.json') as f:
            config = json.load(f)

        correct_password = config['password']
        return entered_password == correct_password

    def update_html(self):
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
        for file in self.data:
            file_name = os.path.basename(file)
            html_content += f'        <li><a href="https://github.com/Smokez01/Projekt/raw/main/data/{file_name}" target="_blank">{file_name}</a></li>\n'
        
        html_content += """    </ul>
</body>
</html>"""
        
        with open(html_file, "w", encoding="utf-8") as file:
            file.write(html_content)

    def upload_to_github(self):
        try:
            subprocess.run(["git", "add", "data/"], check=True)
            subprocess.run(["git", "commit", "-m", "Update data"], check=True)
            subprocess.run(["git", "push"], check=True)
            print("Daten erfolgreich auf GitHub hochgeladen!")
        except subprocess.CalledProcessError as e:
            print(f"Fehler beim Hochladen: {e}")

    def add_file(self):
        file_path = filedialog.askopenfilename(title="Datei auswählen")
        if file_path:
            file_name = os.path.basename(file_path)
            dest_path = os.path.join(self.DATA_FOLDER, file_name)
            shutil.copy(file_path, dest_path)
            self.data.append(dest_path)
            self.save_data()
            self.upload_to_github()
            self.open_html()

    def remove_from_cloud(self):
        if not self.authenticate():
            print("Falsches Passwort! Zugriff verweigert.")
            return
        
        file_to_remove = simpledialog.askstring("Datei entfernen", "Dateinamen eingeben, der gelöscht werden soll:")
        
        if file_to_remove:
            file_to_remove_path = os.path.join(self.DATA_FOLDER, file_to_remove)
            
            if file_to_remove_path.lower() in (file.lower() for file in self.data):
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
        self.update_html()
        webbrowser.open("cloud.html")

    def load_image(self, path, size=(40, 40)):
        img = Image.open(path)
        img = img.resize(size, Image.Resampling.LANCZOS)
        return ImageTk.PhotoImage(img)

    def create_widgets(self):
        upload_img = self.load_image("images/upload.png")
        download_img = self.load_image("images/download.png")
        delete_img = self.load_image("images/delete.png")
        open_img = self.load_image("images/open.png")

        button_bg_color = "Coral"
        button_ab_color = "Aqua"

        Button(self.root, image=upload_img, command=self.add_file, bg=button_bg_color, relief=FLAT, activebackground=button_ab_color).place(x=10, y=80)
        Button(self.root, image=download_img, command=self.open_html, bg=button_bg_color, relief=FLAT, activebackground=button_ab_color).place(x=80, y=80)
        Button(self.root, image=delete_img, command=self.remove_from_cloud, bg=button_bg_color, relief=FLAT, activebackground=button_ab_color).place(x=150, y=80)
        Button(self.root, image=open_img, command=self.open_html, bg=button_bg_color, relief=FLAT, activebackground=button_ab_color).place(x=80, y=10)

        # Bilder referenzieren, damit sie nicht vom Garbage Collector entfernt werden
        self.upload_img = upload_img
        self.download_img = download_img
        self.delete_img = delete_img
        self.open_img = open_img


if __name__ == "__main__":
    root = Tk()
    app = FeetDriveApp(root)
    root.mainloop()
