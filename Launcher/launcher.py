#Imports
from sys import version_info as vi
from subprocess import call, TimeoutExpired
import sys
import tkinter as tk
import webbrowser
import os
import contextlib
import zipfile
import requests
import shutil
import requests
        
#Get all the versions
versions = requests.get("https://minecraft-python-v2.drakeerv.repl.co/versions.php").content.decode().split("<br>")
versions.pop(-1)

#Find all installations
installations = []

for i in [x for x in os.listdir() if "." not in x and "textures" not in x]:
    if os.path.isfile(f"{i}/mc-python-version"):
        installations.append(i)

#Checks a given number to see if it is a int and it is greater than 0
def check_number(number_to_check):
    with contextlib.suppress(ValueError):
        if(int(number_to_check) > 0):
            return True

    return False

#downloads a url file
def download_url(url, save_path, chunk_size=128):
    r = requests.get(url, stream=True)
    with open(save_path, 'wb') as fd:
        for chunk in r.iter_content(chunk_size=chunk_size):
            fd.write(chunk)

#First time setup
if not os.path.isfile("./options.txt"):
    with open("options.txt", "w") as file:
        file.write(f"optionsHeight = 600\n")
        file.write(f"optionsWidth = 800\n")
        file.write(f"optionsVsync = True\n")
        file.write(f"optionsFpsWindow = False\n")

if not os.path.isdir("./textures"):
    file_name = "textures.zip"
    
    download_url(f"https://minecraft-python-v2.drakeerv.repl.co/{file_name}", f"./{file_name}")
    with zipfile.ZipFile(f"./{file_name}") as file:
            file.extractall("./")

    os.remove(f"./{file_name}")

#Opens the local folder
def open_folder():
    webbrowser.open(os.path.realpath("./"))

#Opens the website with the deafault browser
def open_website():
    webbrowser.open("https://github.com/obiwac/python-minecraft-clone")

#Creates and returns a info message
def info(message):
    return ''.join(['===================================================\n',
            f'{str(message)}\n',
            '===================================================\n'])

#Defines the launch function
def launch():
    print(info('Launch: Minecraft Clone'))
    os.chdir(installation_var.get())

    with contextlib.suppress(TimeoutExpired):
        call(f"{sys.executable} main.py", shell=True, timeout=5)

    os.chdir("..")

#Creates the options menu
def create_options_menu():
    options = tk.Toplevel(root)

    #Apply the changes
    def apply():
        open('options.txt', 'w').close()

        height_entry = entry_height.get()
        width_entry = entry_width.get()
        vsync_entry = vsync_bool.get()
        fps_entry = fps_bool.get()

        if not check_number(height_entry):
            height_entry = 600

        if not check_number(width_entry):
            width_entry = 800

        with open('options.txt', 'a') as file:
            file.write(f"optionsHeight = {height_entry}\n")
            file.write(f"optionsWidth = {width_entry}\n")
            file.write(f"optionsVsync = {vsync_entry}\n")
            file.write(f"optionsFpsWindow = {fps_entry}\n")

    vsync_bool = tk.BooleanVar()
    fps_bool = tk.BooleanVar()

    options_title = tk.Label(options, text="Options Menu", font=('helvetica', 15, 'bold'))
    options_description = tk.Label(options, text="Leave everything blank to reset to deafault.", font=('helvetica', 11, 'normal'))
    exit_button = tk.Button(options, text="Exit", command=options.destroy, bg='red', fg='white', font=('helvetica', 12, 'bold'))
    apply_button = tk.Button(options, text="Apply", command=apply, bg='blue', fg='white', font=('helvetica', 12, 'bold'))
    vsync_checkbox = tk.Checkbutton(options, text="Enable Vsync", variable=vsync_bool, onvalue=True, offvalue=False)
    fps_checkbox = tk.Checkbutton(options, text="Enable FPS Window", variable=fps_bool, onvalue=True, offvalue=False)
    height_label = tk.Label(options, text="Height:")
    width_label = tk.Label(options, text="Width:")
    entry_height = tk.Spinbox(options, value=600, from_=1, to=9000)
    entry_width = tk.Spinbox(options, value=800, from_=1, to=9000)

    options_title.place(relx=0.5, rely=0.1, anchor=tk.CENTER)
    options_description.place(relx=0.5, rely=0.8, anchor=tk.CENTER)
    exit_button.place(relx=0.0, rely=0.0, anchor=tk.NW)
    apply_button.place(relx=1, rely=0, anchor=tk.NE)
    entry_height.place(relx=0.3, rely=0.5, anchor=tk.CENTER)
    height_label.place(relx=0.3, rely=0.4, anchor=tk.CENTER)
    entry_width.place(relx=0.7, rely=0.5, anchor=tk.CENTER)
    width_label.place(relx=0.7, rely=0.4, anchor=tk.CENTER)
    vsync_checkbox.place(relx=0.5, rely=0.6, anchor=tk.CENTER)
    fps_checkbox.place(relx=0.5, rely=0.7, anchor=tk.CENTER)

    options.resizable(0, 0)
    options.title("Minecraft Python Options")
    options.iconphoto(False, icon)
    options.geometry("500x400")

def create_installation_menu():
    installation_menu = tk.Toplevel(root)

    #Download the selected version
    def download_version():
        download_url(f"https://minecraft-python-v2.drakeerv.repl.co/{versions_download_var.get()}.zip", f"./{versions_download_var.get()}.zip")

        with zipfile.ZipFile(f"./{versions_download_var.get()}") as file:
            file.extractall("./")

        os.remove(f"./{versions_download_var.get()}")

        finished_download_label = tk.Label(installation_menu, text="Done! Please restart your launcher to play your version!")

        finished_download_label.place(relx=0.5, rely=0.6, anchor=tk.S)

    def remove_version():
        shutil.rmtree(f"./{versions_remove_var.get()}")

        finished_remove_label = tk.Label(installation_menu, text="Done! Please restart your launcher to see the changes!")

        finished_remove_label.place(relx=0.5, rely=1, anchor=tk.S)

    versions_download_var = tk.StringVar(installation_menu)
    versions_download_var.set(versions[-1].replace(".zip", ""))
    versions_download_picker = tk.OptionMenu(installation_menu, versions_download_var, *[s.replace(".zip", "") for s in versions])

    with contextlib.suppress(IndexError, TypeError):
        versions_remove_var = tk.StringVar(installation_menu)
        versions_remove_var.set(installations[-1])
        versions_remove_picker = tk.OptionMenu(installation_menu, versions_remove_var, *installations)

    installation_menu_title = tk.Label(installation_menu, text="Installation Menu", font=('helvetica', 15, 'bold'))
    exit_button = tk.Button(installation_menu, text="Exit", command=installation_menu.destroy, bg='red', fg='white', font=('helvetica', 12, 'bold'))
    no_installation_label = tk.Label(installation_menu, text="There are no installations! Please download one.")

    installation_menu_title.place(relx=0.5, rely=0.1, anchor=tk.CENTER)
    exit_button.place(relx=0.0, rely=0.0, anchor=tk.NW)

    versions_remove_label = tk.Label(installation_menu, text="Please pick the veriosn you want to remove:")
    versions_remove = tk.Button(installation_menu, text="Remove Version", command=remove_version, bg='red', fg='white', font=('helvetica', 12, 'bold'))

    if len(installations) > 0:
        versions_remove_label.place(relx=0.5, rely=0.7, anchor=tk.CENTER)
        versions_remove_picker.place(relx=0.5, rely=0.8, anchor=tk.CENTER)
        versions_remove.place(relx=0.5, rely=0.9, anchor=tk.CENTER)
    else:
        no_installation_label.place(relx=0.5, rely=0.8, anchor=tk.CENTER)

    versions_download_label = tk.Label(installation_menu, text="Please pick the version you want to install:")
    versions_download = tk.Button(installation_menu, text="Download Version", command=download_version, bg='blue', fg='white', font=('helvetica', 12, 'bold'))

    versions_download_label.place(relx=0.5, rely=0.3, anchor=tk.CENTER)
    versions_download_picker.place(relx=0.5, rely=0.4, anchor=tk.CENTER)
    versions_download.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    installation_menu.resizable(0, 0)
    installation_menu.title("Minecraft Python Installation Menu")
    installation_menu.iconphoto(False, icon)
    installation_menu.geometry("500x400")

#Creates the main window
root = tk.Tk()

icon = tk.PhotoImage(file ="textures/icon.png")
installation_var = tk.StringVar(root)

with contextlib.suppress(IndexError):
    installation_var.set(installations[-1])
    installation_picker = tk.OptionMenu(root, installation_var, *installations)

launch_button = tk.Button(root, text='      Launch Minecraft: Python Edition    ', command=launch, bg='green', fg='white', font=('helvetica', 12, 'bold'))
installation_menu_button = tk.Button(root, text='Version Manager', command=create_installation_menu, bg='blue', fg='white')
open_button = tk.Button(root, text='Open Folder', command=open_folder,  bg='blue', fg='white', font=('helvetica', 12, 'bold'))
website_button = tk.Button(root, text='Open Website', command=open_website,  bg='blue', fg='white', font=('helvetica', 12, 'bold'))
exit_button = tk.Button(root, text="Exit", command=root.destroy, bg='red', fg='white', font=('helvetica', 12, 'bold'))
options_button = tk.Button(root, text="Options", command=create_options_menu, bg='blue', fg='white', font=('helvetica', 12, 'bold'))
launch_version = tk.Label(root, text=f"Launcher version: 2")
python_version = tk.Label(root, text=f"Python version: {vi.major}.{vi.minor}.{vi.micro}")
mc_title = tk.Label(root, text="Minecraft: Python Edition", font=('helvetica', 24, 'bold'))

no_installation_label = tk.Label(root, text="There are no installations! Please download one.")
installation_label = tk.Label(root, text="Installations:")

exit_button.place(relx=0.0, rely=0.0, anchor=tk.NW)
open_button.place(relx=0.48, rely=1.0, anchor=tk.SE)
website_button.place(relx=0.52, rely=1.0, anchor=tk.SW)
options_button.place(relx=1, rely=0, anchor=tk.NE)
mc_title.place(relx=0.5, rely=0.3, anchor=tk.CENTER)
python_version.place(relx=0.0, rely=1, anchor=tk.SW)
launch_button.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
installation_menu_button.place(relx=0.5, rely=0.8, anchor=tk.CENTER)

if len(installations) > 0:
    installation_label.place(relx=0.5, rely=0.65, anchor=tk.CENTER)
    installation_picker.place(relx=0.5, rely=0.7, anchor=tk.CENTER)
    launch_version.place(relx=1, rely=1, anchor=tk.SE)
else:
    no_installation_label.place(relx=0.5, rely=0.65, anchor=tk.CENTER)

root.resizable(0, 0)
root.title("Minecraft Python Launcher")
root.iconphoto(False, icon) 
root.geometry("600x500")

root.mainloop()