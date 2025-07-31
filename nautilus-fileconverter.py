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
CONVERTER_VERSION = "001003009" # Change the number if you want to trigger an update.

# --- Variable to enable debug mode ---
DEBUG_MODE = True

#######
####### AUTO-INSTALLATION SECTION
####### Used for one-liner installation. Only uses minimal imports and logic. MAY NOT HAVE EXTERNAL DEPENDENCIES BESIDES python3 AND pip

# --- Make essential imports ---
import sys
import os
from pathlib import Path
from traceback import format_exc
from enum import Enum

# --- Get config directory and commandline args ---
CONFIGURATION_FILE = "~/.config/linux-file-converter-addon/config.json"
CONFIGURATION_FILE = str(Path(CONFIGURATION_FILE).expanduser())
CONFIGURATION_DIRECTORY = Path(CONFIGURATION_FILE).parent
SYSTEM_ARGUMENTS = sys.argv[1:len(sys.argv)]

# --- Enum to identify a spcific type of installation of the script ---
class InstallationType(Enum):
    NAUTILUS = "nautilus",
    NEMO = "nemo",
    THUNAR = "thunar",
    UNKNOWN = "unknown"

# --- A dict to connect each installation type with a location for the main script ---
INSTALLATION_LOCATIONS =    {InstallationType.NAUTILUS: os.path.expanduser("~/.local/share/nautilus-python/extensions/linux-file-converter-addon.py"),
                            InstallationType.NEMO: os.path.expanduser("~/.local/share/nemo/actions/linux-file-converter-addon.py"),
                            InstallationType.THUNAR: os.path.expanduser("~/.local/bin/linux-file-converter-addon.py")}

if len(SYSTEM_ARGUMENTS) >= 1:
    # --- Show the copyright notice ---
    def copyright_notice():
        print("Linux-File-Converter-Addon  Copyright (C) 2025  Linus Tibert\nThis program comes with ABSOLUTELY NO WARRANTY.\nThis is free software, and you are welcome to redistribute it\nunder certain conditions; run with `--license' for details.")
    # --- Show the license in default browser if asked to ---
    if SYSTEM_ARGUMENTS[0] == "--license":
        from subprocess import Popen
        Popen(["xdg-open", "https://github.com/Lich-Corals/linux-file-converter-addon/blob/main/LICENSE"])
        exit()
    # --- Create a local venv with dependencies ---
    if SYSTEM_ARGUMENTS[0] == "--create-venv":
        def status_print(string):
            print(f"VENV-CREATION: {string}")
        copyright_notice()
        if len(SYSTEM_ARGUMENTS) >= 2 and SYSTEM_ARGUMENTS[1] != "--full":
            status_print("Usage: nautilus-file-converter.py --create-venv (--full)\n              Optionally add the '--full' option to get additional format support.")
            exit()
        SYSTEM_ARGUMENTS.append("idontwanttocheckforlengthagainsoiaddanotherargumenttoavoiderrors-argument™")
        status_print("Looking for directories...")
        if not os.path.isdir(CONFIGURATION_DIRECTORY) and os.access(CONFIGURATION_DIRECTORY, os.W_OK):
            os.system(f'mkdir "{CONFIGURATION_DIRECTORY}"')
            status_print(f"Created {CONFIGURATION_DIRECTORY}")
        elif not os.access(CONFIGURATION_DIRECTORY, os.W_OK):
            status_print(f"ERROR: No write access in {Path(CONFIGURATION_DIRECTORY).parent} - Aborting.")
            exit()
        if os.access(CONFIGURATION_DIRECTORY, os.W_OK):
            status_print(f"Setting up venv...")
            result = os.system(f'python3 -m venv "{CONFIGURATION_DIRECTORY}/venv"')
            if result != 0:
                result = os.system(f'python -m venv "{CONFIGURATION_DIRECTORY}/venv"')
                if result != 0:
                    status_print(f"ERROR: Something went wrong creating the venv. Check output above. Aborting.")
                    exit()
            status_print(f"Installing dependencies...")
            result = os.system(f'{CONFIGURATION_DIRECTORY}/venv/bin/pip install python-magic Pillow ')
            if result != 0:
                status_print("ERROR: Pip didn't run as expected. Aborting.")
                exit()
            else:
                status_print("Done.")
            if SYSTEM_ARGUMENTS[1] == "--full":
                status_print("Installing optional dependencies...")
                dependencies = ["pillow-heif", "pillow-avif-plugin", "jxlpy"]
                failed = 0
                for dependency in dependencies:
                    result = os.system(f'{CONFIGURATION_DIRECTORY}/venv/bin/pip install {dependency}')
                    if result != 0:
                        failed += 1
                if failed != 0:
                    status_print(f"WARNING: Installed {len(dependencies)-failed} out of {len(dependencies)} optional dependencies successfully. This means the installation of {failed} of them has failed and thus {failed} format(s) will not be available unless you install the dependency manually. You can directly install the module(s) into the venv in {CONFIGURATION_DIRECTORY} to make them available to this program. Check the output above for more information about the problem(s).")
                else:
                    status_print(f"All {len(dependencies)} optional dependencies installed.")
            status_print("The venv is ready for use now. You can run Nautilus or one of the adaption file viewers now to use the extension. (If all non-pip dependencies are installed.)")
            exit()
        else:
            status_print(f"ERROR: No write acces in {CONFIGURATION_DIRECTORY} - Aborting.")
            exit()

    # --- Install linux-file-converter-addon for selected file manager(s) ---
    if "--install-for-" in SYSTEM_ARGUMENTS[0]:
        # --- Find out which InstallationTypes should be installed ---
        def status_print(string):
            print(f"SELF-INSTALLATION: {string}")
        copyright_notice()
        installation_targets = {}
        for installation_location in INSTALLATION_LOCATIONS:
            print(installation_location.value[0])
            if SYSTEM_ARGUMENTS[0] == f"--install-for-{installation_location.value[0]}":
                installation_targets[installation_location] = INSTALLATION_LOCATIONS[installation_location]
        if SYSTEM_ARGUMENTS[0] == "--install-for-all":
            installation_targets = INSTALLATION_LOCATIONS
        if installation_targets == {}:
            status_print(f"""{SYSTEM_ARGUMENTS[0].replace("--install-for-", "")} not supported. Use "nautilus", "nemo", "thunar" or "all" instead.""")
            exit()
        # --- Perform the basic script installation ---
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
            # --- InstallationType specific actions ---
            match installation_target:
                case InstallationType.NAUTILUS:
                    status_print("Killing nautilus...")
                    os.system("nautilus -q")
                case InstallationType.NEMO:
                    status_print("Downloading nemo_action...")
                    nemo_action = ""
                    try:
                        with request.urlopen("https://raw.githubusercontent.com/Lich-Corals/linux-file-converter-addon/main/nautilus-fileconverter.nemo_action") as f:
                            nemo_action = f.read().decode().strip()
                    except:
                        status_print(f"{format_exc()}\nERROR: Can't download nemo_action file. Aborting.")
                        exit()
                    status_print("Writing nemo_action...")
                    with open(f"{Path(installation_path).parent}/linux-file-converter-addon.nemo_action", 'w') as f:
                        f.write(nemo_action.replace("Exec=<nautilus-fileconverter.py %F>", "Exec=<linux-file-converter-addon.py %F>"))
                        f.close()
                    status_print("Updating script permissions...")
                    os.chmod(installation_path, os.stat(installation_path).st_mode | stat.S_IEXEC)
                case InstallationType.THUNAR:
                    status_print("Updating script permissions...")
                    os.chmod(installation_path, os.stat(installation_path).st_mode | stat.S_IEXEC)
                    status_print(f"Used this path for thunar installation: {installation_path}")
        status_print("Installation successfull. Consider taking a look at the configuration of the extension: https://github.com/Lich-Corals/linux-file-converter-addon/blob/main/markdown/configuration.md")
        exit()

#######
####### SELF-PREPARATION SECTION
####### Used to prepare the script for running. Mostly imports and definition of GLOBAL_CONSTANTS

#######
####### SELF-PREPARATION SECTION  --  SYSTEM
####### Imports, determining system conditions

# --- Add modules installed in local venv to path ---
if os.path.isdir(f"{CONFIGURATION_DIRECTORY}/venv"):
    lib_path = f"""{CONFIGURATION_DIRECTORY}/venv/lib/{os.listdir(f"{CONFIGURATION_DIRECTORY}/venv/lib/")[0]}/site-packages"""
    sys.path.insert(0, lib_path)
    if DEBUG_MODE:
        print(f"INFO(Nautilus-file-converter): Added {lib_path} to system path to access modules.")

# --- Main imports ---
import gi
from PIL import Image, UnidentifiedImageError
from urllib.parse import urlparse, unquote
from urllib import request
from datetime import datetime
import os, shlex
import json
import re
from multiprocessing import Process
# --- Imports vary if the program is started with arguments (for the adaption version) ---
#     Also, Gtk3 is imported instead of Gtk4 if there are arguments
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
    from subprocess import Popen

# --- Get the path to the script and check if it's writeable ---
#     These need to be located after the auto-installation section, because __file__ can't be used when running python3 -c $(curl ...)
APPLICATION_PATH = str(Path(__file__).parent.resolve())
PERMISSION_TO_UPDATE = os.access(f"{APPLICATION_PATH}/{os.path.basename(__file__)}", os.W_OK)

# --- Check if dependencies are installed and importable ---
HEIF_AVAILABLE = False
JXL_AVAILABLE = False
AVIF_AVAILABLE = False

try:
    from pillow_heif import register_heif_opener
    register_heif_opener()
    HEIF_AVAILABLE = True
except ImportError:
    HEIF_AVAILABLE = False
    print(f"WARNING(Nautilus-file-converter)(100): \"pillow_heif\" not found. View https://github.com/Lich-Corals/linux-file-converter-addon/blob/main/markdown/errors-and-warnings.md for more information." )

try:
    from jxlpy import JXLImagePlugin
    JXL_AVAILABLE = True
except ImportError:
    JXL_AVAILABLE = False
    print(f"WARNING(Nautilus-file-converter)(101): \"jxlpy\" not found. View https://github.com/Lich-Corals/linux-file-converter-addon/blob/main/markdown/errors-and-warnings.md for more information.")

try:
    import pillow_avif
    AVIF_AVAILABLE = True
except ImportError:
        print(f"WARNING(Nautilus-file-converter)(102) \"pillow-avif-plugin\" not found. View https://github.com/Lich-Corals/linux-file-converter-addon/blob/main/markdown/errors-and-warnings.md for more information.")

# --- Warn the user if there is no permission to self-update ---
if not PERMISSION_TO_UPDATE:
    print(f"ERROR(Nautilus-file-converter)(402): No permission to self-update; script at \"{APPLICATION_PATH}/{os.path.basename(__file__)}\" is not writeable. View https://github.com/Lich-Corals/linux-file-converter-addon/blob/main/markdown/errors-and-warnings.md for more information.")

#######
####### SELF-PREPARATION SECTION  --  CONFIGURATION
####### Getting user configuration

# --- Set default configs ---
#     These are the default settings and will reset with each update; edit ~/.config/linux-file-converter-addon/config.json if the program has permission to read and write it.
CONFIG_PRESET = {
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
    "displayFinishNotification": True,
    "alwaysCreateNemoAction": False
}

# --- Move settings from old config file to new location if the old one exists ---
if not os.path.isdir(CONFIGURATION_DIRECTORY):
    os.system(f'mkdir "{CONFIGURATION_DIRECTORY}"')
if Path(f"{APPLICATION_PATH}/NFC43-Config.json").is_file() and os.access(f"{APPLICATION_PATH}/NFC43-Config.json", os.W_OK):
    with open(f"{APPLICATION_PATH}/NFC43-Config.json", 'r') as file:
        try:
            old_config = json.load(file)
        except json.decoder.JSONDecodeError:
            old_config = CONFIG_PRESET
        file.close()
    CONFIG_PRESET = old_config.copy()
    with open(f"{APPLICATION_PATH}/NFC43-Config.json", 'w') as old_config_file:
        old_config["comment"] = f"THIS FILE DOES NOT CONFIGURE ANYTHING ANYMORE. USE {CONFIGURATION_FILE} INSTEAD!"
        old_config = json.dumps(old_config, indent=4)
        old_config_file.write(old_config)
        old_config_file.close()
    os.system(f'mv "{APPLICATION_PATH}/NFC43-Config.json" "{APPLICATION_PATH}/NFC43-Config.json.DISABLED"')
    os.system(f'notify-send --app-name="linux-file-converter-addon" "Config file moved." "Your new config file is here:\n{CONFIGURATION_DIRECTORY}"')
user_configuration = CONFIG_PRESET

# --- Load or store configs json ---
if os.access(CONFIGURATION_DIRECTORY, os.W_OK):
    try:
        if Path(CONFIGURATION_FILE).is_file():
            with open(CONFIGURATION_FILE, 'r') as file:
                try:
                    loaded_json = json.load(file)
                except json.decoder.JSONDecodeError:
                    loaded_json = CONFIG_PRESET
                user_configuration = loaded_json
            for setting in CONFIG_PRESET:
                if setting not in user_configuration:
                    user_configuration[setting] = CONFIG_PRESET[setting]
            loaded_json = json.dumps(user_configuration, indent=4)
        else:
            loaded_json = json.dumps(CONFIG_PRESET, indent=4)
        with open(CONFIGURATION_FILE, "w") as file:
            file.write(loaded_json)
    except:
        print("ERROR(Nautilus-file-converter)(401): Something went wrong while loading or updating the configuration file.")
        print(f"{format_exc()}")
else:
    print(f"ERROR(Nautilus-file-converter)(403): No permission to write configuration file; \"{CONFIGURATION_DIRECTORY}\" is not writeable. View https://github.com/Lich-Corals/linux-file-converter-addon/blob/main/markdown/errors-and-warnings.md for more information.")

#######
####### SELF-PREPARATION SECTION  --  SELF-UPDATE
####### Pretty self explaining...

# --- Check for updates and update if auto-update is enabled ---
if user_configuration["automaticUpdates"]:
    with request.urlopen("https://raw.githubusercontent.com/Lich-Corals/linux-file-converter-addon/main/nautilus-fileconverter.py") as f:
        downloaded_data = f.read().decode().strip()
    if CONVERTER_VERSION not in downloaded_data:
        print(f"UPDATES(Nautilus-file-converter)(104): Current Version: {CONVERTER_VERSION}\n"
              f"                                       Attempting to update...")
        if PERMISSION_TO_UPDATE:
            print("Updating...")
            application_file_location = f"{APPLICATION_PATH}/{os.path.basename(__file__)}"
            if user_configuration["showPatchNotes"]:
                #os.system(f"nohup xdg-open \"https://github.com/Lich-Corals/linux-file-converter-addon/blob/main/markdown/update-notification.md\" &")
                os.system('notify-send --app-name="linux-file-converter-addon" "Update installed." "More info: https://github.com/Lich-Corals/linux-file-converter-addon/blob/main/markdown/update-notification.md"')
            with open(application_file_location, 'w') as file:
                file.write(downloaded_data)

# --- Check for duplicate script if enabled ---
if user_configuration["checkForDoubleInstallation"] and "/.local/share/" in APPLICATION_PATH and os.path.isfile("/usr/share/nautilus-python/extensions/nautilus-fileconverter.py"):
    print(f"WARNING(Nautilus-file-converter)(103): Double script installation detected. View https://github.com/Lich-Corals/linux-file-converter-addon/blob/main/markdown/errors-and-warnings.md for more information.")

# --- Check for development status and apply settings ---
#     print() isn't working anymore after this command unless DEBUG_MODE is enabled
if not DEBUG_MODE:
    print = lambda *wish, **verbosity: None

print(f"pyheif: {HEIF_AVAILABLE}\njxlpy: {JXL_AVAILABLE}\npillow_avif: {AVIF_AVAILABLE}")

#######
####### SELF-PREPARATION SECTION  --  FORMATS
####### Defining read- and write formats

# --- Create file format tuples and write format dict-lists ---
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

# --- Add optional formats to existing lists ---
if user_configuration["convertFromOctetStream"]:
    READ_FORMATS_IMAGE = READ_FORMATS_IMAGE + OCTET_STREAM_FORMATS

if HEIF_AVAILABLE:
    READ_FORMATS_IMAGE = READ_FORMATS_IMAGE + READ_FORMATS_PYHEIF

if JXL_AVAILABLE:
    READ_FORMATS_IMAGE = READ_FORMATS_IMAGE + (READ_FORMATS_JXLPY,)
    WRITE_FORMATS_IMAGE.extend(WRITE_FORMATS_JXLPY)

if AVIF_AVAILABLE:
    WRITE_FORMATS_IMAGE.extend(WRITE_FORMATS_AVIF)

#######
####### SELF-PREPARATION SECTION  --  FUNCTIONS
####### Global function definitions

# --- Function used to get a mimetype's extension ---
def get_format_extension(file_format):
    return f".{file_format.get('extension', file_format['name'])}".lower()

# --- Function used to remove old timestamp ---
def remove_timestamp(file_path_stem):
    clean_stem = re.sub(r'\d{4}(-\d{2}){5}', "", file_path_stem)
    return clean_stem

# --- Adds datetime to file name if configured this way ---
def name_addition():
    if user_configuration["timeInNames"]:
        return datetime.today().strftime('%Y-%m-%d-%H-%M-%S')
    else:
        return ""

# --- Send a system notification if the option is enabled ---
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
def start_image_conversion(menu, arguments):
    subprocess = Process(target=convert_images, kwargs={"menu":menu, "format": arguments["format"], "files": arguments["files"]})
    subprocess.start()

# --- Function to start ffmpeg conversion in a new subprocess ---
def start_ffmpeg_conversion(menu, arguments):
    subprocess = Process(target=convert_ffmpeg_media, kwargs={"menu":menu, "format": arguments["format"], "files": arguments["files"]})
    subprocess.start()

# --- Find out for which program the extension is installed ---
def get_installation_type() -> InstallationType:
    global APPLICATION_PATH
    global INSTALLATION_LOCATIONS
    detected_installation_type = InstallationType.UNKNOWN
    for installation_location in INSTALLATION_LOCATIONS:
        if str(Path(INSTALLATION_LOCATIONS[installation_location]).parent) in APPLICATION_PATH:
            detected_installation_type = installation_location
    return detected_installation_type

#######
####### SELF-PREPARATION SECTION  --  CLASSES
####### Definitions of classes for Nautilus- and adaption use

print(f"Detected installation type: {get_installation_type()}")

# --- Nautilus class ---
if get_installation_type() == InstallationType.NAUTILUS:
    class LinuxFileConverterMenuProvider(GObject.GObject, Nautilus.MenuProvider):
        # --- Get file mime and trigger submenu building ---
        def get_file_items(self, *args) -> List[Nautilus.MenuItem]:
            files = args[-1]
            for file in files:
                print(file.get_mime_type())
                file_mime = file.get_mime_type()
                if file_mime in READ_FORMATS_IMAGE or file_mime == 'application/octet-stream':
                    return self.sub_menu_builder(WRITE_FORMATS_IMAGE,
                                                callback=start_image_conversion,
                                                files=files)
                if file_mime in READ_FORMATS_AUDIO:
                    return self.sub_menu_builder(WRITE_FORMATS_AUDIO,
                                                callback=start_ffmpeg_conversion,
                                                files=files)
                if file_mime in READ_FORMATS_VIDEO:
                    return self.sub_menu_builder(WRITE_FORMATS_VIDEO,
                                                callback=start_ffmpeg_conversion,
                                                files=files)

        # --- Create a new sub-menu ---
        def create_sub_menu_object(self, name, label):
            menu_item = Nautilus.MenuItem(
                name=f"LinuxFileConverterMenuProvider::{name}",
                label=label,
            )
            menu = Nautilus.Menu()
            menu_item.set_submenu(menu)
            return menu, menu_item

        # --- Add a sub-menu item to a selected sub menu with a callback function and associated arguments ---
        def add_sub_menu_item(self, name, label, menu, callback, arguments):
            menu_item = Nautilus.MenuItem(
                name=f"LinuxFileConverterMenuProvider::{name}",
                label=label,
            )
            menu_item.connect('activate', callback, arguments)
            menu.append_item(menu_item)

        # --- Build the context menu and submenus ---
        def sub_menu_builder(self, formats, callback, files):
            main_menu, main_menu_item = self.create_sub_menu_object("convert_to_menu", "Convert to...")

            for file_format in formats:
                self.add_sub_menu_item(f"convert_to_{file_format['name']}", file_format['name'], main_menu, callback, {"format": file_format, "files": files})

            if callback == start_image_conversion:
                if user_configuration["convertToSquares"]:
                    main_menu_sub_menu_squares, main_menu_sub_menu_item_squares = self.create_sub_menu_object("square_format_menu", "Square...")
                    for square_format in WRITE_FORMATS_SQUARE:
                        self.add_sub_menu_item(f"square_convert_{square_format["name"]}", square_format["name"], main_menu_sub_menu_squares, callback, {"format": square_format, "files": files})
                    main_menu.append_item(main_menu_sub_menu_item_squares)

                if user_configuration["convertToWallpapers"]:
                    main_menu_sub_menu_wallpapers, main_menu_sub_menu_item_wallpapers = self.create_sub_menu_object("wallpaper_format_menu", "Wallpaper...")
                    for wallpaper_format in WRITE_FORMATS_WALLPAPER:
                        self.add_sub_menu_item(f"wallpaper_convert_{wallpaper_format["name"]}", wallpaper_format["name"], main_menu_sub_menu_wallpapers, callback, {"format": wallpaper_format, "files": files})
                    main_menu.append_item(main_menu_sub_menu_item_wallpapers)

            if user_configuration["showPatchNoteButton"]:
                self.add_sub_menu_item("patch_notes", f"View patch notes ({CONVERTER_VERSION})", main_menu, self.show_patch_notes, {})

            if user_configuration["showConfigHint"]:
                self.add_sub_menu_item("patch_notes", f"Configure LFCA", main_menu, self.show_configuration_page, {})

            return [main_menu_item]

        # --- openPatchNotes and openConfigHint functions for context menu options ---
        def show_patch_notes(self, menu, arguments):
            Popen(["xdg-open", "https://github.com/Lich-Corals/linux-file-converter-addon/releases"])

        def show_configuration_page(self, menu, arguments):
            Popen(["xdg-open", "https://github.com/Lich-Corals/linux-file-converter-addon/blob/main/markdown/configuration.md"])
            Popen(["xdg-open", f"{CONFIGURATION_FILE}"])

# --- Adaption class ---
if get_installation_type() != InstallationType.NAUTILUS:
    class LinuxFileConverterWindow(Gtk.Window):
        # --- Add a label to a selected box ---
        def add_label_centered(self, box, markup):
            label = Gtk.Label()
            label.set_markup(markup)
            label.set_justify(Gtk.Justification.CENTER)
            box.pack_start(label, True, True, 0)

        # --- Generate the combo-box with all compatible formats ---
        def add_format_combo_box(self, box):
            extensions = Gtk.ListStore(str, str, int)
            only_images_selected = True
            only_audios_selected = True
            only_videos_selected = True
            for argument in SYSTEM_ARGUMENTS:
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
            combo_box = Gtk.ComboBox.new_with_model(extensions)
            renderer_text = Gtk.CellRendererText()
            combo_box.set_entry_text_column(0)
            combo_box.pack_start(renderer_text, True)
            combo_box.add_attribute(renderer_text, "text", 0)
            combo_box.connect("changed", self.start_conversion)
            box.pack_start(combo_box, True, True, 0)
        
        def __init__(self):
            super().__init__(title=f"Convert file")
            self.set_border_width(15)
            self.set_default_size(200, 20)
            self.set_resizable(False)
            self.connect("key-press-event",self.on_key_press_event)

            box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)

            self.add_label_centered(box, "Select a format:")
            self.add_format_combo_box(box)
            if user_configuration["showPatchNoteButton"]:
                self.add_label_centered(box, f"""<span size="x-small">version {CONVERTER_VERSION}</span>""")
            if user_configuration["showConfigHint"]:
                self.add_label_centered(box, f"""<span size="x-small">View <a href="https://github.com/Lich-Corals/linux-file-converter-addon/blob/main/markdown/configuration.md">the config documentation</a>\nto configure the script and hide this text.</span>""")
            self.add_label_centered(box, f"""<span color="#696969" size="x-small">Linux-File-Converter-Addon  Copyright (C) 2025  Linus Tibert\nunder the <a href="https://github.com/Lich-Corals/linux-file-converter-addon/blob/main/LICENSE">GNU Affero General Public License</a>.</span>""")
            self.add(box)

        # --- Get data from combo-box and run the right conversion function ---
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
                    for retun_path in SYSTEM_ARGUMENTS:
                        return_paths.append(Path(retun_path))
                    if return_type == 0:
                        start_image_conversion(self, {"format": return_format, "files": return_paths})
                    elif return_type == 1:
                        start_ffmpeg_conversion(self, {"format": return_format, "files": return_paths})
            Gtk.main_quit()

        # --- Close the popup if ESC is pressed ---
        def on_key_press_event(self, widget, event):
            print(f"Key pressed: {event.keyval}")
            quit_window_key_value = 65307
            if event.keyval == quit_window_key_value:
                exit()

    #######
    ####### ADAPTION-STARTUP SECTION
    ####### Creation of the nemo_action and finally of the Gtk Window

    print(f"Args: {str(SYSTEM_ARGUMENTS)} \nPath:{APPLICATION_PATH}")
    # --- Create nemo_action ---
    if get_installation_type() == InstallationType.NEMO or user_configuration["alwaysCreateNemoAction"]:
        nemo_read_formats = ""
        global_read_formats = READ_FORMATS_IMAGE + READ_FORMATS_AUDIO + READ_FORMATS_VIDEO
        for media_format in global_read_formats:
            if media_format not in nemo_read_formats:
                nemo_read_formats += media_format + ";"
        nemo_action_lines = ["[Nemo Action]",
                            "Name=Convert to...",
                            "Comment=Convert file using linux-file-converter-addon",
                            f"Exec=<{os.path.basename(__file__)} %F>",
                            "Selection=NotNone",
                            f"Mimetypes={nemo_read_formats}"]
        with open(f"{APPLICATION_PATH}/{Path(os.path.basename(__file__)).stem}.nemo_action", "w") as file:
            for line in nemo_action_lines:
                file.write(line + "\n")
            file.close()
    
    # --- Create the window ---
    gtk_popup_window_object = LinuxFileConverterWindow()
    gtk_popup_window_object.connect("destroy", Gtk.main_quit)
    gtk_popup_window_object.show_all()
    Gtk.main()