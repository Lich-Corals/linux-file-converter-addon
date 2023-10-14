converterVersion = "001000008" # Change the number if you want to trigger an update.
automaticUpdates = True # Replace the "True" with "False" if you don't want automatic updates.

from gi.repository import Nautilus, GObject
from typing import List
from PIL import Image, UnidentifiedImageError
from urllib.parse import urlparse, unquote
from pathlib import Path
import pathlib
import os, shlex
import urllib.request

try:
    import pyheif
except ImportError:
    print(f"WARNING(Nautilus-file-converter): \"pyheif\" not found, if you want to convert from heif format, install the package using \"pip install pyheif\". See the readme on GitHub for more information." )

try:
    import jxlpy
    from jxlpy import JXLImagePlugin
except ImportError:
    print(f"WARNING(Nautilus-file-converter): \"jxlpy\" not found, if you want to convert from- or to jxl format, install the package using \"pip install jxlpy\". See the readme on GitHub for more information.")

if automaticUpdates:
    with urllib.request.urlopen(
            "https://raw.githubusercontent.com/Lich-Corals/Nautilus-fileconverter-43/main/nautilus-fileconverter.py") as f:
        onlineFile = f.read().decode().strip()
    if converterVersion not in onlineFile:
        print("Updating...")
        currentPath = str(pathlib.Path(__file__).parent.resolve())
        if "/home/" in currentPath:
            fileUpdatePath = f"{currentPath}/{os.path.basename(__file__)}"
            with open(fileUpdatePath, 'w') as file:
                file.write(onlineFile)
        else:
            print("updating only supported in home!")

print = lambda *wish, **verbosity: None    # comment it out, if you wish debug printing

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
                          'image/webp',
                          'image/avif',
                          'image/heif',
                          'image/jxl')

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

    WRITE_FORMATS_IMAGE = [{'name': 'JPEG', 'extension': 'jpg'},
                           {'name': 'PNG'},
                           {'name': 'BMP'},
                           {'name': 'GIF'},
                           {'name': 'WebP'},
                           {'name': 'JXL'}]

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
        return [top_menuitem]


    def __get_extension(self, format):
        return f".{format.get('extension', format['name'])}".lower()


    def convert_image(self, menu, format, files):
        print(format)
        for file in files:
            file_path = Path(unquote(urlparse(file.get_uri()).path))
            try:
                image = Image.open(file_path)
                if (format['name']) == 'JPEG':
                    image = image.convert('RGB')
                image.save(file_path.with_suffix(self.__get_extension(format)),
                           format=(format['name']))
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
                    if (format['name']) == 'JPEG':
                        heif_image = heif_image.convert("RGB")
                    heif_image.save(file_path.with_suffix(self.__get_extension(format)), format['name'])
                except UnidentifiedImageError:
                    pass
                pass


    def convert_audio(self, menu, format, files):
        print(format)
        for file in files:
            from_file_path = Path(unquote(urlparse(file.get_uri()).path))
            to_file_path = from_file_path.with_suffix(self.__get_extension(format).lower())
            count = 0
            to_file_path_mod = from_file_path.with_name(f"{from_file_path.stem}")
            while to_file_path_mod.exists() or to_file_path.exists():
                count = count + 1
                to_file_path_mod = from_file_path.with_name(f"{from_file_path.stem}({count}){self.__get_extension(format).lower()}")
                print(shlex.quote(str(from_file_path)))
                to_file_path = to_file_path_mod
            os.system(
                f"nohup ffmpeg -i {shlex.quote(str(from_file_path))} -strict experimental -c:v libvpx-vp9 -crf 18 -preset slower -b:v 4000k {shlex.quote(str(to_file_path))} | tee &")
    def convert_video(self, menu, format, files):
        # use same ffmpeg backend
        self.convert_audio(menu, format, files)