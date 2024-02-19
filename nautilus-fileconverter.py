# --- Version number ---
converterVersion = "001002001" # Change the number if you want to trigger an update.

# --- Imports ---
from gi.repository import Nautilus, GObject
from typing import List
from PIL import Image, UnidentifiedImageError
from urllib.parse import urlparse, unquote
from pathlib import Path
import pathlib
import os, shlex
import urllib.request
import json

# --- Get the path to the script and if it's writeable ---
currentPath = str(pathlib.Path(__file__).parent.resolve())  # used for config file and self-update!
scriptUpdateable = os.access(f"{currentPath}/{os.path.basename(__file__)}", os.W_OK)

# --- Check if dependencies are installed and imported ---
pyheifInstalled = False
jxlpyInstalled = False

try:
    import pyheif
    pyheifInstalled = True
except ImportError:
    pyheifInstalled = False
    print(f"WARNING(Nautilus-file-converter)(000): \"pyheif\" not found, if you want to convert from heif format. View https://github.com/Lich-Corals/Nautilus-fileconverter-43/blob/main/README.md#6-warnings-and-errors for more information." )

try:
    import jxlpy
    from jxlpy import JXLImagePlugin
    jxlpyInstalled = True
except ImportError:
    jxlpyInstalled = False
    print(f"WARNING(Nautilus-file-converter)(001): \"jxlpy\" not found, if you want to convert from- or to jxl format. View https://github.com/Lich-Corals/Nautilus-fileconverter-43/blob/main/README.md#6-warnings-and-errors for more information.")

if not scriptUpdateable:
    print(f"WARNING(Nautilus-file-converter)(002): No permission to self-update; script at \"{currentPath}/{os.path.basename(__file__)}\" is not writeable. View https://github.com/Lich-Corals/Nautilus-fileconverter-43/blob/main/README.md#6-warnings-and-errors for more information.")

if not os.access(currentPath, os.W_OK):
    print(f"WARNING(Nautilus-file-converter)(003): No permission to write configuration file; \"{currentPath}\" is not writeable. View https://github.com/Lich-Corals/Nautilus-fileconverter-43/blob/main/README.md#6-warnings-and-errors for more information.")

# --- Set default configs ---
_configPreset = {                                 # These are the pre-defined default settings; edit NFC43-Config.json if the program is installed in your home dictionary.
    "automaticUpdates": True,           # Replace the "True" with "False" if you don't want automatic updates.
    "showPatchNotes": True,             # Replace the "True" with "False" if you don't want to see patch notes.
    "showPatchNoteButton": True,        # Replace the "True" with "False" if you don't want the "View patch notes" button in the converter menu.
    "showConfigHint": True,             # Replace the "True" with "False" if you don't want to see the config hint.
    "convertToSquares": True,           # Replace the "True" with "False" if you don't want to convert to square formats.
    "convertToWallpapers": True,        # Replace the "True" with "False" if you don't want to convert to wallpaper formats.
    "checkForDoubleInstallation": True  # Replace the "True" with "False" if you don't the script to check if there is a second installation in another dictionary.
}

# --- Load or store configs json ---
if scriptUpdateable:
    if Path(f"{currentPath}/NFC43-Config.json").is_file():
        with open(f"{currentPath}/NFC43-Config.json", 'r') as jsonFile:
            try:
                configJson = json.load(jsonFile)
            except json.decoder.JSONDecodeError:
                configJson = _configPreset
            _config = configJson
        for _setting in _configPreset:
            if _setting not in _config:
                _config[_setting] = _configPreset[_setting]
        configJson = json.dumps(_config, indent=4)
    else:
        configJson = json.dumps(_configPreset, indent=4)
    with open(f"{currentPath}/NFC43-Config.json", "w") as jsonFile:
        jsonFile.write(configJson)

# --- Check for updates and update if auto-update is enabled ---
if _config["automaticUpdates"]:
    with urllib.request.urlopen(
            "https://raw.githubusercontent.com/Lich-Corals/Nautilus-fileconverter-43/main/nautilus-fileconverter.py") as f:
        onlineFile = f.read().decode().strip()
    if converterVersion not in onlineFile:
        print("Updating...")
        if _config["showPatchNotes"]:
            os.system(f"nohup xdg-open \"https://github.com/Lich-Corals/Nautilus-fileconverter-43/releases\" &")
        if scriptUpdateable:
            fileUpdatePath = f"{currentPath}/{os.path.basename(__file__)}"
            with open(fileUpdatePath, 'w') as file:
                file.write(onlineFile)

# --- Check for duplicate script if enabled ---
if _config["checkForDoubleInstallation"] and scriptUpdateable and os.path.isfile("/usr/share/nautilus-python/extensions/nautilus-fileconverter.py"):
    print(f"WARNING(Nautilus-file-converter)(004): Double script installation detected. View https://github.com/Lich-Corals/Nautilus-fileconverter-43/blob/main/README.md#6-warnings-and-errors for more information.")

# --- Disable debug printing ---
# comment it out (using '#' in front of the line) if you wish debug printing
print = lambda *wish, **verbosity: None

# --- Create file format tuples and write format dict-lists? ---
class FileConverterMenuProvider(GObject.GObject, Nautilus.MenuProvider):
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
                          'application/octet-stream',
                          'windows/metafile',
                          'image/x-xpixmap',
                          'image/webp')

    pyheifReadFormats = ('image/avif',
                         'image/heif')

    jxlpyReadFormats = ('image/jxl')

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

    WRITE_FORMATS_IMAGE = [{'name': 'JPEG'},
                           {'name': 'PNG'},
                           {'name': 'BMP'},
                           {'name': 'GIF'},
                           {'name': 'WebP'},
                           {'name': 'TIFF'}]

    jxlpyWriteFormats = [{'name': 'JXL'}]

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

    if pyheifInstalled:
        READ_FORMATS_IMAGE = READ_FORMATS_IMAGE + pyheifReadFormats

    if jxlpyInstalled:
        READ_FORMATS_IMAGE = READ_FORMATS_IMAGE + (jxlpyReadFormats,)
        WRITE_FORMATS_IMAGE.extend(jxlpyWriteFormats)

# --- Get file mime and trigger submenu building ---
    def get_file_items(self, *args) -> List[Nautilus.MenuItem]:
        files = args[-1]
        for file in files:
            print(file.get_mime_type())
            file_mime = file.get_mime_type()
            if file_mime in self.READ_FORMATS_IMAGE:
                return self.__submenu_builder(self.WRITE_FORMATS_IMAGE,
                                              callback=self.convert_image,
                                              files=files)
            if file_mime in self.READ_FORMATS_AUDIO:
                return self.__submenu_builder(self.WRITE_FORMATS_AUDIO,
                                              callback=self.convert_audio,
                                              files=files)
            if file_mime in self.READ_FORMATS_VIDEO:
                return self.__submenu_builder(self.WRITE_FORMATS_VIDEO,
                                              callback=self.convert_video,
                                              files=files)

# --- Build the context menu and submenus ---
    def __submenu_builder(self, formats, callback, files):
        top_menuitem = Nautilus.MenuItem(
            name="FileConverterMenuProvider::convert_to",
            label="Convert to...",
        )
        submenu = Nautilus.Menu()
        top_menuitem.set_submenu(submenu)

        for format in formats:
            sub_menuitem = Nautilus.MenuItem(
                name='ConvertToSubmenu_' + format['name'],
                label=(format['name']),
            )
            sub_menuitem.connect('activate', callback, format, files)
            submenu.append_item(sub_menuitem)

        if formats[0]['name'] == 'JPEG':
            if _config["convertToSquares"]:
                top_menuitemSquare = Nautilus.MenuItem(
                    name="FileConverterMenuProvider::square_png",
                    label="Square...",
                )
                submenuSquare = Nautilus.Menu()
                top_menuitemSquare.set_submenu(submenuSquare)
                for formatSquare in self.WRITE_FORMATS_SQUARE:
                    sub_menuitemSquare = Nautilus.MenuItem(
                        name='squarePngSubmenu_' + formatSquare['name'],
                        label=(formatSquare['name']),
                    )
                    sub_menuitemSquare.connect('activate', callback, formatSquare, files)
                    submenuSquare.append_item(sub_menuitemSquare)
                submenu.append_item(top_menuitemSquare)

            if _config["convertToWallpapers"]:
                top_menuitemWallpaper = Nautilus.MenuItem(
                    name="FileConverterMenuProvider::wallpaper",
                    label="Wallpaper...",
                )
                submenuWallpaper = Nautilus.Menu()
                top_menuitemWallpaper.set_submenu(submenuWallpaper)
                for formatWallpaper in self.WRITE_FORMATS_WALLPAPER:
                    sub_menuitemWallpaper = Nautilus.MenuItem(
                        name='WallpaperPngSubmenu_' + formatWallpaper['name'],
                        label=(formatWallpaper['name']),
                    )
                    sub_menuitemWallpaper.connect('activate', callback, formatWallpaper, files)
                    submenuWallpaper.append_item(sub_menuitemWallpaper)
                submenu.append_item(top_menuitemWallpaper)

        if _config["showPatchNoteButton"]:
            sub_menuitem_patchNotes = Nautilus.MenuItem(
                name="patchNotes",
                label=f"View patch notes ({converterVersion})",
            )
            callback = self.openPatchNotes
            sub_menuitem_patchNotes.connect('activate', callback,)
            submenu.append_item(sub_menuitem_patchNotes)

        if _config["showConfigHint"]:
            sub_menuitem_configHint = Nautilus.MenuItem(
                name="configHint",
                label=f"Configure NFC43",
            )
            callback = self.openConfigHint
            sub_menuitem_configHint.connect('activate', callback,)
            submenu.append_item(sub_menuitem_configHint)

        return [top_menuitem]

# --- openPatchNotes and openConfigHint functions for context menu options ---
    def openPatchNotes(self, menu):
        os.system(f"nohup xdg-open \"https://github.com/Lich-Corals/Nautilus-fileconverter-43/releases\" &")

    def openConfigHint(self, menu):
        os.system(f"nohup xdg-open \"https://github.com/Lich-Corals/Nautilus-fileconverter-43?tab=readme-ov-file#3-configuration\" &")

# --- Function used to get a mimetype's extension ---
    def __get_extension(self, format):
        return f".{format.get('extension', format['name'])}".lower()

# --- Function to convert between image formats ---
    def convert_image(self, menu, format, files):
        global file_path_to
        print(format)
        for file in files:
            if 'extension' not in format:
                format['extension'] = format['name']
            file_path = Path(unquote(urlparse(file.get_uri()).path))
            count = 0
            to_file_path_mod = file_path.with_name(f"{file_path.stem}")
            while os.path.exists(shlex.quote(f"{to_file_path_mod}.{format['extension'].lower()}")):
                count += 1
                to_file_path_mod = file_path.with_name(
                    f"{file_path.stem}-{count}")
                file_path_to = to_file_path_mod
            try:
                image = Image.open(file_path)
                if (format['name']) == 'JPEG':
                    image = image.convert('RGB')
                if 'square' in format:
                    image = image.resize((int(format['square']), int(format['square'])))
                if 'w' in format:
                    image = image.resize((int(format['w']), int(format['h'])))
                file_path_to = f"{to_file_path_mod}.{format['extension'].lower()}"
                image.save(file_path_to,
                           format=(format['extension']))
            except UnidentifiedImageError:
                try:
                    heif_file = pyheif.read(file_path)
                    heif_image = Image.frombytes(
                        heif_file.mode,
                        heif_file.size,
                        heif_file.data,
                        "raw",
                        heif_file.mode,
                        heif_file.stride,
                    )
                    if (format['extension']) == 'JPEG':
                        heif_image = heif_image.convert("RGB")
                    heif_image.save(file_path.with_suffix(self.__get_extension(format)), format['extension'])
                except UnidentifiedImageError:
                    pass
                pass

# --- Function to convert using FFMPEG (video and audio) ---
    def convert_audio(self, menu, format, files):
        print(format)
        for file in files:
            from_file_path = Path(unquote(urlparse(file.get_uri()).path))
            to_file_path = from_file_path.with_suffix(self.__get_extension(format).lower())
            count = 0
            to_file_path_mod = from_file_path.with_name(f"{from_file_path.stem}")
            while to_file_path_mod.exists() or to_file_path.exists():
                count += 1
                to_file_path_mod = from_file_path.with_name(f"{from_file_path.stem}({count}){self.__get_extension(format).lower()}")
                print(shlex.quote(str(from_file_path)))
                to_file_path = to_file_path_mod
            os.system(
                f"nohup ffmpeg -i {shlex.quote(str(from_file_path))} -strict experimental -c:v libvpx-vp9 -crf 18 -preset slower -b:v 4000k {shlex.quote(str(to_file_path))} | tee &")

    # --- Convert video with the convert_audio() function ---
    def convert_video(self, menu, format, files):
        # use same ffmpeg backend
        self.convert_audio(menu, format, files)