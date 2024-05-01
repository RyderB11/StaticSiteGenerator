import unittest
from htmlnode import HTMLNode

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

#    def test_props_to_html_with_integer_props(self):
        # Intentionally giving props an incorrect type (int)
 #       node_with_bad_props = HTMLNode(props=int)  # This would normally be a misuse of the props parameter
        
        # Depending on how you designed props_to_html to react to bad props,
        # the expected result here is subjective:
        # - It could be an empty string if your code catches and handles this gracefully.
        # - Or, if your implementation allows it to proceed without error, whatever that output might be.
        
        # Here, assuming your method is designed to return an empty string if props are not usable:
 #       expected_result = ''  
        
        # Testing the output of props_to_html()
 #       actual_result = node_with_bad_props.props_to_html()
        
 #       self.assertEqual(actual_result, expected_result)



# This makes the test run if you execute the script directly.
if __name__ == "__main__":
    unittest.main()
