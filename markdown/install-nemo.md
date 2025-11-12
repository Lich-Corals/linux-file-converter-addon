# Installation for Nemo
This section will guide you through the installation for Nemo.

> [!IMPORTANT]  
> Make sure you have installed all [general dependencies](https://codeberg.org/Lich-Corals/linux-file-converter-addon/src/branch/main/markdown/install-dependencies.md) before you try to install the script.

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
You can either install the extension manually or with a one-liner.

### One-liner installation
Just run this command:
```bash
python3 -c "$(curl -sS https://raw.githubusercontent.com/Lich-Corals/linux-file-converter-addon/main/nautilus-fileconverter.py)" --install-for-nemo
```
Now go to the [next section](#enabling-the-action-in-nemo).

### Manual installation
- Download the nautilus-fileconverter.py and the nautilus-fileconverter.nemo_action file from the [release page](https://codeberg.org/Lich-Corals/linux-file-converter-addon/releases).
    - Git users can also get the repository with these commands[:](https://bit.ly/3BlS71b)
     ```bash
     git clone https://github.com/Lich-Corals/linux-file-converter-addon

     cd ./linux-file-converter-addon
     ```
- Copy the files into the ~/.local/share/nemo/actions folder:
     ```bash
     mv nautilus-fileconverter.py ~/.local/share/nemo/actions/linux-file-converter-addon.py
     mv nautilus-fileconverter.nemo_action ~/.local/share/nemo/actions/linux-file-converter-addon.nemo_action
     ```
- Give the script permission to be executed as script:
     ```bash
     chmod +x ~/.local/share/nemo/actions/nautilus-fileconverter.py
     ```

## Enabling the action in Nemo
 You may need to enable the action in Nemo's settings. To do so, you can open Nemo and go edit>Plugins (or press Alt+P) and check the checkbox labelled with "Convert to..." in the "Actions" area.