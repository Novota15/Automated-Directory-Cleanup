import os
import configparser
from sys import argv
from shutil import rmtree

def read_config():
    subdirs_to_clean = []
    files_to_preserve = []
    # read data from config file
    config = configparser.ConfigParser()
    config.read('config.ini')
    for sub_dir in config['Subfolders to Clean-Up']:
        subdirs_to_clean.append(str(config['Subfolders to Clean-Up'][sub_dir]))
    for suffix in config['Files to Preserve Given Suffix']:
        files_to_preserve.append(str(config['Files to Preserve Given Suffix'][suffix]))
    return subdirs_to_clean, files_to_preserve

def subdir_clean_recurse(root_dir, files_to_preserve, delete, output_file):
    # folders = []
    for root, dirlist, filelist in os.walk(root_dir):
        for file in filelist: # loop through files in subdir
            preserve = False
            for suffix in files_to_preserve:
                fullpath = os.path.join(root, file) # get the full path to the file
                # if "NextSeq" in fullpath:
                    # preserve = False
                    # break
                elif file.endswith(suffix): # file suffix matches a preservation suffix
                    if delete == False: # for checking run, will print files that are marked to be preserved
                        print("preserved:", fullpath)
                    preserve = True
                    break
            if delete == True and preserve == False: # remove the file
                fullpath = os.path.join(root, file)
                if output_file:
                    output_file.write(fullpath + "deleted" + "\n")
                print(fullpath, "deleted")
                os.remove(fullpath)
            # elif delete == False and preserve == False:
            #     fullpath = os.path.join(root, file)
            #     folder = fullpath.split("/")[:-1]
            #     folder = "/".join(folder)
                # if folder not in folders:
                #     folders.append(folder)
    # for folder in folders:
    #     print(folder, "will be cleaned")
    return

def file_recurse(root_dir, subdirs_to_clean, files_to_preserve, delete, output_file_name):
    # open file for writing
    if output_file_name:
        output_file = open(output_file_name,"a")
    else:
        output_file = None
    for root, dirlist, filelist in os.walk(root_dir): # traverse through the directory to be cleaned
        if os.path.basename(root) in subdirs_to_clean: # folder matches a subdir to be cleaned
            if delete == False:
                print(root, "will be cleaned")
            subdir_clean_recurse(root, files_to_preserve, delete, output_file)
        # else:
        #     if delete == False:
        #         if root == root_dir:
        #             for file in filelist:
        #                 fullpath = os.path.join(root, file)
        #                 print(fullpath, "will be preserved")
        #         else:
        #             preserve_msg = True
        #             for dir in subdirs_to_clean:
        #                 if dir in root.split("/"):
        #                     preserve_msg = False
        #                     break
        #             if preserve_msg == True:
        #                 print("Everything inside ", "/" + os.path.basename(root), "will be preserved")
    if output_file_name:
        output_file.close()
    return

def yes_or_no(question):
    while 1:
        reply = str(input(question + ' (y/n):')).lower().strip()
        if reply[0] == 'y':
            return True
        if reply[0] == 'n':
            return False

def delete_files(root_path, output_file_name):
    if root_path != None:
        subdirs_to_clean, files_to_preserve = read_config()
        # check if the user is ok with the files being preserved
        response = yes_or_no("Are you ok with the files being preserved and ready to run clean-up?")
        if response == True:
            file_recurse(root_path, subdirs_to_clean, files_to_preserve, True, output_file_name)
            print("Files have been deleted")
        else:
            print("Program closed, no files have been deleted")
            return
    else:
        print("Directory path missing")
    return

def check_files(root_path, output_file_name):
    if root_path != None:
        subdirs_to_clean, files_to_preserve = read_config()
        file_recurse(root_path, subdirs_to_clean, files_to_preserve, False, output_file_name)
    else:
        print("Directory path missing")
    return

def help():
    helptext = """
    File-Cleanup Commands:
    check_files DIR_PATH -> shows files that will be preserved with the given config
    delete_files DIR_PATH -> cleans folders specified in the config
    """
    print(helptext)
    return

commands = {
    "help": help,
    "delete_files": delete_files,
    "check_files": check_files
}

if len(argv) >= 2 and argv[1] in commands:
    read_config()
    if len(argv) > 2:
        try:
            # user gave file path for output file
            commands[argv[1]](argv[2], argv[3])
        except:
            # user did not provide output file path
            commands[argv[1]](argv[2], None)
    else:
        commands[argv[1]](None)
else:
    help()
