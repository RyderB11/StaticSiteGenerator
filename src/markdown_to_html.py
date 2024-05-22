from htmlnode import HTMLNode

# Define constants for block types
BLOCK_TYPE_HEADING = "heading"
BLOCK_TYPE_CODE_BLOCK = "code_block"
BLOCK_TYPE_QUOTE = "quote"
BLOCK_TYPE_UNORDERED_LIST = "unordered_list"
BLOCK_TYPE_ORDERED_LIST = "ordered_list"
BLOCK_TYPE_PARAGRAPH = "paragraph"
BLOCK_TYPE_IMAGE = "image"
BLOCK_TYPE_LINK = "link"
BLOCK_TYPE_BOLD = "bold"
BLOCK_TYPE_ITALICS = "italics"

# this is for inline bold and italics, this is needed for nested operations, without this, the headings for example would be in heading format, but not bold or italics
def process_bold_and_italic(text):
    while "**" in text:
        start = text.index("**")
        end = text.index("**", start + 2)
        bold_text = text[start + 2:end]
        text = text[:start] + f"<strong>{bold_text}</strong>" + text[end + 2:]
    
    while "*" in text:
        start = text.index("*")
        end = text.index("*", start + 1)
        italic_text = text[start + 1:end]
        text = text[:start] + f"<em>{italic_text}</em>" + text[end + 1:]
    
    return text

def block_to_block_type(block):
    # Check for heading
    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BLOCK_TYPE_HEADING
    
    # Check for code block
    if block.startswith("```") and block.endswith("```"):
        return BLOCK_TYPE_CODE_BLOCK
    
    # Check for quote block
    if all(line.startswith("> ") for line in block.splitlines()):
        return BLOCK_TYPE_QUOTE
    
    # Check for unordered list
    if all(line.startswith("* ") or line.startswith("- ") for line in block.splitlines()):
        return BLOCK_TYPE_UNORDERED_LIST
    
    # Check for ordered list
    lines = block.splitlines()
    if all(line.lstrip().startswith(f"{i+1}. ") for i, line in enumerate(lines)):
        return BLOCK_TYPE_ORDERED_LIST
    
    # Check for image
    if block.startswith("![") and "](" in block and block.endswith(")"):
        return BLOCK_TYPE_IMAGE
    
    # Check for link
    if block.startswith("[") and "](" in block and block.endswith(")"):
        return BLOCK_TYPE_LINK

    # Check for bold text
    if "**" in block:
        return BLOCK_TYPE_BOLD
    
    # check for italics
    if "*" in block and not "**" in block:
        return BLOCK_TYPE_ITALICS
    
    # Default to paragraph
    return BLOCK_TYPE_PARAGRAPH

def heading_to_html_node(block):
    level = block.count('#', 0, block.index(' '))
    content = block[level+1:].strip()
    content = process_bold_and_italic(content)
    return HTMLNode(f"h{level}", value=content)

def code_block_to_html_node(block):
    content = block.strip('`').strip()
    code_node = HTMLNode("code", value=content)
    return HTMLNode("pre", children=[code_node])

def quote_block_to_html_node(block):
    lines = block.splitlines()
    content = "\n".join(line[2:].strip() for line in lines)
    return HTMLNode("blockquote", value=content)

def unordered_list_to_html_node(block):
    lines = block.splitlines()
    ul_node = HTMLNode("ul")
    for line in lines:
        content = line[2:].strip()
        ul_node.add_child(HTMLNode("li", value=content))
    return ul_node

def ordered_list_to_html_node(block):
    lines = block.splitlines()
    ol_node = HTMLNode("ol")
    for line in lines:
        content = line[line.index(".") + 2:].strip()
        ol_node.add_child(HTMLNode("li", value=content))
    return ol_node

def image_to_html_node(block):
    alt_text_start = block.index("![") + 2
    alt_text_end = block.index("]", alt_text_start)
    alt_text = block[alt_text_start:alt_text_end]
    
    url_start = block.index("(", alt_text_end) + 1
    url_end = block.index(")", url_start)
    image_url = block[url_start:url_end]
    
    return HTMLNode("img", props={"src": image_url, "alt": alt_text})

def link_to_html_node(block):
    text_start = block.index("[") + 1
    text_end = block.index("]", text_start)
    text = block[text_start:text_end]

    url_start = block.index("(") + 1
    url_end = block.index(")", url_start)
    url = block[url_start:url_end]

    return HTMLNode("a", value=text, props={"href": url})

def convert_bold_text_node(block):
    # Convert bold text
    while "**" in block:
        start = block.index("**")
        end = block.index("**", start + 2)
        bold_text = block[start + 2:end]
        block = block[:start] + f"<strong>{bold_text}</strong>" + block[end + 2:]
    
    return HTMLNode("p", value=block)

def convert_italics_text_node(block):
    # Convert italic text
    while "*" in block:
        start = block.index("*")
        end = block.index("*", start + 1)
        italic_text = block[start + 1:end]
        block = block[:start] + f"<em>{italic_text}</em>" + block[end + 1:]
    
    return HTMLNode("p", value=block)

def paragraph_to_html_node(block):
    content = process_bold_and_italic(block.strip())
    return HTMLNode("p", value=content)

    
def block_to_html_node(block):
    block_type = block_to_block_type(block)

    if block_type == BLOCK_TYPE_HEADING:
        return heading_to_html_node(block)
    elif block_type == BLOCK_TYPE_CODE_BLOCK:
        return code_block_to_html_node(block)
    elif block_type == BLOCK_TYPE_QUOTE:
        return quote_block_to_html_node(block)
    elif block_type == BLOCK_TYPE_UNORDERED_LIST:
        return unordered_list_to_html_node(block)
    elif block_type == BLOCK_TYPE_ORDERED_LIST:
        return ordered_list_to_html_node(block)
    elif block_type == BLOCK_TYPE_IMAGE:
        return image_to_html_node(block)
    elif block_type == BLOCK_TYPE_LINK:
        return link_to_html_node(block)
    elif block_type == BLOCK_TYPE_BOLD:
        return convert_bold_text_node(block)
    elif block_type == BLOCK_TYPE_ITALICS:
        return convert_italics_text_node(block)
    else:
        return paragraph_to_html_node(block)


def markdown_to_html_node(markdown):
    blocks = markdown.split('\n\n')
    root = HTMLNode("div")
    
    for block in blocks:
        html_node = block_to_html_node(block)
        root.add_child(html_node)
    
    return root
