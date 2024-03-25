# Install dependencies
## 2.1 Dependencies
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
###

[ffmpeg](https://ffmpeg.org/download.html#build-linux) is needed to convert audio and video.

```bash
Debian based distros:
sudo apt install ffmpeg

Fedora based distros:
sudo dnf install ffmpeg

Arch based distros:
sudo pacman -S ffmpeg
```

## 2.2 Optional dependencies
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
