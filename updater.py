import tkinter as tk
import requests
import json
import os
from zipfile import ZipFile

devUrl = "https://raw.githubusercontent.com/V-o-x-a-r-y/Aizan-Version/main/developmentVersion.json"
stableUrl = "https://raw.githubusercontent.com/V-o-x-a-r-y/Aizan-Version/main/stableVersion.json"


def currentStableVersion():
    global scriptPath
    scriptPath = os.path.abspath(__file__)
    global versionPath
    # Construisez le chemin complet vers le fichier version.txt dans le même répertoire que le script
    versionPath = os.path.join(os.path.dirname(scriptPath), "versionStable.txt")

    # Vérifiez si le fichier version.txt existe
    if os.path.exists(versionPath):
        with open(versionPath, 'r') as versionFile:
            content = versionFile.read()
            return content
    else:
        open(versionPath, 'w').close()
        return False
def getStableVersion():
    global cSV
    response = requests.get(stableUrl)
    if response.status_code == 200:
        data = json.loads(response.text)
        stable_version = data.get("version")
    cSV = currentStableVersion()
    if not cSV:
        if stable_version == "unknow":
            os.system(f"cscript //nologo {os.path.join(os.path.dirname(scriptPath), "stableMSG.vbs")}")
    else: 
        with open(f'{versionPath}', 'w') as stableFile:
            stableFile.write(f"{stable_version}")
        updateStable(data.get("url"))
def updateStable(url):
    zip_file_path = os.path.join(os.getenv("TEMP"), f"{cSV}.zip")
    extracted_folder_path = os.path.join(os.getenv("TEMP"), f"{cSV}")
    response = requests.get(url)
    with open(zip_file_path, "wb") as zip_file:
        zip_file.write(response.content)
    with ZipFile(zip_file_path, "r") as zip_ref:
        zip_ref.extractall(extracted_folder_path)
    new_folder_path = os.path.join(os.getenv("TEMP"), f"{cSV}")
    os.rename(extracted_folder_path, new_folder_path)
    os.remove(zip_file_path)

def currentDevVersion():
    global scriptPath
    scriptPath = os.path.abspath(__file__)
    global versionPath
    # Construisez le chemin complet vers le fichier version.txt dans le même répertoire que le script
    versionPath = os.path.join(os.path.dirname(scriptPath), "versionDev.txt")

    # Vérifiez si le fichier version.txt existe
    if os.path.exists(versionPath):
        with open(versionPath, 'r') as versionFile:
            content = versionFile.read()
            return content
    else:
        open(versionPath, 'w').close()
        return False  
def getDevVersion():
    global cDV
    response = requests.get(devUrl)
    if response.status_code == 200:
        data = json.loads(response.text)
        dev_version = data.get("version")
    cDV = currentDevVersion()
    if not cDV:
        if dev_version == "unknow":
            os.system(f"cscript //nologo {os.path.join(os.path.dirname(scriptPath), "devMSG.vbs")}")
    else: 
        with open(f'{versionPath}', 'w') as devFile:
            devFile.write(f"{dev_version}")
        updateDev(data.get("url"))
def updateDev(url):
    zip_file_path = os.path.join(os.getenv("TEMP"), f"{cDV}.zip")
    extracted_folder_path = os.path.join(os.getenv("TEMP"), f"{cDV}")
    response = requests.get(url)
    with open(zip_file_path, "wb") as zip_file:
        zip_file.write(response.content)
    with ZipFile(zip_file_path, "r") as zip_ref:
        zip_ref.extractall(extracted_folder_path)
    new_folder_path = os.path.join(os.getenv("TEMP"), f"{cDV}")
    os.rename(extracted_folder_path, new_folder_path)
    os.remove(zip_file_path)


class ChannelSelectorApp:
    def __init__(self, master):
        self.master = master
        master.title("")
        master.resizable(False, False)

        button_padding_percent = 10
        button_padding = int(300 * button_padding_percent / 100)

        self.stable_button = tk.Button(master, text="Canal Stable", command=self.select_stable_channel)
        self.development_button = tk.Button(master, text="Canal de Développement", command=self.select_development_channel)

        self.stable_button.grid(row=0, column=0, padx=button_padding, pady=button_padding)
        self.development_button.grid(row=1, column=0, padx=button_padding, pady=button_padding)

    def select_stable_channel(self):
        getStableVersion()
        self.master.destroy()

    def select_development_channel(self):
        getDevVersion()
        self.master.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = ChannelSelectorApp(root)
    root.mainloop()
