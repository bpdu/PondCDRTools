import os

RED = "\033[91m"
RESET = "\033[0m"

def load_cdr_ids(path):
    with open(path, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]

def search_in_file(filepath, cdr):
    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        for i, line in enumerate(f, start=1):
            if cdr in line:
                return i, line.strip()
    return None, None

def index_all_files(folder):
    files = {}
    for root, _, fs in os.walk(folder):
        for name in fs:
            files[name] = os.path.join(root, name)
    return files

def main():
    default_folder = r"\\AMTELDC\CDRs\cdr"
    folder = input(f"Enter path to CDR folder [{default_folder}]: ").strip() or default_folder
    if not os.path.isdir(folder):
        print("Folder not found! Bye..")
        return
    print("Folder found! Continue..")

    default_cdr_file = os.path.join(os.getcwd(), "cdr_ids.txt")
    cdr_file = input(f"Enter path to file with CDR IDs [{default_cdr_file}]: ").strip() or default_cdr_file
    if not os.path.isfile(cdr_file):
        print("CDR ID file not found! Bye..")
        return
    print("CDR ID file found! Continue..\n")

    cdr_ids = load_cdr_ids(cdr_file)
    files = index_all_files(folder)

    for cdr in cdr_ids:
        found = False
        for filename, fullpath in files.items():
            line_number, line_content = search_in_file(fullpath, cdr)
            if line_number:
                print(f"{cdr} - {RED}Found{RESET} ({filename} - Line {line_number})")
                print()
                print(line_content)
                print()
                found = True
                break
        if not found:
            print(f"{cdr} - {RED}Not found{RESET}")

if __name__ == "__main__":
    main()
