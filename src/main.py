from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode


def text_node_to_html_node(text_node: TextNode):
  match text.text_type

def main():
  text_node = TextNode("This is a text node", TextType.BOLD, "https://www.boot.dev")
  print(text_node)
  html_node = HTMLNode(tag="p", value="this is some sample paragraph text")
  print(html_node)
  leaf_node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
  print(leaf_node)
  parent_node = ParentNode(
    "p",
    [
      ParentNode("p", [LeafNode(tag="i", value="nested")]),
      LeafNode(tag="b", value="Bold text"),
      LeafNode(tag=None, value="Normal text"),
      LeafNode(tag="i", value="italic text"),
      LeafNode(tag=None, value="Normal text"),
    ],
  )
  print(parent_node.to_html())


if __name__ == "__main__":
  main()
