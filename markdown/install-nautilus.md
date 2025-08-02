# Installation for Nautilus
This section will guide you through the installation for Nautilus.

> [!IMPORTANT]  
> Make sure you have installed all [general dependencies](https://github.com/Lich-Corals/linux-file-converter-addon/blob/main/markdown/install-dependencies.md) before you try to install the script.

## Nautilus specific dependencies
GNOME's file viewer [Nautilus](https://apps.gnome.org/en-GB/app/org.gnome.Nautilus/) should be installed, otherwise it will be hard to install extension to it.

[nautilus-python](https://github.com/GNOME/nautilus-python) needs to be installed to install extensions:

```bash
Debian based distros:
sudo apt install python3-nautilus

Fedora based distros:
sudo dnf install nautilus-python

Arch based distros:
sudo pacman -Sy python-nautilus
```

## Installation
You can either install the extension manually or with a one-liner.

### One-liner installation
Just run this command, and you are done:
```bash
python3 -c "$(curl -sS https://raw.githubusercontent.com/Lich-Corals/linux-file-converter-addon/main/nautilus-fileconverter.py)" --install-for-nautilus
```
Nautilus will quit at the end of the installation. This is intended and necessary for the extension to get activated.

### Manual installation
- Download the nautilus-fileconverter.py file from the [release page](https://github.com/Lich-Corals/linux-file-converter-addon/releases).
    - Git users can also get the repository with these commands[:](https://bit.ly/3BlS71b)
        ```bash
        git clone https://github.com/Lich-Corals/linux-file-converter-addon

        cd ./linux-file-converter-addon
        ```
- Move the script to the right location:

> [!CAUTION]  
> Only use <i>one</i> of the following commands, otherwise you will get the menu-option in Nautilus twice!</b>
    
    - For a user specific installation move the file to '~/.local/share/nautilus-python/extensions/' using this command in the dictionary with the file:
      ```bash
      mv nautilus-fileconverter.py ~/.local/share/nautilus-python/extensions/nautilus-fileconverter.py
      ```
    - For a system-wide installation move the file to '/usr/share/nautilus-python/extensions/' using this command in the dictionary with the file:
        ```bash
        sudo mv nautilus-fileconverter.py /usr/share/nautilus-python/extensions/nautilus-fileconverter.py
        ```

> [!IMPORTANT]  
> Automatic updates are limited for root installations; I recommend the other installation option. More information is available in the [errors and warnings section](https://github.com/Lich-Corals/linux-file-converter-addon/blob/main/markdown%2Ferrors-and-warnings.md#003-no-permission-to-self-update).

- Now you only have to restart Nautilus using the following commands:
    ```bash
   #Quit Nautilus
   nautilus -q

   #start it again, you can also use the normal launcher.
   nohup nautilus & disown
    ```

#### All sections
- [Main page](https://github.com/Lich-Corals/linux-file-converter-addon/blob/main/README.md)
- [Configuration](https://github.com/Lich-Corals/linux-file-converter-addon/blob/main/markdown/configuration.md)
- [Errorrs and warnings](https://github.com/Lich-Corals/linux-file-converter-addon/blob/main/markdown/errors-and-warnings.md)
- [TL;DR installation guide](https://github.com/Lich-Corals/linux-file-converter-addon/blob/main/markdown/tldr-installation.md)
- [Install dependencies](https://github.com/Lich-Corals/linux-file-converter-addon/blob/main/markdown/install-dependencies.md)
- __[Installation for Nautilus](https://github.com/Lich-Corals/linux-file-converter-addon/blob/main/markdown/install-nautilus.md)__
- [Installation for Nemo](https://github.com/Lich-Corals/linux-file-converter-addon/blob/main/markdown/install-nemo.md)
- [Installation for Thunar](https://github.com/Lich-Corals/linux-file-converter-addon/blob/main/markdown/install-thunar.md)
- [Installation for Dolphin](https://github.com/Lich-Corals/linux-file-converter-addon/blob/main/markdown/install-dolphin.md)