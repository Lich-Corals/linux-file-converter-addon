# Installation for Thunar
This section will guide you through the installation for Thunar file manager.

> [!IMPORTANT]  
> Make sure you have installed all [general dependencies](https://codeberg.org/Lich-Corals/linux-file-converter-addon/src/branch/main/markdown/install-dependencies.md) before you try to install the script.

## Thunar specific dependencies
[Thunar](https://github.com/neilbrown/thunar) needs to be installed.

## Installation
You can either install the extension manually or with a one-liner.

### One-liner installation
Just run this command:
```bash
python3 -c "$(curl -sS https://codeberg.org/Lich-Corals/linux-file-converter-addon/raw/branch/main/nautilus-fileconverter.py)" --install-for-thunar
```
Now go to the [next section](#enable-the-action-in-thunar).

### Manual installation
- Download the nautilus-fileconverter.py file from the [release page](https://codeberg.org/Lich-Corals/linux-file-converter-addon/releases).
    - Git users can also get the repository with these commands[:](https://bit.ly/3BlS71b)
     ```bash
     git clone https://codeberg.org/Lich-Corals/linux-file-converter-addon

     cd ./linux-file-converter-addon
     ```
- Copy the file into the ~/.local/bin folder:
     ```bash
     mv nautilus-fileconverter.py ~/.local/bin/linux-file-converter-addon.py
     ```

> [!TIP]   
> You can place the file anywhere you want. The guide will continue with `.local/bin ` as the location for the script.

- Give the script permission to be executed as script:
     ```bash
     chmod +x ~/.local/bin/linux-file-converter-addon.py
     ```

## Enable the action in Thunar
- Open Thunar and navigate Edit>Configure custom actions...
- Click the "+" button to add a new action
- Set the following Basic settings...
     - Name: Convert to...
     - Command: /home/YOUR USERNAME/.local/bin/linux-file-converter-addon.py %f
- Set the following Appearance Conditions...
     - File Pattern: *
     - Range (min-max): *
     - [ ] Directories
     - [x] Audio Files
     - [x] Image Files
     - [ ] Text Files
     - [x] Video Files
     - [ ] Other Files

You should now see the 'Convert to...' action when selecting an image, audio or video file.

> [!NOTE]  
> It may occur to you that you don't see the action when selecting multiple files. This is an issue with Thunar.