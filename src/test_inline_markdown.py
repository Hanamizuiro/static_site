import unittest
from textnode import TextNode, TextType
from inline_markdown import extract_markdown_images, extract_markdown_links, split_nodes_delimiter, split_nodes_image, split_nodes_link, text_to_textnodes

class TestTextToTextNodes(unittest.TestCase):
    def test_text_to_textnodes_full(self):
        # Boot.dev provided sample test with a mix of everything
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            nodes,
        )

    def test_text_to_textnodes_plain(self):
        # Edge case: Ensure completely plain text passes through unmutated
        text = "This is just clean plain text without any formatting whatsoever."
        nodes = text_to_textnodes(text)
        self.assertListEqual([TextNode(text, TextType.TEXT)], nodes)

    def test_text_to_textnodes_only_formatting(self):
        # Edge case: Consecutive formatted items with no text buffers between them
        text = "**bold**_italic_`code`"
        nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("bold", TextType.BOLD),
                TextNode("italic", TextType.ITALIC),
                TextNode("code", TextType.CODE),
            ],
            nodes,
        )

class TestInlineMarkdownSplits(unittest.TestCase):
    def test_split_images(self):
        # Boot.dev provided test verifying sequential image isolation
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )

    def test_split_links(self):
        # Test basic sequential link isolation
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
            ],
            new_nodes,
        )

    def test_split_link_at_start(self):
        # Edge case: String starting directly with a markdown link asset
        node = TextNode("[Boot.dev](https://www.boot.dev) is an amazing platform.", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Boot.dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" is an amazing platform.", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_no_links_or_images(self):
        # Verification that standard unformatted nodes pass cleanly without mutations
        node = TextNode("Just a plain text node with no links or images.", TextType.TEXT)
        self.assertListEqual([node], split_nodes_link([node]))
        self.assertListEqual([node], split_nodes_image([node]))

class TestInlineMarkdown(unittest.TestCase):
    def test_delim_code(self):
        # Testing the code block backtick case from the prompt
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ]
        )

    def test_delim_bold(self):
        # Testing double asterisk parsing for bold sections
        node = TextNode("This is **bold** text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" text", TextType.TEXT),
            ]
        )

    def test_delim_italic(self):
        # Testing single underscore parsing for italic sections
        node = TextNode("This is _italic_ text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" text", TextType.TEXT),
            ]
        )

    def test_delim_multiple_same_type(self):
        # Testing handling multiple instances of the same delimiter in one node
        node = TextNode("Start **bold 1** middle **bold 2** end", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
            new_nodes,
            [
                TextNode("Start ", TextType.TEXT),
                TextNode("bold 1", TextType.BOLD),
                TextNode(" middle ", TextType.TEXT),
                TextNode("bold 2", TextType.BOLD),
                TextNode(" end", TextType.TEXT),
            ]
        )

    def test_delim_non_text_node_ignored(self):
        # Testing that pre-existing formatted nodes are skipped completely
        bold_node = TextNode("already bold", TextType.BOLD)
        text_node = TextNode("normal `code` text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([bold_node, text_node], "`", TextType.CODE)
        self.assertEqual(
            new_nodes,
            [
                TextNode("already bold", TextType.BOLD),
                TextNode("normal ", TextType.TEXT),
                TextNode("code", TextType.CODE),
                TextNode(" text", TextType.TEXT),
            ]
        )

    def test_missing_closing_delimiter_raises_error(self):
        # Testing that mismatched syntax breaks early with a clear exception
        node = TextNode("This is **unclosed bold text", TextType.TEXT)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "**", TextType.BOLD)


class TestMarkdownExtraction(unittest.TestCase):
    def test_extract_markdown_images(self):
        # Testing extraction of multiple images from a string
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        matches = extract_markdown_images(text)
        self.assertListEqual(
            [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")],
            matches
        )

    def test_extract_markdown_images_single(self):
        # Boot.dev provided sample test
        matches = extract_markdown_images("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)")
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        # Testing extraction of multiple links from a string
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        matches = extract_markdown_links(text)
        self.assertListEqual(
            [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")],
            matches
        )

    def test_extract_links_ignores_images(self):
        # Crucial edge case: Extracting links shouldn't accidentally parse an image
        text = "Here is a link [Boot.dev](https://www.boot.dev) and an image ![logo](https://www.boot.dev/logo.png)"
        matches = extract_markdown_links(text)
        self.assertListEqual([("Boot.dev", "https://www.boot.dev")], matches)

    def test_no_matches(self):
        # Verifies that both functions safely return empty lists when no syntax is found
        text = "This text has regular words, no fancy links or markdown elements."
        self.assertListEqual(extract_markdown_images(text), [])
        self.assertListEqual(extract_markdown_links(text), [])

if __name__ == "__main__":
    unittest.main()