from gi.repository import Nautilus, GObject
from typing import List
from PIL import Image
from urllib.parse import urlparse, unquote
from pathlib import Path
import os, shlex

#print=lambda *wish, **verbosity: None    # comment it out, if you wish debug printing

class FileConverterMenuProvider(GObject.GObject, Nautilus.MenuProvider):
    READ_FORMATS_IMAGE = ('image/jpeg', 'image/png', 'image/bmp', 'application/postscript', 'image/gif',
                          'image/x-icon', 'image/x-pcx', 'image/x-portable-pixmap', 'image/tiff', 'image/x-xbm',
                          'image/x-xbitmap', 'video/fli', 'image/vnd.fpx', 'image/vnd.net-fpx',
                          'application/octet-stream', 'windows/metafile', 'image/x-xpixmap', 'image/webp')
    READ_FORMATS_AUDIO = ('audio/mpeg', 'audio/mpeg3', 'video/x-mpeg', 'audio/x-mpeg-3',
                          'audio/x-wav', 'audio/wav', 'audio/wave', 'audio/x-pn-wave', 'audio/vnd.wave', 'audio/x-mpegurl',
                          'audio/mp4', 'audio/mp4a-latm', 'audio/mpeg4-generic', 'audio/x-matroska',
                          'audio/aac', 'audio/aacp', 'audio/3gpp', 'audio/3gpp2', 'audio/ogg', 'audio/opus',
                          'audio/flac', 'audio/x-vorbis+ogg')
    READ_FORMATS_VIDEO = ('video/mp4', 'video/webm', 'video/x-matroska', 'video/avi', 'video/msvideo',
                          'video/x-msvideo')
    WRITE_FORMATS_IMAGE = [{'name': 'JPEG', 'mimes': ['image/jpeg']},
                           {'name': 'PNG', 'mimes': ['image/png']},
                           {'name': 'BMP', 'mimes': ['image/bmp']},
                           {'name': 'GIF', 'mimes': ['image/gif']},
                           {'name': 'WebP', 'mimes': ['image/webp']}]
    WRITE_FORMATS_AUDIO = [{'name': 'MP3', 'mimes': ['audio/mpeg', 'audio/mpeg3', 'video/x-mpeg', 'audio/x-mpeg-3']},
                           {'name': 'WAV', 'mimes': ['audio/x-wav', 'audio/wav', 'audio/wave', 'audio/x-pn-wave', 'audio/vnd.wave']},
                           {'name': 'AAC', 'mimes': ['audio/aac', 'audio/aacp', 'audio/3gpp', 'audio/3gpp2']},
                           {'name': 'FLAC', 'mimes': ['audio/flac']},
                           {'name': 'M4A', 'mimes': ['audio/mp4', 'audio/mp4a-latm', 'audio/mpeg4-generic']},
                           {'name': 'OGG', 'mimes': ['audio/ogg']},
                           {'name': 'OPUS', 'mimes': ['audio/opus']}]
    WRITE_FORMATS_VIDEO = [{'name': 'MP4', 'mimes': ['video/mp4']},
                           {'name': 'WebM', 'mimes': ['video/webm']},
                           {'name': 'MKV', 'mimes': ['video/x-matroska']},
                           {'name': 'AVI', 'mimes': ['video/avi', 'video/msvideo', 'video/x-msvideo']},
                           {'name': 'GIF', 'mimes': ['image/gif']},
                           {'name': 'MP3', 'mimes': ['audio/mpeg3']},
                           {'name': 'WAV', 'mimes': ['audio/x-wav']}]


    def get_file_items(self, files) -> List[Nautilus.MenuItem]:
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


    def convert_image(self, menu, mime_output, files):
        print(mime_output)
        for file in files:
            file_path = Path(unquote(urlparse(file.get_uri()).path))
            image = Image.open(file_path)
            if (mime_output['name']) == 'JPEG':
                image = image.convert('RGB')
            image.save(file_path.with_suffix('.' + mime_output['name'].lower()),
                       format=(mime_output['name']))
    def convert_audio(self, menu, mime_output, files):
        print(mime_output)
        for file in files:
            from_file_path = Path(unquote(urlparse(file.get_uri()).path))
            to_file_path = from_file_path.with_suffix(
                f".{mime_output['name']}")
            os.system(
                f"nohup ffmpeg -i {shlex.quote(str(from_file_path))} -strict experimental {shlex.quote(str(to_file_path))} | tee &")
    def convert_video(self, menu, mime_output, files):
        # use same ffmpeg backend
        self.convert_audio(menu, mime_output, files)
