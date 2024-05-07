import unittest
from textnode import split_nodes_delimiter, extract_markdown_images, extract_markdown_links

from textnode import (
    TextNode,
    text_type_text,
    text_type_bold,
    text_type_italic,
    text_type_code,
    text_type_image,
    text_type_link,
)

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        self.assertEqual(node, node2)

    def test_uneq(self):
        node = TextNode("This is a text node","bold", "123")
        node2 = TextNode("This is a text node", "bold",)
        self.assertNotEqual(node,node2)

    def test_uneq2(self):
        node = TextNode("This is a text node","bold",)
        node2 = TextNode("This is not a text node","italics",)
        self.assertNotEqual(node,node2)

class Testsplitnodesdelimiter(unittest.TestCase):
    def test_split_single_node(self):
        nodes = [TextNode("This is **bold** text", "text")]
        delimiter = "**"
        text_type = "bold"
        expected = [
            TextNode("This is ", "text"),
            TextNode("bold", "bold"),
            TextNode(" text", "text")
        ]
        result = split_nodes_delimiter(nodes, delimiter, text_type)
        self.assertEqual(len(result), len(expected))
        for res_node, exp_node in zip(result, expected):
            self.assertEqual(res_node.text, exp_node.text)
            self.assertEqual(res_node.text_type, exp_node.text_type)

    def test_split_multiple_nodes(self):
        nodes = [
            TextNode("This is **bold** text", "text"),
            TextNode("Another **bold** example", "text")
        ]
        delimiter = "**"
        text_type = "bold"
        expected = [
            TextNode("This is ", "text"),
            TextNode("bold", "bold"),
            TextNode(" text", "text"),
            TextNode("Another ", "text"),
            TextNode("bold", "bold"),
            TextNode(" example", "text")
        ]
        result = split_nodes_delimiter(nodes, delimiter, text_type)
        self.assertEqual(len(result), len(expected))
        for res_node, exp_node in zip(result, expected):
            self.assertEqual(res_node.text, exp_node.text)
            self.assertEqual(res_node.text_type, exp_node.text_type)

    def test_no_delimiter_found(self):
        nodes = [TextNode("No delimiter here", "text")]
        delimiter = "**"
        text_type = "bold"
        expected = [TextNode("No delimiter here", "text")]
        result = split_nodes_delimiter(nodes, delimiter, text_type)
        self.assertEqual(result, expected)

    def test_empty_nodes_list(self):
        nodes = []
        delimiter = "**"
        text_type = "bold"
        expected = []
        result = split_nodes_delimiter(nodes, delimiter, text_type)
        self.assertEqual(result, expected)

class Extracttions(unittest.TestCase):
    def test_image_eq(self):
        text = "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and ![another](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png)"
        expected = [("image", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"), ("another", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png")]
        result = extract_markdown_images(text)
        self.assertEqual(result, expected)

    def test_links_eq(self):
        text = "This is text with a [link](https://www.example.com) and [another](https://www.example.com/another)"
        expected = [("link", "https://www.example.com"), ("another", "https://www.example.com/another")]
        result = extract_markdown_links(text)
        self.assertEqual(result, expected)

    def test_image_empty(self):
        text = ""
        expected = []
        result = extract_markdown_images(text)
        self.assertEqual(result, expected)

    def test_link_empty(self):
        text = ""
        expected = []
        result = extract_markdown_links(text)
        self.assertEqual(result, expected)

    def test_image_one_string(self):
        text = "This is text with an ![](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and ![](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png)"
        expected = [("", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"), ("", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png")]
        result = extract_markdown_images(text)
        self.assertEqual(result, expected)

    def test_link_one_string(self):
        text = "This is text with an [](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and [](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png)"
        expected = [("", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"), ("", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png")]
        result = extract_markdown_links(text)
        self.assertEqual(result, expected)        

    def test_link_imageregex(self):
        text = "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and ![another](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png)"
        expected = [("image", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"), ("another", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png")]
        result = extract_markdown_links(text)
        self.assertEqual(result, expected)
        
    def test_image_linkregex(self):
        text = "This is text with a [link](https://www.example.com) and ![an image](https://www.example.com/image.png)"
        expected = [("an image", "https://www.example.com/image.png")]
        result = extract_markdown_images(text)
        self.assertEqual(result, expected)



if __name__ == "__main__":
    unittest.main()
