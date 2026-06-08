import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode

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


class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        # Test basic paragraph tag generation
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_link(self):
        # Test tag generation incorporating attributes
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')

    def test_leaf_to_html_raw_text(self):
        # Test when tag is None; it should output raw text strings
        node = LeafNode(None, "Just some plain text.")
        self.assertEqual(node.to_html(), "Just some plain text.")

    def test_leaf_value_error(self):
        # Test that omitting a value raises a ValueError as expected
        node = LeafNode("span", None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_repr(self):
        # Test that __repr__ outputs a clean string without children array
        node = LeafNode("b", "Bold text")
        self.assertEqual(repr(node), "LeafNode(b, Bold text, None)")
        

class TestParentNode(unittest.TestCase):
    # --- Boot.dev Provided Tests ---
    
    def test_to_html_with_children(self):
        # Verifies simple one-level parent/child structure
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        # Verifies deep multi-level recursion structure
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    # --- Extra Critical Edge Cases ---

    def test_to_html_many_children(self):
        # Verifies a parent can sequentially handle a massive cluster of children
        node = ParentNode(
            "ul",
            [
                LeafNode("li", "Item 1"),
                LeafNode("li", "Item 2"),
                LeafNode("li", "Item 3"),
                LeafNode("li", "Item 4"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<ul><li>Item 1</li><li>Item 2</li><li>Item 3</li><li>Item 4</li></ul>"
        )

    def test_to_html_mixed_children(self):
        # Verifies a parent can handle standard text (no tag), leaves, and other parents together
        node = ParentNode(
            "p",
            [
                LeafNode(None, "Welcome to "),
                LeafNode("b", "Boot.dev"),
                LeafNode(None, "! Check this "),
                ParentNode("span", [LeafNode("a", "link", {"href": "#"})]),
            ]
        )
        self.assertEqual(
            node.to_html(),
            '<p>Welcome to <b>Boot.dev</b>! Check this <span><a href="#">link</a></span></p>'
        )

    def test_to_html_stacked_props(self):
        # Verifies that attributes render properly at every node layer independently
        node = ParentNode(
            "div",
            [
                ParentNode(
                    "form",
                    [LeafNode("input", "", {"type": "text", "placeholder": "Name"})],
                    {"method": "POST"}
                )
            ],
            {"class": "wrapper"}
        )
        self.assertEqual(
            node.to_html(),
            '<div class="wrapper"><form method="POST"><input type="text" placeholder="Name"></input></form></div>'
        )

    def test_empty_children_list_raises_error(self):
        # Verifies that passing an empty list triggers a ValueError
        node = ParentNode("div", [])
        with self.assertRaises(ValueError) as context:
            node.to_html()
        self.assertEqual(str(context.exception), "Invalid HTML: ParentNode must have children")

if __name__ == "__main__":
    unittest.main()
