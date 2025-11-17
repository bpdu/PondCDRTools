import os
import re
import shutil
from datetime import datetime

def validate_folder(path, should_create=False, check_write_access=False):
    """Validate folder existence and permissions"""
    if not os.path.exists(path):
        if should_create:
            try:
                os.makedirs(path, exist_ok=True)
                print(f"Creating a folder {path}..")
                return True
            except Exception as e:
                print(f"Error: Failed to create folder {path} - {str(e)}")
                return False
        else:
            return False
    else:
        if check_write_access:
            test_file = os.path.join(path, "testfile.tmp")
            try:
                with open(test_file, 'w') as f:
                    f.write("test")
                os.remove(test_file)
                print(f"Checking a folder {path}..")
                print("Valid destination!")
                return True
            except Exception as e:
                print(f"Error: No write access to folder {path} - {str(e)}")
                return False
        return True

def parse_date_from_filename(filename):
    """Extract client and date information from filename"""
    pattern = r'LIVE_(.+?)_(?:CDR|LU)_(\d{4})(\d{2})(\d{2})\d+'
    match = re.match(pattern, filename)
    if match:
        return {
            'client': match.group(1),
            'year': int(match.group(2)),
            'month': int(match.group(3)),
            'day': int(match.group(4))
        }
    return None

def copy_files_with_progress(source, destination, period, create_client_folders):
    """Copy matching files with progress reporting"""
    matching_files = []
    
    # First pass: find matching files
    for filename in os.listdir(source):
        filepath = os.path.join(source, filename)
        if os.path.isfile(filepath):
            date_info = parse_date_from_filename(filename)
            if date_info and date_info['year'] == period['year'] and date_info['month'] == period['month']:
                matching_files.append((filepath, filename, date_info['client'] if create_client_folders else None))
    
    print(f"Looking for CDR/LU files for the period of {period['year']}-{period['month']:02d}: {len(matching_files)} files found!")
    
    if not matching_files:
        return 0
    
    # Second pass: copy files
    print("Start copying files..")
    copied_count = 0
    for i, (filepath, filename, client) in enumerate(matching_files, 1):
        dest_path = destination
        if client:
            client_folder = os.path.join(destination, client)
            os.makedirs(client_folder, exist_ok=True)
            dest_path = client_folder
        
        try:
            shutil.copy2(filepath, os.path.join(dest_path, filename))
            copied_count += 1
            progress = int((i / len(matching_files)) * 100)
            print(f"Copy progress: {progress}% ({i}/{len(matching_files)})\n", end='\r')
        except Exception as e:
            print(f"\nError copying file {filename}: {str(e)}")
    
    print()  # New line after progress
    return copied_count

def main():
    print("======================")
    print("CDR/LU files copy utility")
    print("-----------------------------------------")
    print("Enter your source and destination folders")
    print("along with the period of time to match.")
    print("-----------------------------------------")
    print("\nINPUT:")

    
    # 1a. Source folder
    default_source = r"\\AMTELDC\CDRs\telna"
    source_folder = input(f"Enter source folder path (default: {default_source}): ").strip() or default_source
    if not os.path.isdir(source_folder):
        print(f"Error: Invalid source folder: {source_folder}")
        print("Bye")
        return
    else:
        print(f"Valid source!")

    
    # 1b. Destination folder
    default_dest = r"\\AMTELDC\CDRs\cdr_copy"
    dest_folder = input(f"\nEnter destination folder path (default: {default_dest}): ").strip() or default_dest
    if source_folder == dest_folder:
        print(f"Error: Cannot copy files to the same folder!")
        print("Bye")
        return
    if not validate_folder(dest_folder, check_write_access=True):
        create_dest = input("Warning: Destination folder doesn't exist or isn't writable. Create it? (Y/n): ").strip().lower()
        if create_dest not in ('n', 'no'):
            if not validate_folder(dest_folder, should_create=True, check_write_access=True):
                print(f"Error: Invalid destination folder: {dest_folder}")
                print("Bye")
                return
        else:
            print(f"Error: Invalid destination folder: {dest_folder}")
            print("Bye")
            return
    
    # 1c. Create client subfolders
    create_client_folders_input = input("\nCreate client subfolders? (Y/n): ").strip().lower()
    create_client_folders = create_client_folders_input not in ('n', 'no')
    
    # 1d. Year
    current_year = datetime.now().year
    year_input = input(f"\nEnter year to match (YYYY, default: {current_year}): ").strip()
    try:
        year = int(year_input) if year_input else current_year
    except ValueError:
        print("Error: Invalid year format")
        return
    
    # 1e. Month
    current_month = datetime.now().month
    month_input = input(f"Enter month to match (MM, default: {current_month:02d}): ").strip()
    try:
        month = int(month_input) if month_input else current_month
    except ValueError:
        print("Error: Invalid month format")
        return
    
    # 2. Display request summary
    print("-----------------------------------------\n")
    print("YOUR REQUEST:")
    print(f"Source folder: {source_folder}")
    print(f"Destination folder: {dest_folder}")
    print(f"Period: {month:02d}-{year}")
    print(f"Create client folders: {create_client_folders}")
    print("-----------------------------------------\n")
    
    # 3. Prepare filesystem
    print("RUNNING:")
    month_folder = os.path.join(dest_folder, "{}-{:02d}".format(year, month))
    if not validate_folder(month_folder, should_create=True):
        return
    
    # 4. Copy files
    period = {'year': year, 'month': month}
    copied_count = copy_files_with_progress(
        source_folder, 
        month_folder, 
        period, 
        create_client_folders
    )
    
    # 5. Display report
    print("-----------------------------------------\n")
    print("REPORT:")
    print(f"{copied_count} files have been copied with no errors\n")
    print(f"Check copied files in:")
    print(f"{dest_folder}\n")
    print("-----------------------------------------\n")
    
    # 6. Exit
    print("Bye\n")

if __name__ == "__main__":
    main()