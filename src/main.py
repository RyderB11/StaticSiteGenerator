from textnode import TextNode
import os
import shutil

def copy_directory(src, dst):
    # Ensure the destination directory exists
    if not os.path.exists(dst):
        os.mkdir(dst)  # Create the directory if it doesn't exist
    
    # List all items in the source directory
    for item in os.listdir(src):
        src_path = os.path.join(src, item)  # Full path to the source item
        dst_path = os.path.join(dst, item)  # Full path to the destination item

        if os.path.isfile(src_path):  # Check if the item is a file
            shutil.copy(src_path, dst_path)  # If so, copy the file to the destination
            print(f"Copied file: {src_path} to {dst_path}")
        elif os.path.isdir(src_path):  # Check if the item is a directory
            copy_directory(src_path, dst_path)  # If so, recurse into the directory
            print(f"Copied directory: {src_path} to {dst_path}")

def main():
    # Dummy values for testing TextNode
    text = "This is a text node"
    text_type = "bold"
    url = "https://boot.dev"
    node = TextNode(text, text_type, url)
    print(node)  # Print the node to verify it's working

    # Directories for copying
    src_directory = "static"  # Source directory
    dst_directory = "public"  # Destination directory

    # Clear the destination directory before copying
    if os.path.exists(dst_directory):
        shutil.rmtree(dst_directory)  # Remove all contents from the destination
    
    # Copy contents from source to destination
    copy_directory(src_directory, dst_directory)

# Ensure the script runs only when executed directly
if __name__ == "__main__":
    main()
