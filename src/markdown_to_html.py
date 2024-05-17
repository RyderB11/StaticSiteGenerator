from htmlnode import HTMLNode

# Define constants for block types
BLOCK_TYPE_HEADING = "heading"
BLOCK_TYPE_CODE_BLOCK = "code_block"
BLOCK_TYPE_QUOTE = "quote"
BLOCK_TYPE_UNORDERED_LIST = "unordered_list"
BLOCK_TYPE_ORDERED_LIST = "ordered_list"
BLOCK_TYPE_PARAGRAPH = "paragraph"

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
    
    # Default to paragraph
    return BLOCK_TYPE_PARAGRAPH

def heading_to_html_node(block):
    level = block.count('#', 0, block.index(' '))
    content = block[level+1:].strip()
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

def paragraph_to_html_node(block):
    return HTMLNode("p", value=block.strip())

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
    else:
        return paragraph_to_html_node(block)

def markdown_to_html_node(markdown):
    blocks = markdown.split('\n\n')
    root = HTMLNode("div")
    
    for block in blocks:
        html_node = block_to_html_node(block)
        root.add_child(html_node)
    
    return root
