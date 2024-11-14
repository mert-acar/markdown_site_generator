import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
  def test_props_to_html(self):
    node = HTMLNode(props={"href": "https://www.google.com", "target": "_blank"})
    self.assertEqual(node.props_to_html(), ' href="https://www.google.com" target="_blank"')

  def test_repr(self):
    node = HTMLNode(tag="p", value="this is some sample paragraph text")
    node_str = "HTMLNode(p, this is some sample paragraph text, children: None, None)"
    self.assertEqual(node.__repr__(), node_str)

  def test_leaf_html(self):
    node = LeafNode(tag="p", value="This is a paragraph of text.")
    node_html = "<p>This is a paragraph of text.</p>"
    self.assertEqual(node.to_html(), node_html)

    node = LeafNode(tag="a", value="Click me!", props={"href": "https://www.google.com"})
    node_html = '<a href="https://www.google.com">Click me!</a>'
    self.assertEqual(node.to_html(), node_html)

    node = LeafNode("Click me!")
    node_html = "Click me!"
    self.assertEqual(node.to_html(), node_html)

    with self.assertRaises(ValueError):
      node = LeafNode(None, tag="a").to_html()


  def test_parent_html(self):
    node = ParentNode(
      "p",
      [
        LeafNode(tag="b", value="Bold text"),
        LeafNode(tag=None, value="Normal text"),
        LeafNode(tag="i", value="italic text"),
        LeafNode(tag=None, value="Normal text"),
      ],
    )
    node_html = "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"
    self.assertEqual(node.to_html(), node_html)

    node = ParentNode(
      "p",
      [
        ParentNode("p", [LeafNode("some plain text", tag="p")]),
        LeafNode(tag="b", value="Bold text"),
        LeafNode(tag=None, value="Normal text"),
        LeafNode(tag="i", value="italic text"),
        LeafNode(tag=None, value="Normal text"),
      ],
    )
    node_html = "<p><p><p>some plain text</p></p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"
    self.assertEqual(node.to_html(), node_html)

    with self.assertRaises(ValueError):
      node = ParentNode("a", []).to_html()

if __name__ == "__main__":
  unittest.main()
