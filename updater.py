import tkinter as tk
from tkinter import ttk
import requests
import json
import os
import sys
import zipfile
import subprocess
import concurrent.futures
from tqdm import tqdm

devUrl = "https://raw.githubusercontent.com/V-o-x-a-r-y/Aizan-Version/main/developmentVersion.json"
stableUrl = "https://raw.githubusercontent.com/V-o-x-a-r-y/Aizan-Version/main/stableVersion.json"

devMSG = """
Option Explicit

Dim message

' Définir le message à afficher
message = "Attention, il n'y pas de version de dev pour l'instant"

' Afficher la boîte de dialogue MsgBox
MsgBox message, vbInformation, "Attention
"""

stableMSG = """
Option Explicit

Dim message

' Définir le message à afficher
message = "Attention, il n'y pas de version stable pour l'instant"

' Afficher la boîte de dialogue MsgBox
MsgBox message, vbInformation, "Attention"

"""

def debug_message(message):
    if '--debug' in sys.argv:
        print(f"DEBUG: {message}")

def currentStableVersion():
    debug_message("Entering currentStableVersion function")
    
    global scriptPath
    scriptPath = os.path.abspath(__file__)
    debug_message(f"Current script path: {scriptPath}")
    
    global versionPath
    versionPath = os.path.join(os.path.dirname(scriptPath), "versionStable.txt")
    debug_message(f"Current version path: {versionPath}")

    if os.path.exists(versionPath):
        with open(versionPath, 'r') as versionFile:
            content = versionFile.read()
            debug_message(f"Read content from {versionPath}: {content}")
            if content:
                debug_message("Exiting currentStableVersion function")
                return content
            else:
                debug_message("Exiting currentStableVersion function")
                return False
    else:
        open(versionPath, 'w').close()
        debug_message(f"Created an empty file at {versionPath}")
        debug_message("Exiting currentStableVersion function")
        return False

def getStableVersion():
    debug_message("Entering getStableVersion function")

    global cSV
    response = requests.get(stableUrl)
    if response.status_code == 200:
        data = json.loads(response.text)
        stable_version_cloud = data.get("version")
        debug_message(f"Retrieved stable version from {stableUrl}: {stable_version_cloud}")
    cSV = currentStableVersion()

    version_folder_path = os.path.join(os.getenv("TEMP"), f"{cSV}")

    if not cSV or not os.path.exists(version_folder_path) or cSV != stable_version_cloud or '--debug' in sys.argv:
        if stable_version_cloud == "unknow":
            vbs_path = os.path.join(os.path.dirname(scriptPath), 'stableMSG.vbs')
            with open(vbs_path, 'w') as VBSfile:
                VBSfile.write(f"{stableMSG}")
                debug_message(f"Created VBS file at {vbs_path}")
            os.system(f"cscript //nologo {vbs_path}")
            debug_message(f"Executed 'cscript //nologo {vbs_path}'")
            os.remove(vbs_path)
            debug_message(f"Removed VBS file at {vbs_path}")
        else:
            with open(f'{versionPath}', 'w') as stableFile:
                stableFile.write(f"{stable_version_cloud}")
                debug_message(f"Updated {versionPath} with stable version: {stable_version_cloud}")
            update(data.get("url"))

    debug_message("Exiting getStableVersion function")

def currentDevVersion():
    debug_message("Entering currentDevVersion function")
    
    global scriptPath
    scriptPath = os.path.abspath(__file__)
    debug_message(f"Current script path: {scriptPath}")
    
    global versionPath
    versionPath = os.path.join(os.path.dirname(scriptPath), "versionDev.txt")
    debug_message(f"Current version path: {versionPath}")

    if os.path.exists(versionPath):
        with open(versionPath, 'r') as versionFile:
            content = versionFile.read()
            debug_message(f"Read content from {versionPath}: {content}")
            if content:
                debug_message("Exiting currentDevVersion function")
                return content
            else:
                debug_message("Exiting currentDevVersion function")
                return False
    else:
        open(versionPath, 'w').close()
        debug_message(f"Created an empty file at {versionPath}")
        debug_message("Exiting currentDevVersion function")
        return False  

def getDevVersion():
    debug_message("Entering getDevVersion function")
    
    global cDV
    response = requests.get(devUrl)
    if response.status_code == 200:
        data = json.loads(response.text)
        dev_version_cloud = data.get("version")
        debug_message(f"Retrieved development version from {devUrl}: {dev_version_cloud}")
    cDV = currentDevVersion()

    version_folder_path = os.path.join(os.getenv("TEMP"), f"{cDV}")

    if not cDV or not os.path.exists(version_folder_path) or cDV != dev_version_cloud or '--debug' in sys.argv:
        if dev_version_cloud == "unknow":
            vbs_path = os.path.join(os.path.dirname(scriptPath), 'devMSG.vbs')
            os.system(f"cscript //nologo {vbs_path}")
            debug_message(f"Executed 'cscript //nologo {vbs_path}'")
        else:
            with open(f'{versionPath}', 'w') as devFile:
                devFile.write(f"{dev_version_cloud}")
                debug_message(f"Updated {versionPath} with development version: {dev_version_cloud}")
            update(data.get("url"))

    debug_message("Exiting getDevVersion function")

def download_and_extract(url, zip_file_path, extracted_folder_path, progress_var):
    response = requests.get(url, stream=True)

    # Vérifiez si la réponse HTTP est réussie
    if response.status_code == 200:
        total_size = int(response.headers.get('content-length', 0))
        block_size = 1024  # 1 Kibibyte

        # Utilisez tqdm pour créer une barre de progression
        with tqdm(total=total_size, unit='B', unit_scale=True, unit_divisor=1024) as progress_bar:
            with open(zip_file_path, 'wb') as zip_file:
                for data in response.iter_content(block_size):
                    zip_file.write(data)
                    progress_bar.update(len(data))
                    progress_var.set(progress_bar.n / progress_bar.total * 100)

        # Extraction du fichier ZIP
        with zipfile.ZipFile(zip_file_path, "r") as zip_ref:
            zip_ref.extractall(extracted_folder_path)

        # Supprimez le fichier ZIP après extraction
        os.remove(zip_file_path)

def update(url):
    debug_message("Entering update function")

    cDV = "v1.6.2-alpha"  # Remplacez par la version actuelle
    extracted_folder_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), cDV)
    zip_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), f"{cDV}.zip")

    root = tk.Tk()
    root.title("Updating...")
    root.geometry("400x50")

    progress_var = tk.DoubleVar()
    progress_bar = ttk.Progressbar(root, variable=progress_var, length=400, mode="determinate")
    progress_bar.pack()

    # Utilisez un thread pour le téléchargement et l'extraction
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future = executor.submit(download_and_extract, url, zip_file_path, extracted_folder_path, progress_var)

        # Mettez à jour la barre de progression à intervalles réguliers
        while not future.done():
            root.update()
            root.after(100)

    root.destroy()  # Fermez la fenêtre Tkinter après le téléchargement et l'extraction

    debug_message("Exiting update function")

class ChannelSelectorApp:
    def __init__(self, master):
        debug_message("Entering ChannelSelectorApp __init__ function")
        
        self.master = master
        master.title("")
        master.resizable(False, False)

        button_padding_percent = 10
        button_padding = int(300 * button_padding_percent / 100)

        self.stable_button = tk.Button(master, text="Canal Stable", command=self.select_stable_channel)
        self.development_button = tk.Button(master, text="Canal de Développement", command=self.select_development_channel)

        self.stable_button.grid(row=0, column=0, padx=button_padding, pady=button_padding)
        self.development_button.grid(row=1, column=0, padx=button_padding, pady=button_padding)

        debug_message("Exiting ChannelSelectorApp __init__ function")

    def select_stable_channel(self):
        debug_message("Entering select_stable_channel function")
        
        getStableVersion()
        
        debug_message("Exiting select_stable_channel function")
        self.master.destroy()

    def select_development_channel(self):
        debug_message("Entering select_development_channel function")
        
        getDevVersion()
        
        debug_message("Exiting select_development_channel function")
        self.master.destroy()

if __name__ == "__main__":
    debug_message("Entering __main__ block")

    root = tk.Tk()
    app = ChannelSelectorApp(root)
    root.mainloop()

    debug_message("Exiting __main__ block")
