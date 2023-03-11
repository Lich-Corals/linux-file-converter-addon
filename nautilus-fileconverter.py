from gi.repository import Nautilus, GObject
from typing import List
from PIL import Image
from urllib.parse import urlparse, unquote
from pathlib import Path
import os, shlex

#print=lambda *wish, **verbosity: None    # comment it out, if you wish debug printing

class ExampleMenuProvider(GObject.GObject, Nautilus.MenuProvider):
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
    def get_file_items(
            self,
            files,
            WRITE_FORMATS_IMAGE=("x"),
            WRITE_FORMATS_AUDIO=("x"),
            WRITE_FORMATS_VIDEO=("x"),
     ) -> List[Nautilus.MenuItem]:
        for file in files:
            print(file.get_mime_type())
            if file.get_mime_type() in self.READ_FORMATS_IMAGE:
                WRITE_FORMATS_IMAGE = [{'name': 'JPEG', 'mimes': ['image/jpeg']},
                                       {'name': 'PNG', 'mimes': ['image/png']},
                                       {'name': 'BMP', 'mimes': ['image/bmp']},
                                       #{'name': 'PDF', 'mimes': ['application/pdf']},
                                       {'name': 'GIF', 'mimes': ['image/gif']},
                                       #{'name': 'ICO', 'mimes': ['image/x-icon']},
                                       {'name': 'WebP', 'mimes': ['image/webp']}
                                       #{'name': 'EPS', 'mimes': ['application/postscript']}
                                        ]
                LISTED_FORMATS = ["foo", "bar"]
                top_menuitem = Nautilus.MenuItem(
                    name="ExampleMenuProvider::convert_to",
                    label="Convert to...",
                    tip="",
                    icon="",
                )
                submenu = Nautilus.Menu()
                top_menuitem.set_submenu(submenu)
                for IMAGE_FORMATS in WRITE_FORMATS_IMAGE:
                    if IMAGE_FORMATS not in LISTED_FORMATS:
                        LISTED_FORMATS.append(IMAGE_FORMATS)
                        sub_menuitem = Nautilus.MenuItem(
                            name='ExampleMenuProvider::bar' + IMAGE_FORMATS['name'],
                            label=(IMAGE_FORMATS['name']),
                            tip="",
                            icon="",
                        )
                        sub_menuitem.connect('activate', self.convert_image, IMAGE_FORMATS, files)
                        submenu.append_item(sub_menuitem)
                return [
                    top_menuitem,
                ]
            if file.get_mime_type() in self.READ_FORMATS_AUDIO:
                WRITE_FORMATS_AUDIO = [{'name': 'MP3', 'mimes': ['audio/mpeg', 'audio/mpeg3', 'video/x-mpeg', 'audio/x-mpeg-3']},
                               {'name': 'WAV', 'mimes': ['audio/x-wav', 'audio/wav', 'audio/wave', 'audio/x-pn-wave', 'audio/vnd.wave']},
                               {'name': 'AAC', 'mimes': ['audio/aac', 'audio/aacp', 'audio/3gpp', 'audio/3gpp2']},
                               {'name': 'FLAC', 'mimes': ['audio/flac']},
                               {'name': 'M4A', 'mimes': ['audio/mp4', 'audio/mp4a-latm', 'audio/mpeg4-generic']},
                               {'name': 'OGG', 'mimes': ['audio/ogg']},
                               {'name': 'OPUS', 'mimes': ['audio/opus']}]
                LISTED_FORMATS = ["foo", "bar"]
                top_menuitem = Nautilus.MenuItem(
                    name="ExampleMenuProvider::convert_to",
                    label="Convert to...",
                    tip="",
                    icon="",
                )
                submenu = Nautilus.Menu()
                top_menuitem.set_submenu(submenu)
                for AUDIO_FORMATS in WRITE_FORMATS_AUDIO:
                    if AUDIO_FORMATS not in LISTED_FORMATS:
                        LISTED_FORMATS.append(AUDIO_FORMATS)
                        sub_menuitem = Nautilus.MenuItem(
                            name='ExampleMenuProvider::bar' + AUDIO_FORMATS['name'],
                            label=(AUDIO_FORMATS['name']),
                            tip="",
                            icon="",
                        )
                        sub_menuitem.connect('activate', self.convert_audio, AUDIO_FORMATS, files)
                        submenu.append_item(sub_menuitem)
                return [
                    top_menuitem,
                ]
            if file.get_mime_type() in self.READ_FORMATS_VIDEO:
                WRITE_FORMATS_VIDEO = [{'name': 'MP4', 'mimes': ['video/mp4']},
                                       {'name': 'WebM', 'mimes': ['video/webm']},
                                       {'name': 'MKV', 'mimes': ['video/x-matroska']},
                                       {'name': 'AVI', 'mimes': ['video/avi', 'video/msvideo', 'video/x-msvideo']},
                                       {'name': 'GIF', 'mimes': ['image/gif']},
                                       {'name': 'MP3', 'mimes': ['audio/mpeg3']},
                                       {'name': 'WAV', 'mimes': ['audio/x-wav']}]
                LISTED_FORMATS = ["foo", "bar"]
                top_menuitem = Nautilus.MenuItem(
                    name="ExampleMenuProvider::convert_to",
                    label="Convert to...",
                    tip="",
                    icon="",
                )
                submenu = Nautilus.Menu()
                top_menuitem.set_submenu(submenu)
                for VIDEO_FORMATS in WRITE_FORMATS_VIDEO:
                    if VIDEO_FORMATS not in LISTED_FORMATS:
                        LISTED_FORMATS.append(VIDEO_FORMATS)
                        sub_menuitem = Nautilus.MenuItem(
                            name='ExampleMenuProvider::bar' + VIDEO_FORMATS['name'],
                            label=(VIDEO_FORMATS['name']),
                            tip="",
                            icon="",
                        )
                        sub_menuitem.connect('activate', self.convert_audio, VIDEO_FORMATS, files)
                        submenu.append_item(sub_menuitem)
                return [
                    top_menuitem,
                ]
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
