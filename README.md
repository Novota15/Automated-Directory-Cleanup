# Seq Data Cleanup

A python script for removing files.

# Requirements

* Python3
* Install the required python libraries: ```pip3 install -r requirements.txt```

# Configuration

This program is configured by filling out *config.ini* with the desired values. It must comply with the following key-value format, where the keys, such as ```fol0```, ```files0``` may be named anything and the suffix values should not be contained in quotes. ```[Subfolders to Clean-Up]``` **DOES NOT** contain the top level directory you are cleaning out; that is specified in the command line argument when executing the program.

```
[Subfolders to Clean-Up]
fol0 = Test-Subdir0
fol1 = Test-Subdir1
fol2 = Test-Subdir2
[Files to Preserve Given Suffix]
files0 = .txt
files1 = .fastfcq
```

# Running the Script

To use this program execute ```$ python3 file-cleanup.py COMMAND DIR_PATH```, where ```DIR_PATH``` is the absolute path to the top level directory that will be cleaned up and ```COMMAND``` may be one of the following:
* **help**: Displays available commands, this is the default if no arguments are provided.
* **check_files**: Displays the files that will be preserved if the delete command is run. It is recommended to run this first and make sure that you are okay with the output.
* **delete_files**: Deletes all of the files inside the subfolders listed in *config.ini* except for files ending with the same suffixes listed in *config.ini*

# Write deleted files list stdout to a file

If you provide a path to a file as a third argument to the script when deleting files, the list of deleted files will be appended to that file.

# Examples

Checking if files will be preserved correctly:

```
$ python3 file-cleanup.py check_files /home/grant/Test/
filepath0 will be preserved
filepath1 will be preserved
...
```

Executing file cleanup:

```
$ python3 file-cleanup.py delete_files /home/grant/Test/ /home/grant/docs/deleted_list.txt
Are you ok with the files being preserved and ready to run clean-up? (y/n):y
Files have been deleted
```
