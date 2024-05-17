from htmlnode import LeafNode
import re

text_type_text = "text"
text_type_bold = "bold"
text_type_italic = "italic"
text_type_code = "code"
text_type_link = "link"
text_type_image = "image"

# this is the class for TextNode, nothing else to add here, we defaulty url to None so if nothing is passed in, None will return, if something is passed in, self.url will match the input
class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

# here we're trying to create an eq method that should be true if *all* of 2 TextNodes are equal. SO i tried with 2 and statements. will see what happens

    def __eq__(self, other):
        if isinstance(other,TextNode):
            return self.text == other.text and self.text_type == other.text_type and self.url == other.url
        return False
    
# lastly this is the repr for the function. i have my doubts as this returns the values, but not explicitly printing them, will trial and error this one and if we dont see anything printed, i know where to look.
    # i was wrong, this needs to be a return and not a print()
    def __repr__(self):
        return(f"TextNode({self.text}, {self.text_type}, {self.url})")
    
def text_node_to_html_node(text_node):
    if text_node.text_type == text_type_text:
        return LeafNode(None, text_node.text)
    if text_node.text_type == text_type_bold:
        return LeafNode("b", text_node.text)
    if text_node.text_type == text_type_italic:
        return LeafNode("i", text_node.text)
    if text_node.text_type == text_type_code:
        return LeafNode("code", text_node.text)
    if text_node.text_type == text_type_link:
        return LeafNode("a", text_node.text, {"href": text_node.url})
    if text_node.text_type == text_type_image:
        return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
    raise ValueError(f"Invalid text type: {text_node.text_type}")


# solution code that works
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != text_type_text:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        sections = old_node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("Invalid markdown, formatted section not closed")
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], text_type_text))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes
#here is some code that extracts the image, and the other links. now obviously they're repeating code differentiated by the regex. I was thinking this could just be a class and with chatgpt quick look, i could make the input of the findall different.
# But thats a different day. The code below works according to the tests in test_textnode. they're in the extraction class
def extract_markdown_images(text):
    tuple_list = []
    for alt_text, image_url in re.findall(r"!\[(.*?)\]\((.*?)\)", text):
        match_tuple = (alt_text, image_url)
        tuple_list.append(match_tuple)
    return tuple_list

def extract_markdown_links(text):
    tuple_list = []
    for alt_text, image_url in re.findall(r"\[(.*?)\]\((.*?)\)", text):
        match_tuple = (alt_text, image_url)
        tuple_list.append(match_tuple)
    return tuple_list


# here is the right code, some things to note, i havent learned anything about continue or anything. the rest, i honestly was never going to get by myself or with chatgpt or boots. we were talking in circles and i was over it.
def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != text_type_text:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        images = extract_markdown_images(original_text)
        if len(images) == 0:
            new_nodes.append(old_node)
            continue
        for image in images:
            sections = original_text.split(f"![{image[0]}]({image[1]})", 1)
            if len(sections) != 2:
                raise ValueError("Invalid markdown, image section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], text_type_text))
            new_nodes.append(
                TextNode(
                    image[0],
                    text_type_image,
                    image[1],
                )
            )
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, text_type_text))
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != text_type_text:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        links = extract_markdown_links(original_text)
        if len(links) == 0:
            new_nodes.append(old_node)
            continue
        for link in links:
            sections = original_text.split(f"[{link[0]}]({link[1]})", 1)
            if len(sections) != 2:
                raise ValueError("Invalid markdown, link section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], text_type_text))
            new_nodes.append(TextNode(link[0], text_type_link, link[1]))
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, text_type_text))
    return new_nodes



def text_to_textnodes(text):
    nodes = [TextNode(text, text_type_text)]
    nodes = split_nodes_delimiter(nodes, "**", text_type_bold)
    nodes = split_nodes_delimiter(nodes, "*", text_type_italic)
    nodes = split_nodes_delimiter(nodes, "`", text_type_code)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes

def markdown_to_blocks(markdown):
    blocks = markdown.split('\n\n')
    blocks = [block.strip() for block in blocks if block.strip()]
    return blocks
