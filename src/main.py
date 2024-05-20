from textnode import TextNode
from markdown_to_html import markdown_to_html_node
from htmlnode import to_html
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

def extract_title(markdown):
    for line in markdown.split('\n'):
        if line.startswith("\#"):
            return line[2:]
        raise Exception("No h1 header found in the markdown content!")
    

def generate_page(from_path, template_path, dest_path):
    print(f'Generating page from {from_path} to {dest_path} using {template_path}')

    with open(from_path, 'r') as file:
        markdown_content = file.read()

    with open(template_path, 'r') as file:
        template_content = file.read()

    html_content = markdown_to_html_node(markdown_content).to_html()

    title = extract_title(markdown_content)

    new_content = template_content.replace('{{ Title }}', title).replace('{{ Content }}', html_content)

    os.makedirs(os.path.dirname(dest_path), exist_ok = True)
    with open(dest_path, 'W') as file:
        file.write(new_content)




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
