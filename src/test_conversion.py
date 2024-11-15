import unittest

from process import text_node_to_html_node, TextNode, TextType, LeafNode, text_to_textnodes, markdown_to_blocks, block_to_block_type, markdown_to_html_node


class TestNodeConversion(unittest.TestCase):
  def test_conversion(self):
    text_node = TextNode("Sample plain text", TextType.NORMAL)
    html_node = text_node_to_html_node(text_node)
    self.assertEqual(html_node, LeafNode("Sample plain text"))

    text = "Lempel–Ziv–Welch (LZW) is a universal lossless data compression algorithm created by Abraham Lempel, Jacob Ziv, and Terry Welch."
    url = "https://en.wikipedia.org/wiki/Lempel-Ziv-Welch"
    text_node = TextNode(text, TextType.LINK, url)
    html_node = text_node_to_html_node(text_node)
    self.assertEqual(html_node, LeafNode(tag="a", value=text, props={"href": url}))

  def test_all_conversion(self):
    text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
    extracted = text_to_textnodes(text)
    self.assertListEqual(
      extracted, [
        TextNode("This is ", TextType.NORMAL),
        TextNode("text", TextType.BOLD),
        TextNode(" with an ", TextType.NORMAL),
        TextNode("italic", TextType.ITALIC),
        TextNode(" word and a ", TextType.NORMAL),
        TextNode("code block", TextType.CODE),
        TextNode(" and an ", TextType.NORMAL),
        TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
        TextNode(" and a ", TextType.NORMAL),
        TextNode("link", TextType.LINK, "https://boot.dev"),
      ]
    )

  def test_markdown_to_blocks(self):
    text = """# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another list item
    """
    blocks = markdown_to_blocks(text)
    self.assertListEqual(
      blocks, [
        "# This is a heading",
        "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
        "* This is the first list item in a list block\n* This is a list item\n* This is another list item",
      ]
    )

    block_types = [block_to_block_type(block) for block in blocks]
    self.assertListEqual(block_types, ["heading", "paragraph", "unordered_list"])

  def test_paragraph(self):
    md = """
This is **bolded** paragraph
text in a p
tag here

"""

    node = markdown_to_html_node(md)
    html = node.to_html()
    self.assertEqual(
      html,
      "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p></div>",
    )

  def test_paragraphs(self):
    md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with *italic* text and `code` here

"""

    node = markdown_to_html_node(md)
    html = node.to_html()
    self.assertEqual(
      html,
      "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
    )

  def test_lists(self):
    md = """
- This is a list
- with items
- and *more* items

1. This is an `ordered` list
2. with items
3. and more items

"""

    node = markdown_to_html_node(md)
    html = node.to_html()
    self.assertEqual(
      html,
      "<div><ul><li>This is a list</li><li>with items</li><li>and <i>more</i> items</li></ul><ol><li>This is an <code>ordered</code> list</li><li>with items</li><li>and more items</li></ol></div>",
    )

  def test_headings(self):
    md = """
# this is an h1

this is paragraph text

## this is an h2
"""

    node = markdown_to_html_node(md)
    html = node.to_html()
    self.assertEqual(
      html,
      "<div><h1>this is an h1</h1><p>this is paragraph text</p><h2>this is an h2</h2></div>",
    )

  def test_blockquote(self):
    md = """
> This is a
> blockquote block

this is paragraph text

"""

    node = markdown_to_html_node(md)
    html = node.to_html()
    self.assertEqual(
      html,
      "<div><blockquote>This is a blockquote block</blockquote><p>this is paragraph text</p></div>",
    )


if __name__ == "__main__":
  unittest.main()
