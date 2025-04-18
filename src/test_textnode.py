import unittest

from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_url_none(self):
        ex = TextNode("url text", TextType.LINK)
        ex2 = TextNode("url text", TextType.LINK, None)
        self.assertEqual(ex.url, None)
        self.assertEqual(ex2.url, None)

    def test_text_type(self):
        with self.assertRaises(AttributeError):
            TextNode("test text", TextType.OTHER)

    
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_img(self):
        node = TextNode(None, TextType.IMAGE, "https://qosmiques.xyz/fundo.png")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.value, None)
        self.assertEqual(html_node.props["src"], "https://qosmiques.xyz/fundo.png")

if __name__ == "__main__":
    unittest.main()

