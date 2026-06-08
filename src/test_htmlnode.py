import unittest
from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        # Test basic attribute formatting with the required leading space
        node = HTMLNode(
            tag="a", 
            value="Boot.dev", 
            props={"href": "https://www.boot.dev", "target": "_blank"}
        )
        self.assertEqual(
            node.props_to_html(), 
            ' href="https://www.boot.dev" target="_blank"'
        )

    def test_props_to_html_empty_and_none(self):
        # Test that an empty dict or None returns an empty string
        node_none = HTMLNode(tag="p", value="Hello")
        node_empty = HTMLNode(tag="p", value="Hello", props={})
        
        self.assertEqual(node_none.props_to_html(), "")
        self.assertEqual(node_empty.props_to_html(), "")

    def test_default_values(self):
        # Test that everything correctly defaults to None (or empty list for children)
        node = HTMLNode()
        self.assertIsNone(node.tag)
        self.assertIsNone(node.value)
        self.assertEqual(node.children, [])
        self.assertIsNone(node.props)

    def test_repr(self):
        # Test that __repr__ outputs a clean debugging string
        node = HTMLNode(tag="h1", value="Header Text")
        expected_repr = "HTMLNode(h1, Header Text, children: [], None)"
        self.assertEqual(repr(node), expected_repr)

if __name__ == "__main__":
    unittest.main()