import unittest
from textnode import TextNode, TextType

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq_with_url(self):
        # Testing equality when all fields, including the URL, match perfectly
        node = TextNode("Click here", TextType.LINK, "https://www.boot.dev")
        node2 = TextNode("Click here", TextType.LINK, "https://www.boot.dev")
        self.assertEqual(node, node2)

    def test_not_eq_text_type(self):
        # Testing inequality when the text matches, but the TextType is different
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_not_eq_text(self):
        # Testing inequality when the TextType matches, but the text contents differ
        node = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("This is a different text node", TextType.TEXT)
        self.assertNotEqual(node, node2)

    def test_not_eq_url(self):
        # Testing inequality when one node has a URL and the other has None
        node = TextNode("Boot dev link", TextType.LINK, "https://www.boot.dev")
        node2 = TextNode("Boot dev link", TextType.LINK, None)
        self.assertNotEqual(node, node2)


if __name__ == "__main__":
    unittest.main()