import unittest
from process import (
  markdown_to_blocks, split_nodes_delimiter, TextNode, TextType, extract_markdown_links,
  extract_markdown_images, split_nodes_link, split_nodes_image, text_to_textnodes,
  block_to_block_type
)


class TestInlineMarkdown(unittest.TestCase):
  def test_delim_bold(self):
    node = TextNode("This is text with a **bolded** word", TextType.NORMAL)
    new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
    self.assertListEqual(
      [
        TextNode("This is text with a ", TextType.NORMAL),
        TextNode("bolded", TextType.BOLD),
        TextNode(" word", TextType.NORMAL),
      ],
      new_nodes,
    )

  def test_delim_bold_double(self):
    node = TextNode("This is text with a **bolded** word and **another**", TextType.NORMAL)
    new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
    self.assertListEqual(
      [
        TextNode("This is text with a ", TextType.NORMAL),
        TextNode("bolded", TextType.BOLD),
        TextNode(" word and ", TextType.NORMAL),
        TextNode("another", TextType.BOLD),
      ],
      new_nodes,
    )

  def test_delim_bold_multiword(self):
    node = TextNode("This is text with a **bolded word** and **another**", TextType.NORMAL)
    new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
    self.assertListEqual(
      [
        TextNode("This is text with a ", TextType.NORMAL),
        TextNode("bolded word", TextType.BOLD),
        TextNode(" and ", TextType.NORMAL),
        TextNode("another", TextType.BOLD),
      ],
      new_nodes,
    )

  def test_delim_italic(self):
    node = TextNode("This is text with an *italic* word", TextType.NORMAL)
    new_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)
    self.assertListEqual(
      [
        TextNode("This is text with an ", TextType.NORMAL),
        TextNode("italic", TextType.ITALIC),
        TextNode(" word", TextType.NORMAL),
      ],
      new_nodes,
    )

  def test_delim_bold_and_italic(self):
    node = TextNode("**bold** and *italic*", TextType.NORMAL)
    new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
    new_nodes = split_nodes_delimiter(new_nodes, "*", TextType.ITALIC)
    self.assertListEqual(
      [
        TextNode("bold", TextType.BOLD),
        TextNode(" and ", TextType.NORMAL),
        TextNode("italic", TextType.ITALIC),
      ],
      new_nodes,
    )

  def test_delim_code(self):
    node = TextNode("This is text with a `code block` word", TextType.NORMAL)
    new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
    self.assertListEqual(
      [
        TextNode("This is text with a ", TextType.NORMAL),
        TextNode("code block", TextType.CODE),
        TextNode(" word", TextType.NORMAL),
      ],
      new_nodes,
    )

  def test_extract_image_links(self):
    text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
    extracted = extract_markdown_images(text)
    self.assertListEqual(
      extracted, [("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
                  ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]
    )

  def test_extract_links(self):
    text = "This is text with a link [to google](https://www.google.com) and [to youtube](https://www.youtube.com)"
    extracted = extract_markdown_links(text)
    self.assertListEqual(
      extracted, [("to google", "https://www.google.com"),
                  ("to youtube", "https://www.youtube.com")]
    )

  def test_links(self):
    node = TextNode(
      "This is text with a link [to google](https://www.google.com), [to youtube](https://www.youtube.com) and [to twitter](https://www.x.com)",
      TextType.NORMAL
    )
    extracted = split_nodes_link([node])
    self.assertListEqual(
      extracted, [
        TextNode("This is text with a link ", TextType.NORMAL),
        TextNode("to google", TextType.LINK, "https://www.google.com"),
        TextNode(", ", TextType.NORMAL),
        TextNode("to youtube", TextType.LINK, "https://www.youtube.com"),
        TextNode(" and ", TextType.NORMAL),
        TextNode("to twitter", TextType.LINK, "https://www.x.com"),
      ]
    )

  def test_images(self):
    node = TextNode(
      "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)",
      TextType.NORMAL
    )
    extracted = split_nodes_image([node])
    self.assertListEqual(
      extracted, [
        TextNode("This is text with a ", TextType.NORMAL),
        TextNode("rick roll", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif"),
        TextNode(" and ", TextType.NORMAL),
        TextNode("obi wan", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
      ]
    )


if __name__ == "__main__":
  unittest.main()
