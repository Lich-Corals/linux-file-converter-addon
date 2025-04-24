# Errors and warnings
This section will hopefully be helpful, if you experience problems with the plugin.
## WARNING(Nautilus-file-converter)(XXX):
### (100): "pillow_heif" not found
<b>Causes:</b><br/>
This warning is caused, because the script is not able to find your pillow_heif installation.
<br/><br/><b>Possible Effects:</b><br/>
Without pyheif, the converter won't be able to convert from heif file format.
<br/><br/><b>How to solve?</b><br/>
To solve this warning, you need to install pillow_heif using pip.
<br/>View the [Optional dependencies](https://github.com/Lich-Corals/linux-file-converter-addon/blob/main/markdown/install-dependencies.md#optional-dependencies) section to get installation instructions.

### (101): "jxlpy" not found
<b>Causes:</b><br/>
This warning is caused, because the script is not able to find your jxlpy installation.
<br/><br/><b>Possible Effects:</b><br/>
Without jxlpy, the converter won't be able to convert from- or to jxl file format.
<br/><br/><b>How to solve?</b><br/>
To solve this warning, you need to install jxlpy using pip.
<br/>View the [Optional dependencies](https://github.com/Lich-Corals/linux-file-converter-addon/blob/main/markdown/install-dependencies.md#optional-dependencies) section to get installation instructions.

### (102): "pillow-avif-plugin" not found
<b>Causes:</b><br/>
This warning is caused, because the script is not able to find your pillow-avif-plugin installation.
<br/><br/><b>Possible Effects:</b><br/>
Without pillow-avif-plugin, the converter won't be able to convert to avif file format.
<br/><br/><b>How to solve?</b><br/>
To solve this warning, you need to install pillow-avif-plugin using pip.
<br/>View the [Optional dependencies](https://github.com/Lich-Corals/linux-file-converter-addon/blob/main/markdown/install-dependencies.md#optional-dependencies) section to get installation instructions.

### (103): Double script installation detected
<b>Causes:</b><br/>
The script is installed in a home location and finds another script with the same name in the root installation folder ("/usr/share/nautilus-python/extensions/").
<br/><br/><b>Possible Effects:</b><br/>
The context menu may appear two times.
<br/><br/><b>How to solve?</b><br/>
To solve this issue, you have to remove one of the files (in "/usr/share/nautilus-python/extensions/" or in "~/.local/share/nautilus-python/extensions/")

### (104): Attempting to update
<b>Causes:</b><br/>
Automatic updates are enabled and there are updates available.
This is not an error, just information to make problems easier to solve.

## ERROR(Nautilus-file-converter)(XXX):
### (400): is in an unconvertable file-format.
<b>Causes:</b><br/>
A file you wanted to convert can't be read by the program.
Such a file may be in between other files you converted.
<br/><br/><b>Possible Effects:</b><br/>
The mentioned file can not be converted by this extension.
<br/><br/><b>How to solve?</b><br/>
You may open an issue to request the file format of the file you want to convert.

### (401): Something went wrong while loading or updating the configuration file.
<b>Causes:</b><br/>
An error occurred during the update process of the config file.
<br/><br/><b>Possible Effects:</b><br/>
The config file may be missing some settings added by an update; some settings may be out of sync or using the default value.
<br/><br/><b>How to solve?</b><br/>
Consider checking the write-permissions for the `~/.config/linux-file-converter-addon/config.json` file.
If you can't solve the issue on your own, you can open an issue on Github.

### (402): No permission to self-update
<b>Causes:</b><br/>
The program has no permission to write it's own file.
<br/>This warning usually occurs when the script is located at "/usr/share/nautilus-python/extensions/".
<br/><br/><b>Possible Effects:</b><br/>
The self-update function will not be available.
<br/>The script may show the releases page on multiple startups if self-update isn't disabled.
<br/><br/><b>How to solve?</b><br/>
To remove the release popup, you may disable the corresponding setting. To do this, please follow the instructions on the [configuration page](https://github.com/Lich-Corals/linux-file-converter-addon/blob/main/markdown/configuration.md).
<br/>To get self updates, the script needs the permissions to write to itself. This can be done by changing the file permissions using [chmod](https://www.man7.org/linux/man-pages/man1/chmod.1.html) or by running the script as a privileged user.
<br/>To be able to self-update, the user, who is executing the script (by starting Nautilus) needs permissions to edit the script itself.

### (403): No permission to write configuration file
<b>Causes:</b><br/>
The program has no permission to write in the `~/.config/` dictionary, or it doesn't exist.
<br/><br/><b>Possible Effects:</b><br/>
The self-update function may not be available.
<br/>The script needs to be configured by editing the script itself.
<br/>If self-updating is enabled, the script's configuration will reset when an update is performed.
<br/><br/><b>How to solve?</b><br/>
To fix this, the script needs the permissions to write inside the folder, where it is located. This can be done by changing the folder permissions using [chmod](https://www.man7.org/linux/man-pages/man1/chmod.1.html) or the change-permission dialogue of your file manager.
<br/>To use the configuration file, the user, who is executing the script (by starting Nautilus) needs permissions create and edit files inside the `~/.config/` dictionary.
<br/><br/>To prevent the settings from being reset, you can add the `~/.config/linux-file-converter-addon/config.json` file manually and make sure you have permissions to write to it.

#### All sections
- [Main page](https://github.com/Lich-Corals/linux-file-converter-addon/blob/main/README.md)
- [Configuration](https://github.com/Lich-Corals/linux-file-converter-addon/blob/main/markdown/configuration.md)
- __[Errorrs and warnings](https://github.com/Lich-Corals/linux-file-converter-addon/blob/main/markdown/errors-and-warnings.md)__
- [Install dependencies](https://github.com/Lich-Corals/linux-file-converter-addon/blob/main/markdown/install-dependencies.md)
- [Installation for Nautilus](https://github.com/Lich-Corals/linux-file-converter-addon/blob/main/markdown/install-nautilus.md)
- [Installation for Nemo](https://github.com/Lich-Corals/linux-file-converter-addon/blob/main/markdown/install-nemo.md)
- [Installation for Thunar](https://github.com/Lich-Corals/linux-file-converter-addon/blob/main/markdown/install-thunar.md)
