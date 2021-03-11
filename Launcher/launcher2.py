# BETA
# Minecraft Python Launcher
# Made by drakeerv
# TODO:
# 1. Make it check for texture update
# 2. Install verions
# 3. Make setup screen better (Progress bar)

import os
import sys
import subprocess
import contextlib
import requests
import zipfile
import pyglet

import tkinter as tk

# Global directory vars
installations_directory = "versions"
assets_directory = "assets"

# Define vars
versions = None
installations = None

# Define function
def rgbtohex(r,g,b):
    return f"#{r:02x}{g:02x}{b:02x}"

#downloads a file
def download_url(url, save_path, chunk_size=128):
    r = requests.get(url, stream=True)
    with open(save_path, "wb") as fd:
        for chunk in r.iter_content(chunk_size=chunk_size):
            fd.write(chunk)

# Launch
def launch(directory):
    print(directory)
    directory = os.path.realpath(directory)
    os.chdir(directory)

    with contextlib.suppress(subprocess.TimeoutExpired):
        subprocess.call(f"{sys.executable} main.py", shell=True, timeout=1)

    os.chdir("..")

def update_options(object, variable, options):
    object["menu"].delete(0, "end")
    for string in options:
        object["menu"].add_command(label=string)
    variable.set(options[-1])

# First time run
if not (os.path.isdir("versions") or os.path.isdir("assets")):
    # Create root
    root = tk.Tk()

    # Set window size
    window_width = 600
    window_height = 500

    # Define function
    def setup():
        if not os.path.isdir("versions"):
            os.mkdir("versions")
        if not os.path.isdir("assets"):
            download_url("https://minecraft-python-v2.drakeerv.repl.co/assets.zip", "assets.zip")
            with zipfile.ZipFile("assets.zip") as file:
                file.extractall()
            os.remove("assets.zip")
        root.destroy()

    # Creating widgets
    tk.Button(root, text="Exit", cursor="hand2", bg="red", font=("helvetica", 12, "bold"), command=lambda: exit()).place(x=window_width*0, y=window_height*0, anchor=tk.NW)
    tk.Button(root, text="    Download    ", cursor="hand2", bg="green", font=("helvetica", 12, "bold"), command=setup).place(x=window_width*0.5, y=window_height*0.5, anchor=tk.CENTER)
    tk.Label(root, text="The launcher needs to be setup. Please place this py file in the desired directory and hit download.").place(x=window_width*0.5, y=window_height*0.6, anchor=tk.CENTER)

    # Configure window
    root.resizable(0, 0)
    root.title("Minecraft Python Launcher")
    root.geometry(f"{window_width}x{window_height}")
    root.mainloop()

if not (os.path.isdir("versions") or os.path.isdir("assets")): exit()

# Import fonts
pyglet.font.add_file(f"{assets_directory}/Ubuntu-Bold.ttf")

# Pre-start setup
versions = [x for x in requests.get("https://minecraft-python-v2.drakeerv.repl.co/versions.php").content.decode().split("<br>") if "" != x]
installations = [x for x in os.listdir(installations_directory) if "mc-python-version" in os.listdir(f"{installations_directory}/{x}")]

def version_manager(parent_root):
    # Create root
    root = tk.Toplevel(parent_root)

    # Set colors
    background_color = rgbtohex(62, 62, 62)
    active_color = rgbtohex(62, 62, 62)
    foreground_color = rgbtohex(33, 33, 33)

    # Load images
    menu_image = tk.PhotoImage(file=f"{assets_directory}/menu.png")
    play_image = tk.PhotoImage(file=f"{assets_directory}/play.png")
    home_image = tk.PhotoImage(file=f"{assets_directory}/home.png")
    icon_image = tk.PhotoImage(file=f"{assets_directory}/icon.png")
    play_blocked_image = tk.PhotoImage(file=f"{assets_directory}/play_blocked.png")

    # Set window size
    window_width = 600
    window_height = 500

    # Create canvas
    main_canvas = tk.Canvas(root, bg=background_color, highlightthickness=0)

    # Create scrollbar
    bar = tk.Scrollbar(root, command=main_canvas.yview, orient=tk.VERTICAL)

    # Configure canvas and scroll
    bar.pack(side=tk.LEFT, fill=tk.Y)
    main_canvas.pack(fill=tk.BOTH, expand=True)
    main_canvas.configure(yscrollcommand=bar.set)

    # Create widgets
    exit_button = tk.Button(root, text="Return", cursor="hand2", bg="red", font=("helvetica", 12, "bold"), command=root.destroy)
    exit_button.place(x=window_width*1, y=window_height*0, anchor=tk.NE)

    # Create art
    main_canvas.create_rectangle(window_width*0, window_height*0, window_width*1, window_height*0.1, fill=foreground_color)
    main_canvas.create_rectangle(window_width*0, window_height*0, window_width*0.18, window_height*1, fill=foreground_color)
    main_canvas.create_text(window_width*0.01, window_height*0.025, text="Versions", fill="white", anchor=tk.NW, font=("Ubuntu-Bold", (18)))
    main_canvas.create_rectangle(0, 1000, 10, 10010, fill="white")

    # Make canvas scrollable
    main_canvas.configure(scrollregion=main_canvas.bbox(tk.ALL))

    # Configure windows
    root.resizable(0, 0)
    root.title("Minecraft Python Launcher")
    root.iconphoto(False, icon_image) 
    root.geometry(f"{window_width}x{window_height}+{parent_root.winfo_x()+25}+{parent_root.winfo_y()+25}")
    root.mainloop()

# Start
if __name__ == "__main__":
    # Create root
    root = tk.Tk()

    # Set colors
    background_color = rgbtohex(62, 62, 62)
    active_color = rgbtohex(62, 62, 62)
    foreground_color = rgbtohex(33, 33, 33)

    # Load images
    menu_image = tk.PhotoImage(file=f"{assets_directory}/menu.png")
    play_image = tk.PhotoImage(file=f"{assets_directory}/play.png")
    home_image = tk.PhotoImage(file=f"{assets_directory}/home.png")
    icon_image = tk.PhotoImage(file=f"{assets_directory}/icon.png")
    play_blocked_image = tk.PhotoImage(file=f"{assets_directory}/play_blocked.png")

    # Set window size
    window_width = 600
    window_height = 500

    # Create tk vars
    selected_installation = tk.StringVar(root)
    if len(installations) == 0:
        no_versions = True
        installations = ["No Versions"]
    else:
        no_versions = False
    selected_installation.set(installations[-1])
    
    # Create canvas
    main_canvas = tk.Canvas(root, bg=background_color, highlightthickness=0)
    main_canvas.pack(fill=tk.BOTH, expand=True)

    # Create widgets
    play_button = tk.Button(root, image=play_blocked_image, cursor="hand2", activebackground=active_color, bg=background_color, fg=foreground_color, borderwidth=0)
    play_button.place(x=window_width*0.5, y=window_height*0.7, anchor=tk.CENTER)

    installation_options = tk.OptionMenu(root, selected_installation, *installations)
    installation_options.config(anchor=tk.W, indicatoron=0, image=menu_image, activebackground=active_color, bg=background_color, fg="white", compound="left", font=("calibri", (11)), highlightthickness=0, width=125, height=20)
    installation_options.place(x=window_width*0.01, y=window_height*0.74, anchor=tk.W)

    version_manager_button = tk.Button(root, text="Version Manager", cursor="hand2", activebackground=active_color, bg=background_color, fg="white", pady=4.5, command=lambda: version_manager(root))
    version_manager_button.place(x=window_width*0.99, y=window_height*0.74, anchor=tk.E)

    # Create art
    main_canvas.create_rectangle(window_width*0, window_height*0.7, window_width*1, window_height*0.78, fill=foreground_color)
    main_canvas.create_image(window_width*0, window_height*0, anchor=tk.NW, image=home_image)

    # Finish setting up
    if not no_versions:
        play_button.config(image=play_image, command=lambda: launch(f"{installations_directory}/{selected_installation.get()}"))

    # Configure window
    root.resizable(0, 0)
    root.title("Minecraft Python Launcher")
    root.iconphoto(False, icon_image) 
    root.geometry(f"{window_width}x{window_height}")
    root.mainloop()