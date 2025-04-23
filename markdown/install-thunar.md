# Installation for Nemo
This section will guide you through the installation to Thunar file manager.
__Make sure you have installed all [general dependencies](https://github.com/Lich-Corals/linux-file-converter-addon/blob/main/markdown/install-dependencies.md) before you try to install the script.__
## Thunar specific dependencies
[Thunar](https://github.com/neilbrown/thunar) needs to be installed.

## Installation
- Download the nautilus-fileconverter.py file from the [release page](https://github.com/Lich-Corals/linux-file-converter-addon/releases).
    - Git users can also get the repository with these commands[:](https://bit.ly/3BlS71b)
     ```bash
     git clone https://github.com/Lich-Corals/linux-file-converter-addon

     cd ./linux-file-converter-addon
     ```
- Copy the file into the ~/.local/bin folder:
     ```bash
     mv nautilus-fileconverter.py ~/.local/bin/nautilus-fileconverter.py
     ```
     Note: you can place the file anywhere you want. The guide will continue with .local/bin location.
- Give the script permission to be executed as script:
     ```bash
     chmod +x ~/.local/bin/nautilus-fileconverter.py
     ```

## Enable the action in Thunar
- Open Thunar and navigate Edit/Configure custom actions...
- Click the "+" button to add a new action
- Set the following Basic settings...
     - Name: Convert to...
     - Command: /home/linus/.local/bin/nautilus-fileconverter.py %f
- Set the following Appearance Conditions...
     - File Pattern: *
     - Range (min-max): *
     - [ ] Directories
     - [x] Audio Files
     - [x] Image Files
     - [ ] Text Files
     - [x] Video Files
     - [ ] Other Files

You should now see the 'Convert to...' action when selecting a image, audio or video file.
Note: It may occur to you that you don't see the action when selecting multiple files.

#### All sections
- [Main page](https://github.com/Lich-Corals/linux-file-converter-addon/blob/main/README.md)
- [Configuration](https://github.com/Lich-Corals/linux-file-converter-addon/blob/main/markdown/configuration.md)
- [Errorrs and warnings](https://github.com/Lich-Corals/linux-file-converter-addon/blob/main/markdown/errors-and-warnings.md)
- [Install dependencies](https://github.com/Lich-Corals/linux-file-converter-addon/blob/main/markdown/install-dependencies.md)
- [Installation for Nautilus](https://github.com/Lich-Corals/linux-file-converter-addon/blob/main/markdown/install-nautilus.md)
- [Installation for Nemo](https://github.com/Lich-Corals/linux-file-converter-addon/blob/main/markdown/install-nemo.md)
- __[Installation for Thunar](https://github.com/Lich-Corals/linux-file-converter-addon/blob/main/markdown/install-thunar.md)__
