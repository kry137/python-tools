import os

if not os.path.exists("[Kusonime] Test Subject"):
    os.mkdir("[Kusonime] Test Subject")
    print("Test folder created")

if os.path.exists("Test Subject"):
    os.rmdir("Test Subject")
    print("Test folder removed")

if not os.path.exists("[Kusonime] Test Subject.txt"):
    with open("[Kusonime] Test Subject.txt", 'w') as file:
        file.write("File ini telah dibuat dengan Python.\n")
    print(f"Test file created")

if os.path.exists("Test Subject.txt"):
    os.remove("Test Subject.txt")
    print(f"Test file removed")