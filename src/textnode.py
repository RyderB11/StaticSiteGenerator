from htmlnode import LeafNode

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