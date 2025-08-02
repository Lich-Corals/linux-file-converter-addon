# Install dependencies
In this section, you can see which other software is needed to use the converter script and some of its extra features.

## Mandatory dependencies
[pip](https://pypi.org/project/pip/) is needed to install other dependencies; it can be installed with the following commands:

```bash
Debian based distros:
sudo apt install python3-pip

Fedora based distros:
sudo dnf install python3-pip

Arch based distros:
pacman -S python-pip
```

[ffmpeg](https://ffmpeg.org/download.html#build-linux) is needed to convert audio and video.

```bash
Debian based distros:
sudo apt install ffmpeg

Fedora based distros:
sudo dnf install ffmpeg

Arch based distros:
sudo pacman -S ffmpeg
```

### Pip dependencies
These dependencies need to be installed using pip. You can either do it manually or let the program automatically create a local venv with all dependencies.
If you want to install the dependencies manually, skip to [Manual Installation](#manual-installation) and optionally to [Optional dependencies](#optional-dependencies).

#### Automatic installation
The automatic installation will create a local venv and install the needed pip packages into it. This is especially useful if you cannot use pip for global installations because it conflicts with your system's package manager.  

Run this command for a full installation (with optional dependencies):
```bash
python3 -c "$(curl -sS https://raw.githubusercontent.com/Lich-Corals/linux-file-converter-addon/main/nautilus-fileconverter.py)" --create-venv --full
```
Or run this one to only install the mandatory dependencies:
```bash
python3 -c "$(curl -sS https://raw.githubusercontent.com/Lich-Corals/linux-file-converter-addon/main/nautilus-fileconverter.py)" --create-venv
```

> [!TIP]  
> In the case that the command `python3` isn't found, check the python installation or replace it with `python`.

> [!TIP]  
> If the script had an update and (optional) dependencies are added, you can just run the above command again to automatically add them to the venv.

> [!TIP]  
> Should any installations of dependencies fail, you can manually install them into the venv created by the program. It is located here: `~/.config/linux-file-converter-addon/venv`.

You can skip the following sections [Manual Installation](#manual-installation) and [Optional dependencies](#optional-dependencies) if you used automatic installation. Continue by installing the extension to the file manager of your choice.

#### Manual installation
[python-pillow](https://python-pillow.org/) is needed to convert images. It can be installed using pip:
```bash
pip install Pillow
```

[python-magic](https://pypi.org/project/python-magic/) will be used to detect the mime types of files:
```bash
pip install python-magic
```

## Optional dependencies
### pillow_heif (from HEIF, AVIF)
[pillow_heif](https://pypi.org/project/pillow-heif/) is needed if you want to convert from **HEIF** or **AVIF** format.
<br/> Install it using this command:
```bash
pip install pillow-heif
```

### pillow-avif-plugin (to AVIF)
In addition, to convert **to AVIF** format you will need this [plugin for Pillow](https://pypi.org/project/pillow-avif-plugin/).
```bash
pip install pillow-avif-plugin
```

### jxlpy (JXL)
[jxlpy](https://github.com/olokelo/jxlpy) is needed if you want to convert from **JXL** format.
<br/> Install it using this command:
```bash
pip install jxlpy
```

> [!NOTE]
> Jxlpy is in a very early state, you may have issues while installing it using pip. In this case you need to [install it manually](https://github.com/olokelo/jxlpy#build-it-yourself).

#### All sections
- [Main page](https://github.com/Lich-Corals/linux-file-converter-addon/blob/main/README.md)
- [Configuration](https://github.com/Lich-Corals/linux-file-converter-addon/blob/main/markdown/configuration.md)
- [Errorrs and warnings](https://github.com/Lich-Corals/linux-file-converter-addon/blob/main/markdown/errors-and-warnings.md)
- [TL;DR installation guide](https://github.com/Lich-Corals/linux-file-converter-addon/blob/main/markdown/tldr-installation.md)
- __[Install dependencies](https://github.com/Lich-Corals/linux-file-converter-addon/blob/main/markdown/install-dependencies.md)__
- [Installation for Nautilus](https://github.com/Lich-Corals/linux-file-converter-addon/blob/main/markdown/install-nautilus.md)
- [Installation for Nemo](https://github.com/Lich-Corals/linux-file-converter-addon/blob/main/markdown/install-nemo.md)
- [Installation for Thunar](https://github.com/Lich-Corals/linux-file-converter-addon/blob/main/markdown/install-thunar.md)
- [Installation for Dolphin](https://github.com/Lich-Corals/linux-file-converter-addon/blob/main/markdown/install-dolphin.md)