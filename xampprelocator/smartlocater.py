import os
import shutil
from datetime import datetime

currentTime = datetime.now().strftime("%y-%m-%d %H%M%S")

data_file = "smartlocater.data" # Nama file untuk menyimpan pathPrevious
# Cek apakah file smartlocater.data ada
if os.path.exists(data_file):
    # Jika ada, baca nilai pathPrevious dari file
    with open(data_file, "r") as file:
        pathPrevious = file.read().strip()
else:
    # Jika file tidak ada, set default pathPrevious dan buat file
    pathPrevious = "C:/xampp/"
    with open(data_file, "w") as file:
        file.write(pathPrevious)
pathCurrent = os.path.abspath("") + "/"

# Daftar files yang kemungkinan butuh di config ulang
filesToEdit = [
    "apache/conf/httpd.conf",
    "apache/conf/extra/httpd-vhosts.conf",
    "php/php.ini",
    "mysql/bin/my.ini",
    "apache/apache_start.bat",
    "apache/apache_stop.bat",  # Biasanya juga ada file untuk menghentikan Apache
    "apache/logs/error.log",   # Log error Apache
    "apache/logs/access.log",  # Log akses Apache
    "htdocs/index.php",        # File default pada direktori htdocs
    "htdocs/phpmyadmin/config.inc.php"  # File konfigurasi phpMyAdmin
]

def BackupFile(fileTarget):
    global currentTime

    fileName = os.path.basename(fileTarget)  # Dapatkan nama file target
    parentFolder = os.path.dirname(fileTarget).replace(os.path.abspath(""), "")  # Dapatkan parent folder file target
    backupFolder = "backup/" + currentTime  # Tambahkan path folder parent di backup
    os.makedirs(backupFolder + parentFolder, exist_ok=True)  # Buat folder backup dan folder parent yang diperlukan

    try:
        # Baca konten file target
        with open(fileTarget, "r") as targetedFile:
            filesContent = targetedFile.read()

        # Buat file backup dan simpan isinya
        with open(os.path.join(backupFolder, fileName), "w") as backupFile:
            backupFile.write(filesContent)

        print(f"Backup successfully created for file: {fileTarget}")

    except FileNotFoundError:
        print(f"Error: File '{fileTarget}' not found!")
    except Exception as e:
        print(f"An error occurred: {e}")

def EditFile(target):
    global pathPrevious, pathCurrent

    try:
        # Baca konten file target
        with open(target, "r") as file:
            content = file.read()

        # Cek apakah ada perubahan yang akan dilakukan
        if pathPrevious in content:
            # Jika ada perubahan, lakukan penggantian
            new_content = content.replace(pathPrevious, pathCurrent)

            # Tulis konten yang sudah diubah ke file
            with open(target, "w") as file:
                file.write(new_content)

            print(f"File {os.path.basename(target)} has been modified.")
        else:
            print(f"No changes made to {os.path.basename(target)}. The target string '{pathPrevious}' was not found.")

    except FileNotFoundError:
        print(f"Error: File '{target}' not found!")
    except PermissionError:
        print(f"Error: Permission denied while accessing '{target}'!")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# MAIN PROGRAM
print("All files to be edited will be automatically backed up to the 'backup' folder. If any unwanted changes occur, the original files can be restored from the backup.\n")

isContinue = input("Do you want to continue? [Y/N] ")
if isContinue.lower() != "y": exit()

print()

for target in filesToEdit:
    BackupFile(target)
    EditFile(target)
    print()

# CLOSING PROGRAM
with open(data_file, "w") as file:
    file.write(pathCurrent)

print()