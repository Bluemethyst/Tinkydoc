import os
import requests
import zipfile
import shutil
import json
from tqdm import tqdm

def download_zip_file(url, zip_file_path):
    """Download the zip file from the given URL."""
    print(f"Downloading zip file from {url}")
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    block_size = 1024

    with tqdm(total=total_size, unit="B", unit_scale=True, desc="Downloading") as progress_bar:
        with open(zip_file_path, "wb") as file:
            for data in response.iter_content(block_size):
                progress_bar.update(len(data))
                file.write(data)
    if total_size != 0 and progress_bar.n != total_size:
        raise RuntimeError("Could not download file")

def extract_zip_file(zip_file_path, extract_dir):
    """Extract the zip file to the specified directory."""
    print(f"Extracting zip file to {extract_dir}")
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        for member in tqdm(zip_ref.infolist(), desc='Extracting'):
            zip_ref.extract(member, extract_dir)

def get_top_level_dir(extract_dir):
    """Get the top-level directory inside the extracted directory."""
    return os.path.join(extract_dir, os.listdir(extract_dir)[0])

def delete_unwanted_files(top_level_dir, keep_path, kept_files):
    """Delete all files and folders except for the specified keep path."""
    print(f"Deleting files except for {keep_path}")
    for root, dirs, files in os.walk(top_level_dir, topdown=False):
        for name in files:
            file_path = os.path.abspath(os.path.join(root, name))
            if not file_path.startswith(keep_path):
                os.remove(file_path)
            else:
                # Get the relative path from 'book' directory
                relative_path = os.path.relpath(file_path, keep_path)
                kept_files.append(os.path.join("book", relative_path))

def remove_empty_folders(top_level_dir):
    """Remove all empty folders in the top-level directory."""
    print("Removing empty folders")
    for root, dirs, files in os.walk(top_level_dir, topdown=False):
        for dir_name in dirs:
            dir_path = os.path.join(root, dir_name)
            if not os.listdir(dir_path):
                shutil.rmtree(dir_path)

def write_kept_files_to_json(kept_files, output_path):
    """Write the list of kept files to a JSON file."""
    print(f"Writing kept files to {output_path}")
    data = {"files": kept_files}
    with open(output_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)

def clean_up(zip_file_path):
    """Remove the zip file to clean up."""
    print("Cleaning up")
    os.remove(zip_file_path)
    shutil.rmtree("tmp")

def move_to_public(folder, json_file):
    """Move the extracted files to the public directory."""
    print("Moving to public directory")
    shutil.rmtree(r"public\book", ignore_errors=True)
    shutil.move(folder, "public")
    shutil.move(json_file, "public")

# Main flow
url = "https://api.github.com/repos/SlimeKnights/TinkersConstruct/zipball"
zip_file_path = "repo.zip"
extract_dir = "tmp"
kept_files = []  # To store the paths of kept files

# Step 1: Download the zip file
download_zip_file(url, zip_file_path)

# Step 2: Extract the zip file
extract_zip_file(zip_file_path, extract_dir)

# Step 3: Get the top-level directory
top_level_dir = get_top_level_dir(extract_dir)
print(top_level_dir)

# Step 4: Define the path to keep
keep_path = os.path.abspath(os.path.join(top_level_dir, "src/main/resources/assets/tconstruct/book"))
print(f"Keep path: {keep_path}")

# Step 5: Delete unwanted files and collect kept files
delete_unwanted_files(top_level_dir, keep_path, kept_files)

# Step 6: Remove empty folders
remove_empty_folders(top_level_dir)

# Step 7: Write kept files to JSON
output_json_path = "kept_files.json"
write_kept_files_to_json(kept_files, output_json_path)

# Step 8: Move kept files to the public folder
move_to_public(keep_path, output_json_path)

# Step 9: Clean up the zip file
clean_up(zip_file_path)
