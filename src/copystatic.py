import os
import shutil

def copy_directory_recursive(source_dir, dest_dir):
    """
    Recursively copies contents from source_dir to dest_dir.
    Cleans out dest_dir first if it's the initial call.
    """
    # Ensure the source directory exists
    if not os.path.exists(source_dir):
        raise ValueError(f"Source directory '{source_dir}' does not exist.")

    # Iterate through all items in the current source directory
    for item in os.listdir(source_dir):
        source_path = os.path.join(source_dir, item)
        dest_path = os.path.join(dest_dir, item)
        
        if os.path.isfile(source_path):
            print(f"Copying file: {source_path} -> {dest_path}")
            shutil.copy(source_path, dest_path)
        else:
            print(f"Creating directory: {dest_path}")
            os.mkdir(dest_path)
            # Recursively copy contents of the sub-directory
            copy_directory_recursive(source_path, dest_path)

def generate_clean_static_copy(source="static", destination="public"):
    """
    Cleans out the destination directory and safely fires off
    the recursive copy handler.
    """
    print(f"Cleaning out target directory: {destination}/")
    if os.path.exists(destination):
        shutil.rmtree(destination)
        
    print(f"Creating pristine target directory: {destination}/")
    os.mkdir(destination)
    
    # Fire off the recursive worker
    copy_directory_recursive(source, destination)
    print("Static assets synced successfully!")