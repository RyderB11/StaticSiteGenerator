from textnode import TextNode
from markdown_to_html import markdown_to_html_node
import htmlnode
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
    for line in markdown.splitlines():
        if line.startswith("# "):
            return line.lstrip("# ").strip()
        raise Exception("No h1 header found in the markdown content!")
    

def generate_page(from_path, template_path, dest_path):
    print(f'Generating page from {from_path} to {dest_path} using {template_path}')

    # Print diagnostics
    print("Current working directory:", os.getcwd())
    print("Absolute path to from_path:", os.path.abspath(from_path))
    print("Absolute path to template_path:", os.path.abspath(template_path))

    with open(from_path, 'r') as md_file:
        markdown_content = md_file.read()

    with open(template_path, 'r') as template_file:
        template_content = template_file.read()

    html_content = markdown_to_html_node(markdown_content).to_html()

    # Print HTML content for debugging
    print("Generated HTML content:")
    print(html_content)

    title = extract_title(markdown_content)

    output_html = template_content.replace('{{ Title }}', title)
    output_html = output_html.replace('{{ Content }}', html_content)


    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, 'w') as output_file:
        output_file.write(output_html)
    

    # Read the content of the markdown file
    # with open(from_path, 'r') as md_file:
    #    markdown_content = md_file.read()




def main():
    # Dummy values for testing TextNode
   # text = "This is a text node"
   # text_type = "bold"
   # url = "https://boot.dev"
   # node = TextNode(text, text_type, url)
   # print(node)  # Print the node to verify it's working


    # Directories for copying
    src_directory = "../Static Site Generator/static"  # Source directory
    dst_directory = "../Static Site Generator/public"  # Destination directory

    # Clear the destination directory before copying
    if os.path.exists(dst_directory):
        shutil.rmtree(dst_directory)  # Remove all contents from the destination
    
    # Copy contents from source to destination
    copy_directory(src_directory, dst_directory)

    from_path = "../Static Site Generator/content/index.md"
    template_path = "../Static Site Generator/template.html"
    dest_path = "../Static Site Generator/public/index.html"

    # Print diagnostics before calling generate_page
    print("Current working directory:", os.getcwd())
    print("Absolute path to from_path:", os.path.abspath(from_path))
    print("Absolute path to template_path:", os.path.abspath(template_path))
    print("Absolute path to dest_path:", os.path.abspath(dest_path))

    generate_page(from_path, template_path, dest_path)
    

# Ensure the script runs only when executed directly
if __name__ == "__main__":
    main()
