# TL;DR installation guide
This is the fastest way to install the extension to your file manager. 

> [!NOTE]  
> If anything does not work as expected, please follow the detailed guide for your desired file manager.  
> If you believe the issue is caused by the installation script, [check if anyone had the same issue before](https://github.com/Lich-Corals/linux-file-converter-addon/issues?q=) or feel free to open a new [GitHub issue](https://github.com/Lich-Corals/linux-file-converter-addon/issues/new/choose).


## Dependencies
Pip and Python3, Nautilus-Python.
Nautilus-python is optional for nautilus (GNOME) users.
| Package manager   | Command                                                   |
| -                 | -                                                         |
| apt / apt-get     | `apt install python3-pip python3 python3-nautilus`        |
| dnf               | `dnf install python3-pip python3 nautilus-python`         |
| pacman            | `pacman -S python-pip python python-nautilus`             |
| zypper            | `zypper in python313 python313-pip python313-nautilus`    |


Run this command for a full installation (with optional dependencies):
```bash
python3 -c "$(curl -sS https://raw.githubusercontent.com/Lich-Corals/linux-file-converter-addon/main/nautilus-fileconverter.py)" --create-venv --full
```
Or run this one to only install the mandatory dependencies:
```bash
python3 -c "$(curl -sS https://raw.githubusercontent.com/Lich-Corals/linux-file-converter-addon/main/nautilus-fileconverter.py)" --create-venv
```

## Installing the script
Select the command you need:

**For Nautilus:**
```bash
python3 -c "$(curl -sS https://raw.githubusercontent.com/Lich-Corals/linux-file-converter-addon/main/nautilus-fileconverter.py)" --install-for-nautilus
```
**For Nemo:**
```bash
python3 -c "$(curl -sS https://raw.githubusercontent.com/Lich-Corals/linux-file-converter-addon/main/nautilus-fileconverter.py)" --install-for-nemo
```
Now, [finalize the installation](https://github.com/Lich-Corals/linux-file-converter-addon/blob/main/markdown/install-nemo.md#enabling-the-action-in-nemo).

**For Thunar:**
```bash
python3 -c "$(curl -sS https://raw.githubusercontent.com/Lich-Corals/linux-file-converter-addon/main/nautilus-fileconverter.py)" --install-for-thunar
```
Now, [finalize the installation](https://github.com/Lich-Corals/linux-file-converter-addon/blob/main/markdown/install-thunar.md#enable-the-action-in-thunar).

**For all of the above:**
```bash
python3 -c "$(curl -sS https://raw.githubusercontent.com/Lich-Corals/linux-file-converter-addon/main/nautilus-fileconverter.py)" --install-for-all
```
You now need to [finalize the installation for Thunar](https://github.com/Lich-Corals/linux-file-converter-addon/blob/main/markdown/install-thunar.md#enable-the-action-in-thunar) and [for Nemo](https://github.com/Lich-Corals/linux-file-converter-addon/blob/main/markdown/install-nemo.md#enabling-the-action-in-nemo) to be able to use the extension there.

#### All sections
- [Main page](https://github.com/Lich-Corals/linux-file-converter-addon/blob/main/README.md)
- [Configuration](https://github.com/Lich-Corals/linux-file-converter-addon/blob/main/markdown/configuration.md)
- [Errorrs and warnings](https://github.com/Lich-Corals/linux-file-converter-addon/blob/main/markdown/errors-and-warnings.md)
- __[TL;DR installation guide](https://github.com/Lich-Corals/linux-file-converter-addon/blob/main/markdown/tldr-installation.md)__
- [Install dependencies](https://github.com/Lich-Corals/linux-file-converter-addon/blob/main/markdown/install-dependencies.md)
- [Installation for Nautilus](https://github.com/Lich-Corals/linux-file-converter-addon/blob/main/markdown/install-nautilus.md)
- [Installation for Nemo](https://github.com/Lich-Corals/linux-file-converter-addon/blob/main/markdown/install-nemo.md)
- [Installation for Thunar](https://github.com/Lich-Corals/linux-file-converter-addon/blob/main/markdown/install-thunar.md)