# Install dependencies
In this section, you can see which other software is needed to use the converter script and some of its extra features.

## Necessary dependencies
[pip](https://pypi.org/project/pip/) is a pre-dependency for pillow, it can be installed with the following commands:

```bash
Debian based distros:
sudo apt install python3-pip

Fedora based distros:
sudo dnf install python3-pip

Arch based distros:
pacman -S python-pip
```

[python-pillow](https://python-pillow.org/) is needed to convert images. It can be installed using pip:
```bash
pip install Pillow
```

[python-magic](https://pypi.org/project/python-magic/) will be used to detect the mimetypes of files:
```bash
pip install python-magic
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

## Optional dependencies
### pyheif (HEIC, AVIF)
[pyheif](https://pypi.org/project/pyheif/) is needed if you want to convert from **heif** or **avif** format.
<br/> Install it using this command:
```bash
pip install pyheif
```
You may need to install some dependencies before installing pyheif. Otherwise you could get an error installing it.
```bash
yum install libffi libheif-devel libde265-devel
```
### pillow-avif-plugin (to AVIF)
In addition, to convert *to* **avif** format you will need this [plugin for Pillow](https://pypi.org/project/pillow-avif-plugin/).
```bash
pip install pillow-avif-plugin
```

### jxlpy (JXL)
[jxlpy](https://github.com/olokelo/jxlpy) is needed if you want to convert from **jxl** format.
<br/> Install it using this command:
```bash
pip install jxlpy
```
Note: jxlpy is in a very early state, you may have issues while installing it using pip.
You may need to [install it manually](https://github.com/olokelo/jxlpy#build-it-yourself).

#### All sections
- [Main page](https://github.com/Lich-Corals/linux-file-converter-addon/blob/main/README.md)
- [Configuration](https://github.com/Lich-Corals/linux-file-converter-addon/blob/main/markdown/configuration.md)
- [Errorrs and warnings](https://github.com/Lich-Corals/linux-file-converter-addon/blob/main/markdown/errors-and-warnings.md)
- __[Install dependencies](https://github.com/Lich-Corals/linux-file-converter-addon/blob/main/markdown/install-dependencies.md)__
- [Installation for Nautilus](https://github.com/Lich-Corals/linux-file-converter-addon/blob/main/markdown/install-nautilus.md)
- [Installation for Nemo](https://github.com/Lich-Corals/linux-file-converter-addon/blob/main/markdown/install-nemo.md)
