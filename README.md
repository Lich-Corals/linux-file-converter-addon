
# linux-file-converter-addon
[![](https://img.shields.io/endpoint?style=for-the-badge&url=https%3A%2F%2Flichcorals.netlify.app%2Fgnome_look.json)](https://www.gnome-look.org/s/Gnome/p/1965601)

![converterAddon-1](https://github.com/Lich-Corals/linux-file-converter-addon/assets/111392332/a248112e-1774-4e8d-a637-0302d9b67c77)
<img src="https://user-images.githubusercontent.com/111392332/226464712-216ef143-6ca7-4c9d-ac15-e51e3a299550.png" alt="drawing" height="256"/>

# Features
Convert between various image, audio and video formats using the context menu. The addon is written in Python and available for **Nautilus** and **Nemo** file viewers. It adds a new option to the context menu to create an easy way to convert between a huge amount of file types.
The program offers many options to customise the appearance of its context menu. There are also a few extra formats which can be added by installing optional dependencies.
The tool has a built-in auto-update function to make sure the newest version is always installed.
Note that the Nemo port is quite new and not as well tested as the Nautilus version. If you experience any problems, please report them on the [issue page](https://github.com/Lich-Corals/linux-file-converter-addon/issues/new/choose).
```mermaid
    flowchart TD
    A[Supported Image Files]
    B[Supported Audio Files]
    C[Supported Video Files]
    D[image]
    E[audio]
    F[video]

    A["JPG<br/>JPEG<br/>JPE<br/>PNG<br/>BMP<br/>AI<br/>EPS<br/>PS<br/>GIF<br/>ICO<br/>PCX<br/>PPM<br/>TIFF<br/>TIF<br/>XBM<br/>FLI<br/>FPX<br/>BIN<br/>WMF<br/>XPM<br/>WEBP<br/>AVIF¹<br/>HEIC¹<br/>JXL²"]
    B["MP3<br/>MPGA<br/>MPG<br/>MPEG<br/>WAV<br/>M3U<br/>M3U8<br/>M4A<br/>MKA<br/>AAC<br/>3GP<br/>3G2<br/>OGG<br/>OPUS"]
    C["MP4<br/>WebM<br/>MKV<br/>AVI<br/>MOV<br/>QT"]

    D["JPEG<br/>PNG<br/>BMP<br/>GIF<br/>WEBP<br/>JXL²<br/>TIFF<br/>AVIF³<br/>Different square sizes<br/>Different wallpaper sizes"]
    E["MP3<br/>WAV<br/>ACC<br/>FLAC<br/>M4A<br/>OGG<br/>OPUS"]
    F["MP4<br/>WebM<br/>MKV<br/>AVI<br/>MP3<br/>WAV"]

    A --> D
    B --> E
    C --> F
```
¹ [Needs pyheif](https://github.com/Lich-Corals/linux-file-converter-addon/blob/main/markdown/install-dependencies.md#pyheif-heic-avif).
<br/>² [Needs jxlpy](https://github.com/Lich-Corals/linux-file-converter-addon/blob/main/markdown/install-dependencies.md#jxlpy-jxl).
<br/>³ [Needs pillow-avif-plugin](https://github.com/Lich-Corals/linux-file-converter-addon/blob/main/markdown/install-dependencies.md#pillow-avif-plugin-to-avif).

# Installation
Please head over to the installation page for your file manager:
- [Nautilus](https://github.com/Lich-Corals/linux-file-converter-addon/blob/main/markdown/install-nautilus.md)
- [Nemo](https://github.com/Lich-Corals/linux-file-converter-addon/blob/main/markdown/install-nemo.md)

# Updating
If the script is installed in the home folder or has permissions to write in it's dictionary, it will update automatically as long as automatic updates aren't disabled.

If automatic updates are disabled, you can run the installation commands again to update the program.
# Usage

Just right-click on any supported file and choose the "Convert to..." option. In this sub menu you can select any file type you want to convert to.

Converting a file can take some time. There is no indicator when the process is done.

If you experience any issues with the extension, please report it on the [issues](https://github.com/Lich-Corals/linux-file-converter-addon/issues) page.

# Any questions?
If anything is not clear...
<br/>If you have a problem...
<br/>If you need a specific feature...
<br/>If any of your files are not supported...
<br/><b>Check if anyone had the same issue before [on this page](https://github.com/Lich-Corals/linux-file-converter-addon/issues?q=) or feel free to open a new [GitHub issue](https://github.com/Lich-Corals/linux-file-converter-addon/issues/new/choose)!</b>

# Credits
- [Linus Tibert](https://github.com/Lich-Corals)
  <br>Maintenance, issues, support
- [derVedro](https://github.com/derVedro)
  <br>Pull requests, issue solving
- [D10f](https://github.com/D10f)
  <br>Pull requests

#### All sections
- __[Main page](https://github.com/Lich-Corals/linux-file-converter-addon/blob/main/README.md)__
- [Configuration](https://github.com/Lich-Corals/linux-file-converter-addon/blob/main/markdown/configuration.md)
- [Errorrs and warnings](https://github.com/Lich-Corals/linux-file-converter-addon/blob/main/markdown/errors-and-warnings.md)
- [Install dependencies](https://github.com/Lich-Corals/linux-file-converter-addon/blob/main/markdown/install-dependencies.md)
- [Installation for Nautilus](https://github.com/Lich-Corals/linux-file-converter-addon/blob/main/markdown/install-nautilus.md)
- [Installation for Nemo](https://github.com/Lich-Corals/linux-file-converter-addon/blob/main/markdown/install-nemo.md)
