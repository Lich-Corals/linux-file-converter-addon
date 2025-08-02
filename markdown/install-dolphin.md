# Installation for Dolphin
This section will guide you through the installation for Dolphin file manager.

> [!IMPORTANT]  
> Make sure you have installed all [general dependencies](https://github.com/Lich-Corals/linux-file-converter-addon/blob/main/markdown/install-dependencies.md) before you try to install the script.

## Dolphin specific dependencies
[Dolphin](https://apps.kde.org/en-gb/dolphin/) needs to be installed.

## Installation
You can either install the extension manually or with a one-liner.

### One-liner installation
Just run this command:
```bash
python3 -c "$(curl -sS https://raw.githubusercontent.com/Lich-Corals/linux-file-converter-addon/main/nautilus-fileconverter.py)" --install-for-dolphin
```
Now go to the [next section](#enable-the-action-in-thunar).

### Manual installation
- Download the nautilus-fileconverter.py file from the [release page](https://github.com/Lich-Corals/linux-file-converter-addon/releases).
    - Git users can also get the repository with these commands[:](https://bit.ly/3BlS71b)
     ```bash
     git clone https://github.com/Lich-Corals/linux-file-converter-addon

     cd ./linux-file-converter-addon
     ```
- Copy two files into the into their new directories:
     ```bash
     mv nautilus-fileconverter.py ~/.local/bin/linux-file-converter-addon.py
     mv linux-file-converter-addon.kde_servicemenu ~/.local/share/kio/servicemenus/linux-file-converter-addon.desktop
     ```

> [!TIP]   
> You can place the script file anywhere you want. The guide will continue with `.local/bin `.

- Give the script and servicemenu permission to be executed:
     ```bash
     chmod +x ~/.local/bin/linux-file-converter-addon.py
     chmod +x ~/.local/share/kio/servicemenus/linux-file-converter-addon.desktop
     ```

You should now see the 'Convert to...' option when selecting an image, audio or video file in Dolphin.

#### All sections
- [Main page](https://github.com/Lich-Corals/linux-file-converter-addon/blob/main/README.md)
- [Configuration](https://github.com/Lich-Corals/linux-file-converter-addon/blob/main/markdown/configuration.md)
- [Errorrs and warnings](https://github.com/Lich-Corals/linux-file-converter-addon/blob/main/markdown/errors-and-warnings.md)
- [TL;DR installation guide](https://github.com/Lich-Corals/linux-file-converter-addon/blob/main/markdown/tldr-installation.md)
- [Install dependencies](https://github.com/Lich-Corals/linux-file-converter-addon/blob/main/markdown/install-dependencies.md)
- [Installation for Nautilus](https://github.com/Lich-Corals/linux-file-converter-addon/blob/main/markdown/install-nautilus.md)
- [Installation for Nemo](https://github.com/Lich-Corals/linux-file-converter-addon/blob/main/markdown/install-nemo.md)
- [Installation for Thunar](https://github.com/Lich-Corals/linux-file-converter-addon/blob/main/markdown/install-thunar.md)
- __[Installation for Dolphin](https://github.com/Lich-Corals/linux-file-converter-addon/blob/main/markdown/install-dolphin.md)__

