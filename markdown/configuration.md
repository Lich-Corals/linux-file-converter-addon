# Configuration
The program can be configured using the  NFC43-Config.json file, which will be created in the installation dictionary when the script is executed for the first time.
Just modify the file, by changing the 'true' and 'false' values.
If the program is installed in a root location, you need to change the configuration inside the script.
<b>Don't forget to save your changes, and restart Nautilus after modifying the configuration!</b>
```bash
#Quit Nautilus
nautilus -q

#start it again, you can also use the normal launcher.
nohup nautilus & disown
```
## Automatic updates
Automatic updates are only working in the home dictionary. If you've installed the script at the system-wide location, you may turn off automatic updates.
<br/><br/>To <b>turn off automatic updates</b>, open the config file with a text editor and set the `automaticUpdates` variable to 'false'.
To <b>manually trigger a self-update</b>, just open the .py file with a text editor and change the value of the `converterVersion` variable.
To turn off the <b>update pop-up</b>, open the config file with a text editor and set the `showPatchNotes` variable to 'false'.

## Shown menu items
To turn off the <b>patch note button</b> in the context menu and the <b>version number</b> in the adaption window, open the config file with a text editor and set the `showPatchNoteButton` variable to 'false'.
<br/><br/>To turn off the <b>Configure NFC43 button</b> in the context menu and the <b>config hint</b> in the adaption window, open the config file with a text editor and set the `showConfigHint` variable to 'false'.
<br/><br/>To turn off the '<b>convert to square</b>' option, open the config file with a text editor and set the `convertToSquares` variable to 'false'.
<br/><br/>To turn off the '<b>convert to wallpaper</b>' function, open the config file with a text editor and set the `convertToWallpapers` variable to 'false'.

## Other options
<br/>To turn off the <b>Double script installation Warning</b>, open the config file with a text editor and set the `checkForDoubleInstallation` variable to 'false'.
Note: This option may be a bit buggy in Nemo, I'll fix it in the future if it appears to be annoying to some users.
<br/>To turn off the __addition of timestamps__ to filenames, open the config file with a text editor and set the `timeInNames` variable to ‘false’.

## Adaption specific options (Nemo)
<br/>To enable the conversion of <b>application/octet-stream</b> files in the adaption version, set the `convertFromOctetStream` option to 'true'.
<br/>To disable the <b>"-" option</b> in the dropdown-list, set the `showDummyOption` setting to 'false'.

#### All sections
- [Main page](https://github.com/Lich-Corals/linux-file-converter-addon/blob/main/README.md)
- __[Configuration](https://github.com/Lich-Corals/linux-file-converter-addon/blob/main/markdown/configuration.md)__
- [Errorrs and warnings](https://github.com/Lich-Corals/linux-file-converter-addon/blob/main/markdown/errors-and-warnings.md)
- [Install dependencies](https://github.com/Lich-Corals/linux-file-converter-addon/blob/main/markdown/install-dependencies.md)
- [Installation for Nautilus](https://github.com/Lich-Corals/linux-file-converter-addon/blob/main/markdown/install-nautilus.md)
- [Installation for Nemo](https://github.com/Lich-Corals/linux-file-converter-addon/blob/main/markdown/install-nemo.md)
