import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNodePropsToHTML(unittest.TestCase):
    def test_props_to_html(self):
        # Creating an instance of HTMLNode with some properties
        node = HTMLNode(tag="a", props={"href": "https://www.example.com", "target": "_blank"})
        
        # What you expect props_to_html to return
        expected_result = ' href="https://www.example.com" target="_blank"'
        
        # Use assertEqual to check if the result from props_to_html matches your expectation
        self.assertEqual(node.props_to_html(), expected_result)

    def test_props_to_html_empty(self):
        node = HTMLNode(tag='a')
        expected_result = ''
        self.assertEqual(node.props_to_html(), expected_result)

class testLeafNodeToHTML(unittest.TestCase):
    def test_to_html_with_props(self):
        node = LeafNode(value="Click here!", tag="a", props={"href": "https://www.example.com", "target": "_blank"})
        expected_result = '<a href="https://www.example.com" target="_blank">Click here!</a>'
        self.assertEqual(node.to_html(), expected_result)

    def test_to_html_without_props(self):
        node = LeafNode(value="Just text", tag="p")
        expected_result = "<p>Just text</p>"
        self.assertEqual(node.to_html(), expected_result)

    def test_to_html_without_tag(self):
        node = LeafNode(value="Just text", props={"href": "https://www.example.com", "target": "_blank"})
        expected_result = "Just text"
        self.assertEqual(node.to_html(), expected_result)

    def test_to_html_with_empty_value_raises_error(self):
        # Using `with` to contextually expect a ValueError exception
        with self.assertRaises(ValueError):
            # This is the action that should trigger the ValueError
            node = LeafNode(value="" , tag="p")
            node.to_html()

    def test_to_html_with_none_value_raises_error(self):
        # Using `with` to contextually expect a ValueError exception
        with self.assertRaises(ValueError):
            # This is the action that should trigger the ValueError
            node = LeafNode(value = None , tag="p")
            node.to_html()

    def test_to_html_special_characters(self):
        node = LeafNode(value='This is a "quote"', tag="p")
        expected_result = '<p>This is a "quote"</p>'
        self.assertEqual(node.to_html(), expected_result)

    def test_to_html_invalid_props_format(self):
        with self.assertRaises(AttributeError):
            node = LeafNode(value="Text", tag="p", props="invalid props format")
            node.to_html()


class testParentNodeToHTML(unittest.TestCase):
    def test_parentnode_working(self):
        node = ParentNode(
            "p",
            [
                LeafNode("Bold text","b" ),
                LeafNode("Normal text",None),
                LeafNode("italic text","i"),
                LeafNode("Normal text",None),
            ],
        )

        node.to_html()
        expected_result = '<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>'
        self.assertEqual(node.to_html(), expected_result)

    def test_tag_empty(self):
        with self.assertRaises(ValueError):
            node = ParentNode(
                None,
                [
                    LeafNode("Bold text","b" ),
                    LeafNode("Normal text",None),
                    LeafNode("italic text","i"),
                    LeafNode("Normal text",None),
                ],
            )

            node.to_html()


    def test_no_children(self):
        with self.assertRaises(ValueError):
            node = ParentNode(
                None,
                [
                ],
            )

            node.to_html()

    def test_deep_nesting(self):
        # Leaf nodes for content
        leaf1 = LeafNode("This is a paragraph inside the section.", "p")
        leaf2 = LeafNode("This is a paragraph inside the article.", "p")
        
        # nest parent nodes
        section = ParentNode("section", [leaf1])
        article = ParentNode("article", [leaf2])
        
        # top-level parent that contains both section and article
        div = ParentNode("div", [section, article])
        
        # Expected HTML output
        expected_html = '<div><section><p>This is a paragraph inside the section.</p></section><article><p>This is a paragraph inside the article.</p></article></div>'
        
        # Assert
        self.assertEqual(div.to_html(), expected_html)


if __name__ == "__main__":
    unittest.main()
