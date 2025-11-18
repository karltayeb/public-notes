# /// script
# dependencies = [
#   "pyyaml",
# ]
# ///
#
import os
import yaml
import shutil


def extract_front_matter(file_path):
    """
    Extracts the front matter from a Markdown file.

    Parameters:
    - file_path: str, path to the Markdown file.

    Returns:
    - dict: Parsed front matter as a dictionary, or an empty dictionary if no front matter is found or if the file is not a Markdown file.
    """
    # Check if the file is a Markdown file
    if not file_path.endswith(".md"):
        print(f"Skipping non-Markdown file: {file_path}")
        return dict()

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

            # Check if the file starts with front matter
            if content.startswith("---"):
                # Find the end of the front matter
                frontmatter_end = content.find("---", 3)
                if frontmatter_end != -1:
                    # Extract and parse the front matter
                    frontmatter = content[3:frontmatter_end]
                    return yaml.safe_load(frontmatter)
    except Exception as e:
        print(f"Error reading {file_path}: {e}")

    return dict()


def find_shared_files(vault_path):
    shared_files = []

    # Walk through all files in the vault

    for root, dirs, files in os.walk(os.path.expanduser(vault_path)):
        for file in files:
            file_path = os.path.join(root, file)  # Get the full path
            front_matter = extract_front_matter(file_path)
            if front_matter.get("share", False):
                shared_files.append(file_path)
    return shared_files


def copy_if_newer(source_file, destination_folder):
    """
    Copies the source file to the destination folder if the source file is newer
    or if it does not exist in the destination folder.

    Parameters:
    - source_file: str, path to the source file.
    - destination_folder: str, path to the destination folder.
    """
    # Ensure the destination folder exists
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    # Construct the destination file path
    destination_file = os.path.join(destination_folder, os.path.basename(source_file))

    # Check if the file exists in the destination folder
    if not os.path.exists(destination_file):
        # If it doesn't exist, copy the file
        shutil.copy2(source_file, destination_file)
        print(f"Copied: {source_file} to {destination_file}")
    else:
        # If it exists, check the modification times
        source_mtime = os.path.getmtime(source_file)
        destination_mtime = os.path.getmtime(destination_file)

        # Copy if the source file is newer
        if source_mtime > destination_mtime:
            shutil.copy2(source_file, destination_file)
            print(f"Updated: {source_file} to {destination_file}")


# Specify the path to your Obsidian vault
vault_path = "~/Documents/notes/"
shared_files = find_shared_files(vault_path)

# Find and print shared files
destination_folder = "content/"
for shared in shared_files:
    copy_if_newer(shared, destination_folder)
