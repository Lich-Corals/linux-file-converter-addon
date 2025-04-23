#! /usr/bin/python3 -OOt

# --- Version number ---
converterVersion = "001003002" # Change the number if you want to trigger an update.
# --- Variable to enable debug mode ---
development_version = False

# --- Imports ---
import gi
from gi.repository import GObject, Gtk, Nautilus
from typing import List
from PIL import Image, UnidentifiedImageError
from urllib.parse import urlparse, unquote
from pathlib import Path
from datetime import datetime
import magic
import pathlib
import os, shlex
import urllib.request
import json
import sys
import ast
import re
from multiprocessing import Process
import traceback

# --- Create magic object ---
mime = magic.Magic(mime=True)

# --- Get the path to the script and if it's writeable ---
currentPath = str(pathlib.Path(__file__).parent.resolve())  # used for config file and self-update!
scriptUpdateable = os.access(f"{currentPath}/{os.path.basename(__file__)}", os.W_OK)

# --- Check if dependencies are installed and imported ---
pillow_heifInstalled = False
jxlpyInstalled = False
pillow_avif_pluginInstalled = False

try:
    from pillow_heif import register_heif_opener
    register_heif_opener()
    pillow_heifInstalled = True
except ImportError:
    pillow_heifInstalled = False
    print(f"WARNING(Nautilus-file-converter)(100): \"pillow_heif\" not found. View https://github.com/Lich-Corals/linux-file-converter-addon/blob/main/markdown/errors-and-warnings.md for more information." )

try:
    import jxlpy
    from jxlpy import JXLImagePlugin
    jxlpyInstalled = True
except ImportError:
    jxlpyInstalled = False
    print(f"WARNING(Nautilus-file-converter)(101): \"jxlpy\" not found. View https://github.com/Lich-Corals/linux-file-converter-addon/blob/main/markdown/errors-and-warnings.md for more information.")

try:
    import pillow_avif
    pillow_avif_pluginInstalled = True
except ImportError:
        print(f"WARNING(Nautilus-file-converter)(102) \"pillow-avif-plugin\" not found. View https://github.com/Lich-Corals/linux-file-converter-addon/blob/main/markdown/errors-and-warnings.md for more information.")

if not scriptUpdateable:
    print(f"ERROR(Nautilus-file-converter)(402): No permission to self-update; script at \"{currentPath}/{os.path.basename(__file__)}\" is not writeable. View https://github.com/Lich-Corals/linux-file-converter-addon/blob/main/markdown/errors-and-warnings.md for more information.")

if not os.access(currentPath, os.W_OK):
    print(f"ERROR(Nautilus-file-converter)(403): No permission to write configuration file; \"{currentPath}\" is not writeable. View https://github.com/Lich-Corals/linux-file-converter-addon/blob/main/markdown/errors-and-warnings.md for more information.")

# --- Set default configs ---
_configPreset = {                                 # These are the pre-defined default settings; edit NFC43-Config.json if the program has permission to write.
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
_config = _configPreset

# --- Load or store configs json ---
if scriptUpdateable:
    try:
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
    except:
        print("ERROR(Nautilus-file-converter)(401): Something went wrong while loading or updating the configuration file.")
        print(f"{traceback.format_exc()}")

# --- Check for updates and update if auto-update is enabled ---
if _config["automaticUpdates"]:
    with urllib.request.urlopen(
            "https://raw.githubusercontent.com/Lich-Corals/linux-file-converter-addon/main/nautilus-fileconverter.py") as f:
        onlineFile = f.read().decode().strip()
    if converterVersion not in onlineFile:
        print(f"UPDATES(Nautilus-file-converter)(104): Current Version: {converterVersion}\n"
              f"                                       Attempting to update...")
        if scriptUpdateable:
            print("Updating...")
            fileUpdatePath = f"{currentPath}/{os.path.basename(__file__)}"
            if _config["showPatchNotes"]:
                #os.system(f"nohup xdg-open \"https://github.com/Lich-Corals/linux-file-converter-addon/blob/main/markdown/update-notification.md\" &")
                os.system('notify-send --app-name="linux-file-converter-addon" "Update installed." "More info: https://github.com/Lich-Corals/linux-file-converter-addon/blob/main/markdown/update-notification.md"')
            with open(fileUpdatePath, 'w') as file:
                file.write(onlineFile)

# --- Check for duplicate script if enabled ---
if _config["checkForDoubleInstallation"] and "/.local/share/" in currentPath and os.path.isfile("/usr/share/nautilus-python/extensions/nautilus-fileconverter.py"):
    print(f"WARNING(Nautilus-file-converter)(103): Double script installation detected. View https://github.com/Lich-Corals/linux-file-converter-addon/blob/main/markdown/errors-and-warnings.md for more information.")

# --- Check for development status and apply settings ---
if not development_version:
    print = lambda *wish, **verbosity: None

print(f"pyheif: {pillow_heifInstalled}\njxlpy: {jxlpyInstalled}\npillow_avif: {pillow_avif_pluginInstalled}")

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

pyheifReadFormats = ('image/avif',
                     'image/heif',
                     'image/heic')

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

octetStreamFormats = ('application/octet-stream',)

WRITE_FORMATS_IMAGE = [{'name': 'PNG'},
                       {'name': 'JPEG'},
                       {'name': 'BMP'},
                       {'name': 'GIF'},
                       {'name': 'WebP'},
                       {'name': 'TIFF'}]

jxlpyWriteFormats = [{'name': 'JXL'}]

pillow_avif_pluginWriteFormats = [{ 'name': 'AVIF'}]

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

if _config["convertFromOctetStream"]:
    READ_FORMATS_IMAGE = READ_FORMATS_IMAGE + octetStreamFormats

if pillow_heifInstalled:
    READ_FORMATS_IMAGE = READ_FORMATS_IMAGE + pyheifReadFormats

if jxlpyInstalled:
    READ_FORMATS_IMAGE = READ_FORMATS_IMAGE + (jxlpyReadFormats,)
    WRITE_FORMATS_IMAGE.extend(jxlpyWriteFormats)

if pillow_avif_pluginInstalled:
    WRITE_FORMATS_IMAGE.extend(pillow_avif_pluginWriteFormats)

if _config["timeInNames"] == True:
    _addToName = datetime.today().strftime('%Y-%m-%d-%H-%M-%S')
else:
    _addToName = ""

# --- Function used to get a mimetype's extension ---
def __get_extension(format_):
    return f".{format_.get('extension', format_['name'])}".lower()

# --- Function used to remove old timestamp ---
def __removeTimestamp(_stem):
    clearStem = re.sub(r'\d{4}(-\d{2}){5}', "", _stem)
    return clearStem

# --- Function to convert between image formats ---
def _convert_image_process(*args, **kwargs):
    menu = kwargs["menu"]
    format_ = kwargs["format"]
    files = kwargs["files"]
    conversion_results = {"success": 0, "fail": 0}
    for file in files:
        if 'extension' not in format_:
            format_['extension'] = format_['name']
        if str(type(file)) == "<class '__gi__.NautilusVFSFile'>":
            from_file_path = Path(unquote(urlparse(file.get_uri()).path))
        else:
            from_file_path = file
        print(__removeTimestamp(from_file_path.stem) + from_file_path.stem)
        to_file_path = from_file_path.with_name(f"{__removeTimestamp(from_file_path.stem)}{_addToName}.{format_['extension'].lower()}")
        try:
            image = Image.open(from_file_path)
            image_open_error = False
            conversion_results["success"] += 1
        except UnidentifiedImageError:
            print(f"(Nautilus-file-converter)(400): {from_file_path} is in an unconvertable file-format.")
            image_open_error = True
            conversion_results["fail"] += 1
        if not image_open_error:
            if (format_['name']) == 'JPEG':
                image = image.convert('RGB')
            if 'square' in format_:
                image = image.resize((int(format_['square']), int(format_['square'])))
            if 'w' in format_:
                image = image.resize((int(format_['w']), int(format_['h'])))
            image.save(to_file_path, format=(format_['extension']))
    if _config["displayFinishNotification"]:
        os.system(f'notify-send --app-name="linux-file-converter-addon" "Conversion finished" "Successfull: {conversion_results["success"]}\nFailed: {conversion_results["fail"]}"')

# --- Function to start image conversion in a new subprocess ---
def convert_image(menu, format_, files):
    subprocess = Process(target=_convert_image_process, kwargs={"menu":menu, "format": format_, "files": files})
    subprocess.start()

# --- Function to start ffmpeg conversion in a new subprocess ---
def convert_ffmpeg(menu, format_, files):
    subprocess = Process(target=_convert_ffmpeg_process, kwargs={"menu":menu, "format": format_, "files": files})
    subprocess.start()

# --- Function to convert using FFMPEG (video and audio) ---
def _convert_ffmpeg_process(*args, **kwargs):
    menu = kwargs["menu"]
    format_ = kwargs["format"]
    files = kwargs["files"]
    global __get_extension
    converted_files = 0
    for file in files:
        if str(type(file)) == "<class '__gi__.NautilusVFSFile'>":
            from_file_path = Path(unquote(urlparse(file.get_uri()).path))
        else:
            from_file_path = file
        to_file_path = from_file_path.with_name(f"{__removeTimestamp(from_file_path.stem)}{_addToName}{__get_extension(format_).lower()}")
        os.system(f"ffmpeg -i {shlex.quote(str(from_file_path))} -strict experimental -c:v libvpx-vp9 -crf 18 -preset slower -b:v 4000k {shlex.quote(str(to_file_path))}")
        converted_files += 1
    if _config["displayFinishNotification"]:
        os.system(f'notify-send --app-name="linux-file-converter-addon" "Conversion finished" "converted files: {converted_files}"')
        
# --- Nemo adaption ---
class nautilusFileConverterPopup(Gtk.Window):
    def __init__(self):
        super().__init__(title=f"Convert file")
        self.set_border_width(15)
        self.set_default_size(200, 20)

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)

        label = Gtk.Label(label="Select a format:")
        label.set_justify(Gtk.Justification.CENTER)
        vbox.pack_start(label, False, False, 0)
        versionInfo = Gtk.Label()
        versionInfo.set_markup(f"""<span size="x-small">version {converterVersion}</span>""")
        versionInfo.set_justify(Gtk.Justification.CENTER)
        configHint = Gtk.Label()
        configHint.set_justify(Gtk.Justification.CENTER)
        configHint.set_markup(f"""<span size="x-small">View <a href="https://github.com/Lich-Corals/linux-file-converter-addon/blob/main/markdown/configuration.md">the config documentation</a>\nto configure the script and hide this text.</span>""")

        extensions = Gtk.ListStore(str, str, int)
        _allImages = True
        _allAudios = True
        _allVideos = True
        for _arg in _nemoArgs:
            if not mime.from_file(_arg) in READ_FORMATS_IMAGE:
                _allImages = False
            if not mime.from_file(_arg) in READ_FORMATS_AUDIO:
                _allAudios = False
            if not mime.from_file(_arg) in READ_FORMATS_VIDEO:
                _allVideos = False

        if _config["showDummyOption"]:
            extensions.append(["-", "none", 2])

        if _allImages:
            for writeFormat in WRITE_FORMATS_IMAGE:
                print(writeFormat)
                extensions.append([writeFormat['name'], str(writeFormat), 0])
            if _config["convertToSquares"]:
                for writeFormat in WRITE_FORMATS_SQUARE:
                    extensions.append([writeFormat['name'], str(writeFormat), 0])
            if _config["convertToWallpapers"]:
                for writeFormat in WRITE_FORMATS_WALLPAPER:
                    extensions.append([writeFormat['name'], str(writeFormat), 0])
        if _allAudios:
            for writeFormat in WRITE_FORMATS_AUDIO:
                extensions.append([writeFormat['name'], str(writeFormat), 1])
        if _allVideos:
            for writeFormat in WRITE_FORMATS_VIDEO:
                extensions.append([writeFormat['name'], str(writeFormat), 1])

        self.add(vbox)
        combo = Gtk.ComboBox.new_with_model(extensions)
        renderer_text = Gtk.CellRendererText()
        combo.set_entry_text_column(0)
        combo.pack_start(renderer_text, True)
        combo.add_attribute(renderer_text, "text", 0)
        combo.connect("changed", self._nemoConvert)
        vbox.pack_start(combo, False, False, 0)
        if _config["showPatchNoteButton"]:
            vbox.pack_start(versionInfo, False, False, 0)
        if _config["showConfigHint"]:
            vbox.pack_start(configHint, True, True, 0)

    def _nemoConvert(self, combo):
        tree_iter = combo.get_active_iter()
        if tree_iter is not None:
            model = combo.get_model()
            return_name, return_format, return_type = model[tree_iter][:4]
            print(return_name, return_format, return_type)
            return_format = ast.literal_eval(return_format)
            return_paths = []
            if not return_type == 2:
                self.hide()
                for retun_path in _nemoArgs:
                    return_paths.append(Path(retun_path))
                if return_type == 0:
                    convert_image(self, return_format, return_paths)
                elif return_type == 1:
                    convert_ffmpeg(self, return_format, return_paths)


_nemoArgs = sys.argv[1:len(sys.argv)]
if len(sys.argv) > 1:
    print(f"Args: {str(_nemoArgs)} \nPath:{currentPath}")

    # --- Generate nemo_action ---
    _readFormatsNemo = ""
    _allReadFormats = READ_FORMATS_IMAGE + READ_FORMATS_AUDIO + READ_FORMATS_VIDEO
    for _currentFormat in _allReadFormats:
        if _currentFormat not in _readFormatsNemo:
            _readFormatsNemo += _currentFormat + ";"
    _nemoActionLines = ["[Nemo Action]",
                        "Name=Convert to...",
                        "Comment=Convert file using nautilus-fileconverter",
                        "Exec=<nautilus-fileconverter.py %F>",
                        "Selection=NotNone",
                        f"Mimetypes={_readFormatsNemo}"]
    with open(f"{currentPath}/nautilus-fileconverter.nemo_action", "w") as file:
        for _line in _nemoActionLines:
            file.write(_line + "\n")

    _gtkPopupWindow = nautilusFileConverterPopup()
    _gtkPopupWindow.connect("destroy", Gtk.main_quit)
    _gtkPopupWindow.show_all()
    Gtk.main()

# --- Nautilus class ---
class FileConverterMenuProvider(GObject.GObject, Nautilus.MenuProvider):
    # --- Get file mime and trigger submenu building ---
    def get_file_items(self, *args) -> List[Nautilus.MenuItem]:
        files = args[-1]
        for file in files:
            print(file.get_mime_type())
            file_mime = file.get_mime_type()
            if file_mime in READ_FORMATS_IMAGE or file_mime == 'application/octet-stream':
                return self.__submenu_builder(WRITE_FORMATS_IMAGE,
                                              callback=convert_image,
                                              files=files)
            if file_mime in READ_FORMATS_AUDIO:
                return self.__submenu_builder(WRITE_FORMATS_AUDIO,
                                              callback=convert_ffmpeg,
                                              files=files)
            if file_mime in READ_FORMATS_VIDEO:
                return self.__submenu_builder(WRITE_FORMATS_VIDEO,
                                              callback=convert_ffmpeg,
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

        if formats[1]['name'] == 'JPEG':
            if _config["convertToSquares"]:
                top_menuitemSquare = Nautilus.MenuItem(
                    name="FileConverterMenuProvider::square_png",
                    label="Square...",
                )
                submenuSquare = Nautilus.Menu()
                top_menuitemSquare.set_submenu(submenuSquare)
                for formatSquare in WRITE_FORMATS_SQUARE:
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
                for formatWallpaper in WRITE_FORMATS_WALLPAPER:
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
        os.system(f"nohup xdg-open \"https://github.com/Lich-Corals/linux-file-converter-addon/releases\" &")

    def openConfigHint(self, menu):
        os.system(f"nohup xdg-open \"https://github.com/Lich-Corals/linux-file-converter-addon?tab=readme-ov-file#3-configuration\" &")
