# Installation for Nemo
This section will guide you through the installation to Nemo.
__Make sure you have installed all [general dependencies](https://github.com/Lich-Corals/linux-file-converter-addon/blob/main/markdown/install-dependencies.md) before you try to install the script.__
## Nemo specific dependencies
[Nemo](https://github.com/linuxmint/nemo) needs to be installed.
```bash
Debian based distros:
sudo apt install nemo

Fedora based distros:
sudo dnf install nemo

Arch based distros:
sudo pacman -S nemo
```

## Installation
- Download the nautilus-fileconverter.py and the nautilus-fileconverter.nemo_action file from the [release page](https://github.com/Lich-Corals/linux-file-converter-addon/releases).
    - Git users can also get the repository with these commands[:](https://bit.ly/3BlS71b)
     ```bash
     git clone https://github.com/Lich-Corals/linux-file-converter-addon

     cd ./linux-file-converter-addon
     ```
- Copy the files into the ~/.local/share/nemo/actions folder:
     ```bash
     mv nautilus-fileconverter.py ~/.local/share/nemo/actions/nautilus-fileconverter.py
     mv nautilus-fileconverter.nemo_action ~/.local/share/nemo/actions/nautilus-fileconverter.nemo_action
     ```
- Give the script permission to be executed as script:
     ```bash
     chmod +x ~/.local/share/nemo/actions/nautilus-fileconverter.py
     ```
 You may need to enable the action in Nemo's settings. To do so, you can open Nemo and go edit>Plugins (or press Alt+P) and check the checkbox labelled with "Convert to..." in the "Actions" area.

#### All sections
- [Main page](https://github.com/Lich-Corals/linux-file-converter-addon/blob/main/README.md)
- [Configuration](https://github.com/Lich-Corals/linux-file-converter-addon/blob/main/markdown/configuration.md)
- [Errorrs and warnings](https://github.com/Lich-Corals/linux-file-converter-addon/blob/main/markdown/errors-and-warnings.md)
- [Install dependencies](https://github.com/Lich-Corals/linux-file-converter-addon/blob/main/markdown/install-dependencies.md)
- [Installation for Nautilus](https://github.com/Lich-Corals/linux-file-converter-addon/blob/main/markdown/install-nautilus.md)
- __[Installation for Nemo](https://github.com/Lich-Corals/linux-file-converter-addon/blob/main/markdown/install-nemo.md)__
- [Installation for Thunar](https://github.com/Lich-Corals/linux-file-converter-addon/blob/main/markdown/install-thunar.md)
