import unittest
from textnode import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes, markdown_to_blocks

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

    def test_split_image(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
            text_type_text,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", text_type_text),
                TextNode("image", text_type_image, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_split_image_single(self):
        node = TextNode(
            "![image](https://www.example.com/image.png)",
            text_type_text,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", text_type_image, "https://www.example.com/image.png"),
            ],
            new_nodes,
        )

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            text_type_text,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", text_type_text),
                TextNode("image", text_type_image, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", text_type_text),
                TextNode(
                    "second image", text_type_image, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://boot.dev) and [another link](https://blog.boot.dev) with text that follows",
            text_type_text,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", text_type_text),
                TextNode("link", text_type_link, "https://boot.dev"),
                TextNode(" and ", text_type_text),
                TextNode("another link", text_type_link, "https://blog.boot.dev"),
                TextNode(" with text that follows", text_type_text),
            ],
            new_nodes,
        )

class TestInlineMarkdown(unittest.TestCase):
    def test_delim_bold(self):
        node = TextNode("This is text with a **bolded** word", text_type_text)
        new_nodes = split_nodes_delimiter([node], "**", text_type_bold)
        self.assertListEqual(
            [
                TextNode("This is text with a ", text_type_text),
                TextNode("bolded", text_type_bold),
                TextNode(" word", text_type_text),
            ],
            new_nodes,
        )

    def test_delim_bold_double(self):
        node = TextNode(
            "This is text with a **bolded** word and **another**", text_type_text
        )
        new_nodes = split_nodes_delimiter([node], "**", text_type_bold)
        self.assertListEqual(
            [
                TextNode("This is text with a ", text_type_text),
                TextNode("bolded", text_type_bold),
                TextNode(" word and ", text_type_text),
                TextNode("another", text_type_bold),
            ],
            new_nodes,
        )

    def test_delim_bold_multiword(self):
        node = TextNode(
            "This is text with a **bolded word** and **another**", text_type_text
        )
        new_nodes = split_nodes_delimiter([node], "**", text_type_bold)
        self.assertListEqual(
            [
                TextNode("This is text with a ", text_type_text),
                TextNode("bolded word", text_type_bold),
                TextNode(" and ", text_type_text),
                TextNode("another", text_type_bold),
            ],
            new_nodes,
        )

    def test_delim_italic(self):
        node = TextNode("This is text with an *italic* word", text_type_text)
        new_nodes = split_nodes_delimiter([node], "*", text_type_italic)
        self.assertListEqual(
            [
                TextNode("This is text with an ", text_type_text),
                TextNode("italic", text_type_italic),
                TextNode(" word", text_type_text),
            ],
            new_nodes,
        )

    def test_delim_code(self):
        node = TextNode("This is text with a `code block` word", text_type_text)
        new_nodes = split_nodes_delimiter([node], "`", text_type_code)
        self.assertListEqual(
            [
                TextNode("This is text with a ", text_type_text),
                TextNode("code block", text_type_code),
                TextNode(" word", text_type_text),
            ],
            new_nodes,
        )

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://boot.dev) and [another link](https://blog.boot.dev)"
        )
        self.assertListEqual(
            [
                ("link", "https://boot.dev"),
                ("another link", "https://blog.boot.dev"),
            ],
            matches,
        )

    def test_split_image(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
            text_type_text,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", text_type_text),
                TextNode("image", text_type_image, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_split_image_single(self):
        node = TextNode(
            "![image](https://www.example.com/image.png)",
            text_type_text,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", text_type_image, "https://www.example.com/image.png"),
            ],
            new_nodes,
        )

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            text_type_text,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", text_type_text),
                TextNode("image", text_type_image, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", text_type_text),
                TextNode(
                    "second image", text_type_image, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://boot.dev) and [another link](https://blog.boot.dev) with text that follows",
            text_type_text,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", text_type_text),
                TextNode("link", text_type_link, "https://boot.dev"),
                TextNode(" and ", text_type_text),
                TextNode("another link", text_type_link, "https://blog.boot.dev"),
                TextNode(" with text that follows", text_type_text),
            ],
            new_nodes,
        )

    def test_text_to_textnodes(self):
        nodes = text_to_textnodes(
            "This is **text** with an *italic* word and a `code block` and an ![image](https://i.imgur.com/zjjcJKZ.png) and a [link](https://boot.dev)"
        )
        self.assertListEqual(
            [
                TextNode("This is ", text_type_text),
                TextNode("text", text_type_bold),
                TextNode(" with an ", text_type_text),
                TextNode("italic", text_type_italic),
                TextNode(" word and a ", text_type_text),
                TextNode("code block", text_type_code),
                TextNode(" and an ", text_type_text),
                TextNode("image", text_type_image, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and a ", text_type_text),
                TextNode("link", text_type_link, "https://boot.dev"),
            ],
            nodes,
        )

class test_markdown_to_blocks(unittest.TestCase):
    def test_normal(self):
        markdown = "Block1\n\nBlock2\n\nBlock3"
        expected = ['Block1', 'Block2', 'Block3']
        result = markdown_to_blocks(markdown)
        self.assertEqual(result, expected)

    def test_normal2(self):
        markdown = "Block1\n\nBlock2\n\n"
        expected = ['Block1', 'Block2']
        result = markdown_to_blocks(markdown)
        self.assertEqual(result, expected)

    def test_normal3(self):
        markdown = "Block 1\n\n\nBlock 2\n\n\nBlock 3\n\n\n"
        expected = ['Block 1', 'Block 2', 'Block 3']
        result = markdown_to_blocks(markdown)
        self.assertEqual(result, expected)

    def test_normal4(self):
        markdown = "Block 1\nBlock 2\n\nBlock 3"
        expected = ['Block 1\nBlock 2', 'Block 3']
        result = markdown_to_blocks(markdown)
        self.assertEqual(result, expected)

    def test_normal5(self):
        markdown = ""
        expected = []
        result = markdown_to_blocks(markdown)
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
