#! /usr/bin/python3 -OOt

# Linux-File-Converter-Addon - Converting files from context menu
# Copyright (C) 2025  Linus Tibert
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


# --- Version number ---
converter_version = "001003009" # Change the number if you want to trigger an update.
# --- Variable to enable debug mode ---
debug_mode = False

# --- Make system imports ---
import sys
import os
from pathlib import Path
from traceback import format_exc

# --- Get config directory and commandline args ---
configuration_file = "~/.config/linux-file-converter-addon/config.json"
configuration_file = str(Path(configuration_file).expanduser())
config_directory = Path(configuration_file).parent
sys_arguments = sys.argv[1:len(sys.argv)]

if len(sys_arguments) >= 1:
    # --- Create application data location and download dependencies ---
    def copyright_notice():
        print("Linux-File-Converter-Addon  Copyright (C) 2025  Linus Tibert\nThis program comes with ABSOLUTELY NO WARRANTY.\nThis is free software, and you are welcome to redistribute it\nunder certain conditions; run with `--license' for details.")
    if sys_arguments[0] == "--license":
        os.system("xdg-open https://github.com/Lich-Corals/linux-file-converter-addon/blob/main/LICENSE & disown")
        exit()
    if sys_arguments[0] == "--create-venv":
        def status_print(string):
            print(f"VENV-CREATION: {string}")
        copyright_notice()
        if len(sys_arguments) >= 2 and sys_arguments[1] != "--full":
            status_print("Usage: nautilus-file-converter.py --create-venv (--full)\n              Optionally add the '--full' option to get additional format support.")
            exit()
        sys_arguments.append("idontwanttocheckforlengthagainsoiaddanotherargumenttoavoiderrors-argument™")
        status_print("Looking for directories...")
        if not os.path.isdir(config_directory) and os.access(config_directory, os.W_OK):
            os.system(f'mkdir "{config_directory}"')
            status_print(f"Created {config_directory}")
        elif not os.access(config_directory, os.W_OK):
            status_print(f"ERROR: No write access in {Path(config_directory).parent} - Aborting.")
            exit()
        if os.access(config_directory, os.W_OK):
            status_print(f"Setting up venv...")
            result = os.system(f'python3 -m venv "{config_directory}/venv"')
            if result != 0:
                result = os.system(f'python -m venv "{config_directory}/venv"')
                if result != 0:
                    status_print(f"ERROR: Something went wrong creating the venv. Check output above. Aborting.")
                    exit()
            status_print(f"Installing dependencies...")
            result = os.system(f'{config_directory}/venv/bin/pip install python-magic Pillow ')
            if result != 0:
                status_print("ERROR: Pip didn't run as expected. Aborting.")
                exit()
            else:
                status_print("Done.")
            if sys_arguments[1] == "--full":
                status_print("Installing optional dependencies...")
                dependencies = ["pillow-heif", "pillow-avif-plugin", "jxlpy"]
                failed = 0
                for dependency in dependencies:
                    result = os.system(f'{config_directory}/venv/bin/pip install {dependency}')
                    if result != 0:
                        failed += 1
                if failed != 0:
                    status_print(f"WARNING: Installed {len(dependencies)-failed} out of {len(dependencies)} optional dependencies successfully. This means the installation of {failed} of them has failed and thus {failed} format(s) will not be available unless you install the dependency manually. You can directly install the module(s) into the venv in {config_directory} to make them available to this program. Check the output above for more information about the problem(s).")
                else:
                    status_print(f"All {len(dependencies)} optional dependencies installed.")
            status_print("The venv is ready for use now. You can run Nautilus or one of the adaption file viewers now to use the extension. (If all non-pip dependencies are installed.)")
            exit()
        else:
            status_print(f"ERROR: No write acces in {config_directory} - Aborting.")
            exit()
    # --- Install self for ? ---
    if "--install-for-" in sys_arguments[0]:
        def status_print(string):
            print(f"SELF-INSTALLATION: {string}")
        copyright_notice()
        installation_targets = {}
        path_nautilus = os.path.expanduser("~/.local/share/nautilus-python/extensions/linux-file-converter-addon.py")
        path_nemo = os.path.expanduser("~/.local/share/nemo/actions/nautilus-fileconverter.py")
        path_thunar = os.path.expanduser("~/.local/bin/linux-file-converter-addon.py")
        match sys_arguments[0]:
            case "--install-for-nautilus":
                installation_targets = {"nautilus": path_nautilus}
            case "--install-for-nemo":
                installation_targets = {"nemo": path_nemo}
            case "--install-for-thunar":
                installation_targets = {"thunar": path_thunar}
            case "--install-for-all":
                installation_targets = {"nautilus": path_nautilus, "nemo": path_nemo, "thunar": path_thunar}
            case _:
                status_print(f"""{sys_arguments[0].replace("--install-for-", "")} not supported. Use "nautilus", "nemo", "thunar" or "all" instead.""")
                exit()
        status_print("Downloading data...")
        from urllib import request
        import stat
        downloaded_self = ""
        try:
            with request.urlopen("https://raw.githubusercontent.com/Lich-Corals/linux-file-converter-addon/main/nautilus-fileconverter.py") as f:
                downloaded_self = f.read().decode().strip()
        except:
            status_print(f"{format_exc()}\nERROR: Can't download the file. Aborting.")
            exit()
        for target in installation_targets:
            installation_target = target
            installation_path = installation_targets[target]
            try: 
                status_print(f"Creating directory for {target}...")
                os.makedirs(Path(installation_path).parent, exist_ok=True)
                status_print(f"Creating file for {target}...")
                with open(installation_path, 'w') as f:
                    f.write(downloaded_self)
                    f.close()
            except:
                status_print(f"{format_exc()}\nERROR: Something went wrong while creating the new file or path. Aborting.")
                exit()
            status_print(f"Finalizing {target}...")
            match installation_target:
                case "nautilus":
                    status_print("Killing nautilus...")
                    os.system("nautilus -q")
                case "nemo":
                    status_print("Downloading nemo_action...")
                    nemo_action = ""
                    try:
                        with request.urlopen("https://raw.githubusercontent.com/Lich-Corals/linux-file-converter-addon/main/nautilus-fileconverter.nemo_action") as f:
                            nemo_action = f.read().decode().strip()
                    except:
                        status_print(f"{format_exc()}\nERROR: Can't download nemo_action file. Aborting.")
                        exit()
                    status_print("Writing nemo_action...")
                    with open(f"{Path(installation_path).parent}/linux-file-converter.nemo_action", 'w') as f:
                        f.write(nemo_action)
                        f.close()
                    status_print("Updating script permissions...")
                    os.chmod(installation_path, os.stat(installation_path).st_mode | stat.S_IEXEC)
                case "thunar":
                    status_print("Updating script permissions...")
                    os.chmod(installation_path, os.stat(installation_path).st_mode | stat.S_IEXEC)
                    status_print(f"Used this path for thunar installation: {installation_path}")
        status_print("Installation successfull. Consider taking a look at the configuration of the extension: https://github.com/Lich-Corals/linux-file-converter-addon/blob/main/markdown/configuration.md")
        exit()

# --- Add modules installed in venv to path ---
if os.path.isdir(f"{config_directory}/venv"):
    lib_path = f"""{config_directory}/venv/lib/{os.listdir(f"{config_directory}/venv/lib/")[0]}/site-packages"""
    sys.path.insert(0, lib_path)
    if debug_mode:
        print(f"INFO(Nautilus-file-converter): Added {lib_path} to system path to access modules.")

# --- Main imports ---
import gi
if len(sys.argv) > 1:
    gi.require_version("Gtk", "3.0")
    from gi.repository import Gtk, Gdk
    from magic import Magic
    import ast

    # --- Create magic object... a magic wand or something like it ---
    magic_object = Magic(mime=True)
else:
    gi.require_version("Gtk", "4.0")
    from gi.repository import Gtk, GObject, Nautilus
    from typing import List
from PIL import Image, UnidentifiedImageError
from urllib.parse import urlparse, unquote
from urllib import request
from datetime import datetime
import os, shlex
import json
import re
from multiprocessing import Process

# --- Get the path to the script and check if it's writeable ---
application_path = str(Path(__file__).parent.resolve())  # used for config file and self-update!
permission_to_update = os.access(f"{application_path}/{os.path.basename(__file__)}", os.W_OK)

# --- Check if dependencies are installed and imported ---
pillow_heif_installed = False
jxlpy_installed = False
pillow_avif_plugin_installed = False

try:
    from pillow_heif import register_heif_opener
    register_heif_opener()
    pillow_heif_installed = True
except ImportError:
    pillow_heif_installed = False
    print(f"WARNING(Nautilus-file-converter)(100): \"pillow_heif\" not found. View https://github.com/Lich-Corals/linux-file-converter-addon/blob/main/markdown/errors-and-warnings.md for more information." )

try:
    from jxlpy import JXLImagePlugin
    jxlpy_installed = True
except ImportError:
    jxlpy_installed = False
    print(f"WARNING(Nautilus-file-converter)(101): \"jxlpy\" not found. View https://github.com/Lich-Corals/linux-file-converter-addon/blob/main/markdown/errors-and-warnings.md for more information.")

try:
    import pillow_avif
    pillow_avif_plugin_installed = True
except ImportError:
        print(f"WARNING(Nautilus-file-converter)(102) \"pillow-avif-plugin\" not found. View https://github.com/Lich-Corals/linux-file-converter-addon/blob/main/markdown/errors-and-warnings.md for more information.")

if not permission_to_update:
    print(f"ERROR(Nautilus-file-converter)(402): No permission to self-update; script at \"{application_path}/{os.path.basename(__file__)}\" is not writeable. View https://github.com/Lich-Corals/linux-file-converter-addon/blob/main/markdown/errors-and-warnings.md for more information.")

# --- Set default configs ---
config_preset = {                                 # These are the default settings and will reset with each update; edit ~/.config/linux-file-converter-addon/config.json if the program has permission to read and write it.
    "automaticUpdates": True,
    "showPatchNotes": True,
    "showPatchNoteButton": True,
    "showConfigHint": True,
    "convertToSquares": True,
    "convertToWallpapers": True,
    "checkForDoubleInstallation": True,
    "timeInNames": True,
    "convertFromOctetStream": False,
    "showDummyOption": True,
    "displayFinishNotification": True
}

# --- Move settings from old config file to new location if the old one exists ---
if not os.path.isdir(config_directory):
    os.system(f'mkdir "{config_directory}"')
if Path(f"{application_path}/NFC43-Config.json").is_file() and os.access(f"{application_path}/NFC43-Config.json", os.W_OK):
    with open(f"{application_path}/NFC43-Config.json", 'r') as file:
        try:
            old_config = json.load(file)
        except json.decoder.JSONDecodeError:
            old_config = config_preset
        file.close()
    config_preset = old_config.copy()
    with open(f"{application_path}/NFC43-Config.json", 'w') as old_config_file:
        old_config["comment"] = f"THIS FILE DOES NOT CONFIGURE ANYTHING ANYMORE. USE {configuration_file} INSTEAD!"
        old_config = json.dumps(old_config, indent=4)
        old_config_file.write(old_config)
        old_config_file.close()
    os.system(f'mv "{application_path}/NFC43-Config.json" "{application_path}/NFC43-Config.json.DISABLED"')
    os.system(f'notify-send --app-name="linux-file-converter-addon" "Config file moved." "Your new config file is here:\n{config_directory}"')
user_configuration = config_preset

# --- Load or store configs json ---
if os.access(config_directory, os.W_OK):
    try:
        if Path(configuration_file).is_file():
            with open(configuration_file, 'r') as file:
                try:
                    loaded_json = json.load(file)
                except json.decoder.JSONDecodeError:
                    loaded_json = config_preset
                user_configuration = loaded_json
            for setting in config_preset:
                if setting not in user_configuration:
                    user_configuration[setting] = config_preset[setting]
            loaded_json = json.dumps(user_configuration, indent=4)
        else:
            loaded_json = json.dumps(config_preset, indent=4)
        with open(configuration_file, "w") as file:
            file.write(loaded_json)
    except:
        print("ERROR(Nautilus-file-converter)(401): Something went wrong while loading or updating the configuration file.")
        print(f"{format_exc()}")
else:
    print(f"ERROR(Nautilus-file-converter)(403): No permission to write configuration file; \"{config_directory}\" is not writeable. View https://github.com/Lich-Corals/linux-file-converter-addon/blob/main/markdown/errors-and-warnings.md for more information.")

# --- Check for updates and update if auto-update is enabled ---
if user_configuration["automaticUpdates"]:
    with request.urlopen("https://raw.githubusercontent.com/Lich-Corals/linux-file-converter-addon/main/nautilus-fileconverter.py") as f:
        downloaded_data = f.read().decode().strip()
    if converter_version not in downloaded_data:
        print(f"UPDATES(Nautilus-file-converter)(104): Current Version: {converter_version}\n"
              f"                                       Attempting to update...")
        if permission_to_update:
            print("Updating...")
            application_file_location = f"{application_path}/{os.path.basename(__file__)}"
            if user_configuration["showPatchNotes"]:
                #os.system(f"nohup xdg-open \"https://github.com/Lich-Corals/linux-file-converter-addon/blob/main/markdown/update-notification.md\" &")
                os.system('notify-send --app-name="linux-file-converter-addon" "Update installed." "More info: https://github.com/Lich-Corals/linux-file-converter-addon/blob/main/markdown/update-notification.md"')
            with open(application_file_location, 'w') as file:
                file.write(downloaded_data)

# --- Check for duplicate script if enabled ---
if user_configuration["checkForDoubleInstallation"] and "/.local/share/" in application_path and os.path.isfile("/usr/share/nautilus-python/extensions/nautilus-fileconverter.py"):
    print(f"WARNING(Nautilus-file-converter)(103): Double script installation detected. View https://github.com/Lich-Corals/linux-file-converter-addon/blob/main/markdown/errors-and-warnings.md for more information.")

# --- Check for development status and apply settings ---
if not debug_mode:
    print = lambda *wish, **verbosity: None

print(f"pyheif: {pillow_heif_installed}\njxlpy: {jxlpy_installed}\npillow_avif: {pillow_avif_plugin_installed}")

# --- Create file format tuples and write format dict-lists? ---
READ_FORMATS_IMAGE = ('image/jpeg',
                      'image/png',
                      'image/bmp',
                      'application/postscript',
                      'image/gif',
                      'image/x-icon',
                      'image/x-pcx',
                      'image/x-portable-pixmap',
                      'image/tiff',
                      'image/x-xbm',
                      'image/x-xbitmap',
                      'video/fli',
                      'image/vnd.fpx',
                      'image/vnd.net-fpx',
                      'windows/metafile',
                      'image/x-xpixmap',
                      'image/webp')

READ_FORMATS_PYHEIF = ('image/avif',
                     'image/heif',
                     'image/heic')

READ_FORMATS_JXLPY = ('image/jxl')

READ_FORMATS_AUDIO = ('audio/mpeg',
                      'audio/mpeg3',
                      'video/x-mpeg',
                      'audio/x-mpeg-3',
                      'audio/x-wav',
                      'audio/wav',
                      'audio/wave',
                      'audio/x-pn-wave',
                      'audio/vnd.wave',
                      'audio/x-mpegurl',
                      'audio/mp4',
                      'audio/mp4a-latm',
                      'audio/mpeg4-generic',
                      'audio/x-matroska',
                      'audio/aac',
                      'audio/aacp',
                      'audio/3gpp',
                      'audio/3gpp2',
                      'audio/ogg',
                      'audio/opus',
                      'audio/flac',
                      'audio/x-vorbis+ogg')

READ_FORMATS_VIDEO = ('video/mp4',
                      'video/webm',
                      'video/x-matroska',
                      'video/avi',
                      'video/msvideo',
                      'video/x-msvideo',
                      'video/quicktime')

OCTET_STREAM_FORMATS = ('application/octet-stream',)

WRITE_FORMATS_IMAGE = [{'name': 'PNG'},
                       {'name': 'JPEG'},
                       {'name': 'BMP'},
                       {'name': 'GIF'},
                       {'name': 'WebP'},
                       {'name': 'TIFF'}]

WRITE_FORMATS_JXLPY = [{'name': 'JXL'}]

WRITE_FORMATS_AVIF = [{ 'name': 'AVIF'}]

WRITE_FORMATS_SQUARE = [{'name': 'PNG: 16x16', 'extension': 'png', 'square': '16'},
                        {'name': 'PNG: 32x32', 'extension': 'png', 'square': '32'},
                        {'name': 'PNG: 64x64', 'extension': 'png', 'square': '64'},
                        {'name': 'PNG: 128x128', 'extension': 'png', 'square': '128'},
                        {'name': 'PNG: 256x256', 'extension': 'png', 'square': '256'},
                        {'name': 'PNG: 512x512', 'extension': 'png', 'square': '512'},
                        {'name': 'PNG: 1024x1024', 'extension': 'png', 'square': '1024'},
                        {'name': 'JPEG: 16x16', 'extension': 'JPEG', 'square': '16'},
                        {'name': 'JPEG: 32x32', 'extension': 'JPEG', 'square': '32'},
                        {'name': 'JPEG: 64x64', 'extension': 'JPEG', 'square': '64'},
                        {'name': 'JPEG: 128x128', 'extension': 'JPEG', 'square': '128'},
                        {'name': 'JPEG: 256x256', 'extension': 'JPEG', 'square': '256'},
                        {'name': 'JPEG: 512x512', 'extension': 'JPEG', 'square': '512'},
                        {'name': 'JPEG: 1024x1024', 'extension': 'JPEG', 'square': '1024'}]

WRITE_FORMATS_WALLPAPER = [{'name': 'SD P | 480x640', 'extension': 'png', 'w': '480', 'h': '640'},
                           {'name': 'SD L | 640x480', 'extension': 'png', 'w': '640', 'h': '480'},
                           {'name': 'HD P | 720x1280', 'extension': 'png', 'w': '720', 'h': '1280'},
                           {'name': 'HD L | 1280x720', 'extension': 'png', 'w': '1280', 'h': '720'},
                           {'name': 'FHD P | 1080x1920', 'extension': 'png', 'w': '1080', 'h': '1920'},
                           {'name': 'FHD L | 1920x1080', 'extension': 'png', 'w': '1920', 'h': '1080'},
                           {'name': 'QHD P | 1440x2560', 'extension': 'png', 'w': '1440', 'h': '2560'},
                           {'name': 'QHD L | 2560x1440', 'extension': 'png', 'w': '2560', 'h': '1440'},
                           {'name': '4K-UHD P | 2160x3840', 'extension': 'png', 'w': '2160', 'h': '3840'},
                           {'name': '4K-UHD L | 3840x2160', 'extension': 'png', 'w': '3840', 'h': '2160'},
                           {'name': '8K-UHD P | 4320x7680', 'extension': 'png', 'w': '4320', 'h': '7680'},
                           {'name': '8K-UHD L | 7680x4320', 'extension': 'png', 'w': '7680', 'h': '4320'},
                           {'name': 'Galaxy S7 P | 1440x2960', 'extension': 'png', 'w': '1440', 'h': '2960'},
                           {'name': 'Galaxy S7 L | 1440x2960', 'extension': 'png', 'w': '2960', 'h': '1440'},
                           {'name': 'iPad Pro P | 2048x2732', 'extension': 'png', 'w': '2048', 'h': '2732'},
                           {'name': 'iPad Pro L | 2048x2732', 'extension': 'png', 'w': '2732', 'h': '2048'}]

WRITE_FORMATS_AUDIO = [{'name': 'MP3'},
                       {'name': 'WAV'},
                       {'name': 'AAC'},
                       {'name': 'FLAC'},
                       {'name': 'M4A'},
                       {'name': 'OGG'},
                       {'name': 'OPUS'}]

WRITE_FORMATS_VIDEO = [{'name': 'MP4'},
                       {'name': 'WebM'},
                       {'name': 'MKV'},
                       {'name': 'AVI'},
                       {'name': 'MP3'},
                       {'name': 'WAV'}]

if user_configuration["convertFromOctetStream"]:
    READ_FORMATS_IMAGE = READ_FORMATS_IMAGE + OCTET_STREAM_FORMATS

if pillow_heif_installed:
    READ_FORMATS_IMAGE = READ_FORMATS_IMAGE + READ_FORMATS_PYHEIF

if jxlpy_installed:
    READ_FORMATS_IMAGE = READ_FORMATS_IMAGE + (READ_FORMATS_JXLPY,)
    WRITE_FORMATS_IMAGE.extend(WRITE_FORMATS_JXLPY)

if pillow_avif_plugin_installed:
    WRITE_FORMATS_IMAGE.extend(WRITE_FORMATS_AVIF)

# --- Function used to get a mimetype's extension ---
def get_format_extension(file_format):
    return f".{file_format.get('extension', file_format['name'])}".lower()

# --- Function used to remove old timestamp ---
def remove_timestamp(file_path_stem):
    clean_stem = re.sub(r'\d{4}(-\d{2}){5}', "", file_path_stem)
    return clean_stem

def name_addition():
    if user_configuration["timeInNames"]:
        return datetime.today().strftime('%Y-%m-%d-%H-%M-%S')
    else:
        return ""

def finish_conversion(conversion_results):
    if user_configuration["displayFinishNotification"]:
        os.system(f'notify-send --app-name="linux-file-converter-addon" "Conversion finished" "Successfull: {conversion_results["success"]}\nFailed: {conversion_results["fail"]}"')

# --- Function to convert between image formats ---
def convert_images(*args, **kwargs):
    menu = kwargs["menu"]
    file_format = kwargs["format"]
    files = kwargs["files"]
    conversion_results = {"success": 0, "fail": 0}
    for file in files:
        if 'extension' not in file_format:
            file_format['extension'] = file_format['name']
        if str(type(file)) == "<class '__gi__.NautilusVFSFile'>":
            from_file_path = Path(unquote(urlparse(file.get_uri()).path))
        else:
            from_file_path = file
        print(remove_timestamp(from_file_path.stem) + from_file_path.stem)
        to_file_path = from_file_path.with_name(f"{remove_timestamp(from_file_path.stem)}{name_addition()}.{file_format['extension'].lower()}")
        try:
            image = Image.open(from_file_path)
            image_open_error = False
            conversion_results["success"] += 1
        except UnidentifiedImageError:
            print(f"(Nautilus-file-converter)(400): {from_file_path} is in an unconvertable file-format.")
            image_open_error = True
            conversion_results["fail"] += 1
        if not image_open_error:
            if (file_format['name']) == 'JPEG':
                image = image.convert('RGB')
            if 'square' in file_format:
                image = image.resize((int(file_format['square']), int(file_format['square'])))
            if 'w' in file_format:
                image = image.resize((int(file_format['w']), int(file_format['h'])))
            image.save(to_file_path, format=(file_format['extension']))
    finish_conversion(conversion_results)

# --- Function to convert using FFMPEG (video and audio) ---
def convert_ffmpeg_media(*args, **kwargs):
    menu = kwargs["menu"]
    file_format = kwargs["format"]
    files = kwargs["files"]
    global get_format_extension
    conversion_results = {"success": 0, "fail": 0}
    for file in files:
        if str(type(file)) == "<class '__gi__.NautilusVFSFile'>":
            from_file_path = Path(unquote(urlparse(file.get_uri()).path))
        else:
            from_file_path = file
        to_file_path = from_file_path.with_name(f"{remove_timestamp(from_file_path.stem)}{name_addition()}{get_format_extension(file_format).lower()}")
        command_result = os.system(f"ffmpeg -i {shlex.quote(str(from_file_path))} -strict experimental -c:v libvpx-vp9 -crf 18 -preset slower -b:v 4000k {shlex.quote(str(to_file_path))}")
        if command_result == 0:
            conversion_results["success"] += 1
        else:
            conversion_results["fail"] += 1
    finish_conversion(conversion_results)

# --- Function to start image conversion in a new subprocess ---
def start_image_conversion(menu, format_, files):
    subprocess = Process(target=convert_images, kwargs={"menu":menu, "format": format_, "files": files})
    subprocess.start()

# --- Function to start ffmpeg conversion in a new subprocess ---
def start_ffmpeg_conversion(menu, format_, files):
    subprocess = Process(target=convert_ffmpeg_media, kwargs={"menu":menu, "format": format_, "files": files})
    subprocess.start()

# --- Adaption class ---
class LinuxFileConverterWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title=f"Convert file")
        self.set_border_width(15)
        self.set_default_size(200, 20)
        self.set_resizable(False)

        self.connect("key-press-event",self.on_key_press_event)

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)

        label = Gtk.Label(label="Select a format:")
        label.set_justify(Gtk.Justification.CENTER)
        vbox.pack_start(label, False, False, 0)
        version_information_label = Gtk.Label()
        version_information_label.set_markup(f"""<span size="x-small">version {converter_version}</span>""")
        version_information_label.set_justify(Gtk.Justification.CENTER)
        configuration_hint_label = Gtk.Label()
        configuration_hint_label.set_justify(Gtk.Justification.CENTER)
        configuration_hint_label.set_markup(f"""<span size="x-small">View <a href="https://github.com/Lich-Corals/linux-file-converter-addon/blob/main/markdown/configuration.md">the config documentation</a>\nto configure the script and hide this text.</span>""")

        copyright_notice_label = Gtk.Label()
        copyright_notice_label.set_justify(Gtk.Justification.CENTER)
        copyright_notice_label.set_markup(f"""<span color="#696969" size="x-small">Linux-File-Converter-Addon  Copyright (C) 2025  Linus Tibert\nunder the <a href="https://github.com/Lich-Corals/linux-file-converter-addon/blob/main/LICENSE">GNU Affero General Public License</a>.</span>""")

        extensions = Gtk.ListStore(str, str, int)
        only_images_selected = True
        only_audios_selected = True
        only_videos_selected = True
        for argument in sys_arguments:
            if not magic_object.from_file(argument) in READ_FORMATS_IMAGE:
                only_images_selected = False
            if not magic_object.from_file(argument) in READ_FORMATS_AUDIO:
                only_audios_selected = False
            if not magic_object.from_file(argument) in READ_FORMATS_VIDEO:
                only_videos_selected = False

        if user_configuration["showDummyOption"]:
            extensions.append(["-", "none", 2])

        if only_images_selected:
            for selected_write_format in WRITE_FORMATS_IMAGE:
                print(selected_write_format)
                extensions.append([selected_write_format['name'], str(selected_write_format), 0])
            if user_configuration["convertToSquares"]:
                for selected_write_format in WRITE_FORMATS_SQUARE:
                    extensions.append([selected_write_format['name'], str(selected_write_format), 0])
            if user_configuration["convertToWallpapers"]:
                for selected_write_format in WRITE_FORMATS_WALLPAPER:
                    extensions.append([selected_write_format['name'], str(selected_write_format), 0])
        if only_audios_selected:
            for selected_write_format in WRITE_FORMATS_AUDIO:
                extensions.append([selected_write_format['name'], str(selected_write_format), 1])
        if only_videos_selected:
            for selected_write_format in WRITE_FORMATS_VIDEO:
                extensions.append([selected_write_format['name'], str(selected_write_format), 1])

        self.add(vbox)
        combo_box = Gtk.ComboBox.new_with_model(extensions)
        renderer_text = Gtk.CellRendererText()
        combo_box.set_entry_text_column(0)
        combo_box.pack_start(renderer_text, True)
        combo_box.add_attribute(renderer_text, "text", 0)
        combo_box.connect("changed", self.start_conversion)
        vbox.pack_start(combo_box, False, False, 0)
        if user_configuration["showPatchNoteButton"]:
            vbox.pack_start(version_information_label, False, False, 0)
        if user_configuration["showConfigHint"]:
            vbox.pack_start(configuration_hint_label, True, True, 0)
        vbox.pack_start(copyright_notice_label, True, True, 0)

    def start_conversion(self, combo):
        tree_iter = combo.get_active_iter()
        if tree_iter is not None:
            model = combo.get_model()
            return_name, return_format, return_type = model[tree_iter][:4]
            print(return_name, return_format, return_type)
            return_format = ast.literal_eval(return_format)
            return_paths = []
            if not return_type == 2:
                self.hide()
                for retun_path in sys_arguments:
                    return_paths.append(Path(retun_path))
                if return_type == 0:
                    start_image_conversion(self, return_format, return_paths)
                elif return_type == 1:
                    start_ffmpeg_conversion(self, return_format, return_paths)

    def on_key_press_event(self, widget, event):
        print(f"Key pressed: {event.keyval}")
        if event.keyval == 65307:
            exit()

# --- Generate nemo_action ---
if len(sys.argv) > 1:
    print(f"Args: {str(sys_arguments)} \nPath:{application_path}")
    if ".local/bin" not in application_path:
        nemo_read_formats = ""
        global_read_formats = READ_FORMATS_IMAGE + READ_FORMATS_AUDIO + READ_FORMATS_VIDEO
        for media_format in global_read_formats:
            if media_format not in nemo_read_formats:
                nemo_read_formats += media_format + ";"
        nemo_action_lines = ["[Nemo Action]",
                            "Name=Convert to...",
                            "Comment=Convert file using nautilus-fileconverter",
                            "Exec=<nautilus-fileconverter.py %F>",
                            "Selection=NotNone",
                            f"Mimetypes={nemo_read_formats}"]
        with open(f"{application_path}/nautilus-fileconverter.nemo_action", "w") as file:
            for line in nemo_action_lines:
                file.write(line + "\n")
            file.close()
    
    gtk_popup_window_object = LinuxFileConverterWindow()
    gtk_popup_window_object.connect("destroy", Gtk.main_quit)
    gtk_popup_window_object.show_all()
    Gtk.main()

# --- Nautilus class ---
class LinuxFileConverterMenuProvider(GObject.GObject, Nautilus.MenuProvider):
    # --- Get file mime and trigger submenu building ---
    def get_file_items(self, *args) -> List[Nautilus.MenuItem]:
        files = args[-1]
        for file in files:
            print(file.get_mime_type())
            file_mime = file.get_mime_type()
            if file_mime in READ_FORMATS_IMAGE or file_mime == 'application/octet-stream':
                return self.submenu_builder(WRITE_FORMATS_IMAGE,
                                              callback=start_image_conversion,
                                              files=files)
            if file_mime in READ_FORMATS_AUDIO:
                return self.submenu_builder(WRITE_FORMATS_AUDIO,
                                              callback=start_ffmpeg_conversion,
                                              files=files)
            if file_mime in READ_FORMATS_VIDEO:
                return self.submenu_builder(WRITE_FORMATS_VIDEO,
                                              callback=start_ffmpeg_conversion,
                                              files=files)

    # --- Build the context menu and submenus ---
    def submenu_builder(self, formats, callback, files):
        main_menu_item = Nautilus.MenuItem(                         # Create main-submenu item
            name="LinuxFileConverterMenuProvider::convert_to",
            label="Convert to...",
        )
        main_menu = Nautilus.Menu()                                 # Create Nautilus submenu
        main_menu_item.set_submenu(main_menu)                       # Add the item to the submenu

        for file_format in formats:
            main_menu_sub_item = Nautilus.MenuItem(
                name='LinuxFileConverterMenuProvider::convert_to_' + file_format['name'],
                label=(file_format['name']),
            )
            main_menu_sub_item.connect('activate', callback, file_format, files)
            main_menu.append_item(main_menu_sub_item)               # Append sub item to menu

        if formats[1]['name'] == 'JPEG':
            if user_configuration["convertToSquares"]:
                main_menu_sub_menu_item_squares = Nautilus.MenuItem(
                    name="LinuxFileConverterMenuProvider::square_format_menu",
                    label="Square...",
                )
                main_menu_sub_menu_squares = Nautilus.Menu()
                main_menu_sub_menu_item_squares.set_submenu(main_menu_sub_menu_squares)

                for square_format in WRITE_FORMATS_SQUARE:
                    main_menu_sub_menu_squares_sub_item = Nautilus.MenuItem(
                        name='LinuxFileConverterMenuProvider::square_convert_' + square_format['name'],
                        label=(square_format['name']),
                    )
                    main_menu_sub_menu_squares_sub_item.connect('activate', callback, square_format, files)
                    main_menu_sub_menu_squares.append_item(main_menu_sub_menu_squares_sub_item)
                main_menu.append_item(main_menu_sub_menu_item_squares)

            if user_configuration["convertToWallpapers"]:
                main_menu_sub_menu_item_wallpapers = Nautilus.MenuItem(
                    name="LinuxFileConverterMenuProvider::wallpaper_format_menu",
                    label="Wallpaper...",
                )
                main_menu_sub_menu_wallpapers = Nautilus.Menu()
                main_menu_sub_menu_item_wallpapers.set_submenu(main_menu_sub_menu_wallpapers)

                for wallpaper_formats in WRITE_FORMATS_WALLPAPER:
                    main_menu_sub_menu_wallpapers_sub_item = Nautilus.MenuItem(
                        name='LinuxFileConverterMenuProvider::wallpaper_convert_' + wallpaper_formats['name'],
                        label=(wallpaper_formats['name']),
                    )
                    main_menu_sub_menu_wallpapers_sub_item.connect('activate', callback, wallpaper_formats, files)
                    main_menu_sub_menu_wallpapers.append_item(main_menu_sub_menu_wallpapers_sub_item)
                main_menu.append_item(main_menu_sub_menu_item_wallpapers)

        if user_configuration["showPatchNoteButton"]:
            main_menu_sub_item_patch_notes = Nautilus.MenuItem(
                name="LinuxFileConverterMenuProvider::patch_notes",
                label=f"View patch notes ({converter_version})",
            )
            callback = self.show_patch_notes
            main_menu_sub_item_patch_notes.connect('activate', callback,)
            main_menu.append_item(main_menu_sub_item_patch_notes)

        if user_configuration["showConfigHint"]:
            main_menu_sub_item_show_configuration_page = Nautilus.MenuItem(
                name="LinuxFileConverterMenuProvider::show_configuration_page",
                label=f"Configure LFCA",
            )
            callback = self.openConfigHint
            main_menu_sub_item_show_configuration_page.connect('activate', callback,)
            main_menu.append_item(main_menu_sub_item_show_configuration_page)

        return [main_menu_item]

    # --- openPatchNotes and openConfigHint functions for context menu options ---
    def show_patch_notes(self, menu):
        os.system(f"nohup xdg-open \"https://github.com/Lich-Corals/linux-file-converter-addon/releases\" &")

    def openConfigHint(self, menu):
        os.system(f"nohup xdg-open 'https://github.com/Lich-Corals/linux-file-converter-addon/blob/main/markdown/configuration.md' &")
        os.system(f"nohup xdg-open {configuration_file} &")