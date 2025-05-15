import os
from datetime import datetime

TIME = datetime.now().strftime("%Y-%m-%d %H%M%S")
PATH = os.path.abspath("").replace("\\", "/")
PATH2 = os.path.abspath("").replace("/", "\\")
# PATH = "D:/Program Files/xampp" # FOR DEBUGGING

TARGETS = [
    "./apache/conf/httpd.conf",
    "./apache/conf/extra/httpd-ssl.conf",
    "./apache/conf/extra/httpd-xampp.conf",
    "./mysql/bin/my.ini",
]
TARGETS2 = [ # Yang direktorinya menggunakan \ untuk arah alih-alih /
    ".\\php\\php.ini",
]

def CreateBackup(target):
    targetPath = os.path.dirname(target)
    targetFile = os.path.basename(target)
    backupDir = f"backup/{TIME}/{targetPath}"

    if (not os.path.isfile(target)): 
        print(f"Gagal membuat backup, \"{target}\" bukan file") 
        return

    print(f"Membuat backup \"{target}\"")
    os.makedirs(backupDir, exist_ok=True)

    with open(target, "r") as f:
        content = f.read()
    with open(os.path.join(backupDir, targetFile), "w") as f:
        f.write(content)

def Relocate(target, _type):
    xampp = _type + "xampp" + _type                     # EX: "/xampp/" atau "\\xampp\\"

    if (not os.path.isfile(target)): 
        print(f"Gagal mengedit, \"{target}\" bukan file") 
        return
    
    contentAll = ""
    count = 0
    with open(target, "r") as f:
        for line in f:
            if xampp in line:                           # EX: 'Define SRVROOT "C:/xampp/apache"'
                splited = line.split(xampp)             # EX: ['Define SRVROOT "C:', 'apache"']
                first = splited[0]                      # EX: 'Define SRVROOT "C:' (Untuk memperingkas kode)
                for i in range(len(first)-1, -1, -1):   # Iterasi mundur EX: 18, 17, 16, 15...
                    char = first[i]                     # EX: ':' (Harusnya bakal cek dari karakter paling kanan, tapi dalam kasus ini kondisi langsung terpenuhi)
                    if char == ':':
                        count += 1
                        first = first[:i - 1]           # EX: 'Define SRVROOT "'

                        if _type == "/":
                            first += PATH               # EX: 'Define SRVROOT "D:/Program Files/xampp'
                        else:
                            first += PATH2

                        first += _type                  # EX: 'Define SRVROOT "D:/Program Files/xampp/'
                        lineEdited = first + splited[1] # EX: 'Define SRVROOT "D:/Program Files/xampp/' + 'apache"'
                        contentAll += lineEdited        # Tambahkan hasil ke content
                        break

                    if i == 0:                          # Jika simbol ':' tidak ditemukan
                        contentAll += line

            else:
                contentAll += line

    print(f"Mengubah {count} baris yang mengandung {xampp}")

    if count == 0: # Kalau gak ada yang berubah, gak usah tulis ulang
        print(f"File {target} tidak diubah, tidak ada baris yang cocok")
        return 

    try:
        with open(target, "w") as f:
            f.write(contentAll)
    except Exception as e:
        print(f"Gagal menulis file {target}: {e}")
    
def DeleteFile(target):
    try:
        os.remove(target)
        print("Menghapus file " + target)
    except Exception as e:
        print(f"Gagal menghapus file {target}: {e}")
        print(f"Coba untuk menghapus file secara manual")
    print()



if __name__ == "__main__":
    print("\nProgram ini lulus tahap uji coba pada Xampp v3.3.0")
    print("Jika Program dijalankan pada versi Xampp berbeda, mungkin program ini tidak akan berjalan sebagaimana mestinya")
    if input("Lanjutkan? [Y/N] ").lower() != "y": exit()

    print(f"\nMenjalankan program pada direktori \"{PATH}\"")

    print()
    for target in TARGETS:
        CreateBackup(target)
        Relocate(target, "/")
        print()

    for target in TARGETS2:
        CreateBackup(target)
        Relocate(target, "\\")
        print()

    # xcont = "xampp-control.ini"
    # CreateBackup(xcont)
    # DeleteFile(xcont)

input("Tekan Enter untuk keluar... ")
