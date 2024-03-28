# Installation for Nautilus
This section will guide you through the installation to Nautilus.
__Make sure you have installed all [general dependencies](https://github.com/Lich-Corals/linux-file-converter-addon/blob/main/markdown/install-dependencies.md) before you try to install the script.__
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
- Download the nautilus-fileconverter.py file from the [release page](https://github.com/Lich-Corals/linux-file-converter-addon/releases).
    - Git users can also get the repository with these commands[:](https://bit.ly/3BlS71b)
        ```bash
        git clone https://github.com/Lich-Corals/linux-file-converter-addon

        cd ./linux-file-converter-addon
        ```
- Move the script to the right location:
    <br><b>Important: Only use <i>one</i> of the following commands, otherwise you will get the menu-option twice!</b>
    - For a user specific installation move the file to '~/.local/share/nautilus-python/extensions/' using this command in the dictionary with the file:
      ```bash
      mv nautilus-fileconverter.py ~/.local/share/nautilus-python/extensions/nautilus-fileconverter.py
      ```
    - For a system-wide installation move the file to '/usr/share/nautilus-python/extensions/' using this command in the dictionary with the file:
        ```bash
        sudo mv nautilus-fileconverter.py /usr/share/nautilus-python/extensions/nautilus-fileconverter.py
        ```
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
- [Install dependencies](https://github.com/Lich-Corals/linux-file-converter-addon/blob/main/markdown/install-dependencies.md)
- __[Installation for Nautilus](https://github.com/Lich-Corals/linux-file-converter-addon/blob/main/markdown/install-nautilus.md)__
- [Installation for Nemo](https://github.com/Lich-Corals/linux-file-converter-addon/blob/main/markdown/install-nemo.md)
