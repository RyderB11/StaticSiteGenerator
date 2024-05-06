import unittest
from htmlnode import HTMLNode, LeafNode

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


# This makes the test run if you execute the script directly.
if __name__ == "__main__":
    unittest.main()
