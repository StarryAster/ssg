import unittest

from textnode import TextNode, TextType


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

if __name__ == "__main__":
    unittest.main()

