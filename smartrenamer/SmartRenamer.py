TargetToRename = ["[Kusonime] ", "_Kuso__", "Otakudesu.net_", "Otakudesu_", "[KurumiNime] "]

import sys
import os

def GetPermission(question):
    userInput:str = input(question)
    if userInput == "y" or userInput == "Y":
        return True
    else: 
        return False

def Rename(filename):
    splited = ""
    for char in filename:
        splited += char
        if splited in TargetToRename: #Apakah file akan di-rename
            nameRenamed = filename.split(splited)
            return nameRenamed[1]
    return None #Jika nama tidak perlu diubah

def RenameAllFolders():
    global renamed, renameFail
    for i in range(0, len(folders)):
        if foldersAfterRenamed[i] != None:
            try:
                os.rename(folders[i], foldersAfterRenamed[i])
                renamed += 1
            except Exception as e:
                renameFail += 1

def RenameAllFiles():
    global renamed, renameFail
    for i in range(0, len(files)):
        if filesAfterRenamed[i] != None:
            try:
                os.rename(files[i], filesAfterRenamed[i])
                renamed += 1
            except Exception as e:
                renameFail += 1

if __name__ == "__main__":
    
    args = sys.argv
    directory = os.getcwd()

    # Handle arguments
    print()
    if len(args) > 1:
        print(f'Trying to run program on "{args[1]}"')
        if os.path.exists(args[1]): directory = args[1]
        else: 
            print("Directory does not exist, closing program...")
            sys.exit()


    print(f'Running program on directory "{directory}"')
    isContinue = GetPermission('Continue ? [Y/N] ')

    print()

    if isContinue == False:
        print("Closing Program...")
        print()
        sys.exit()

    items = os.listdir(directory)
    files = []
    filesAfterRenamed = []
    folders = []
    foldersAfterRenamed = []

    for item in items:
        if os.path.isfile(item):
            files.append(item)
        else:
            folders.append(item)

    print(f'Including this script, this directory has {len(files)} files and {len(folders)} folders')

    # Rename the items
    for file in files:
        filesAfterRenamed.append(Rename(file))
    for folder in folders:
        foldersAfterRenamed.append(Rename(folder))

    # Count how much items will be renamed 
    renamedFiles = 0
    for i in range(0, len(files)):
        if filesAfterRenamed[i] != None:
            print(f'- "{files[i]}" > "{filesAfterRenamed[i]}"')
            renamedFiles += 1

    renamedFolders = 0
    for i in range(0, len(folders)):
        if foldersAfterRenamed[i] != None:
            print(f'- "{folders[i]}" > "{foldersAfterRenamed[i]}" (Folder)')
            renamedFolders += 1


    if renamedFolders or renamedFiles:
        print(f"Those {renamedFolders} folders and {renamedFiles} files will be renamed, are you sure?")
        print("1. Rename all items")
        print("2. Rename folders only")
        print("3. Rename files only")
        print("0. Do nothing")
        userInput = input("Be carefull, this action is permanent ")
    else:
        print("Nothing to rename, closing program...")
        print()
        sys.exit()

    renamed = 0
    renameFail = 0

    print()
    
    if userInput == "1":
        print("Permission Granted, renaming every items...")
        RenameAllFiles()
        RenameAllFolders()
    elif userInput == "2":
        print("Permission Granted, renaming every folders...")
        RenameAllFolders()
    elif userInput == "3":
        print("Permission Granted, renaming every files...")
        RenameAllFiles()
    else:
        print("Action Cancelled, Closing Program...")
        print()
        sys.exit()

    print()

    print(f"{renamed} items have been renamed...")
    if renameFail > 0: print(f"Failed to rename {renameFail} items...")
    print("Closing Program...")
    print()