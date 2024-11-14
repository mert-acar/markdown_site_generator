import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):

  def test_enum(self):
    with self.assertRaises(AttributeError):
      TextNode("sample text", TextType.NOTANORMALTYPE)

  def test_not_eq(self):
    node1 = TextNode("This is a text node", TextType.BOLD)
    node2 = TextNode("This is another text node", TextType.BOLD)
    self.assertNotEqual(node1, node2)

    node1 = TextNode("This is a text node", TextType.BOLD)
    node2 = TextNode("This is a text node", TextType.BOLD, "https://www.google.com")
    self.assertNotEqual(node1, node2)

    node1 = TextNode("This is a text node", TextType.BOLD)
    node2 = TextNode("This is a text node", TextType.ITALIC)
    self.assertNotEqual(node1, node2)

  def test_eq(self):
    node1 = TextNode("This is a text node", TextType.BOLD)
    node2 = TextNode("This is a text node", TextType.BOLD)
    self.assertEqual(node1, node2)

  def test_repr(self):
    node = TextNode("Sample text", TextType.NORMAL, "https://www.google.com")
    node_string = node.__repr__()
    self.assertEqual(node_string, "TextNode(Sample text, normal, https://www.google.com)")

if __name__ == "__main__":
  unittest.main()
