import re

from typing import Sequence
from functools import partial
from textnode import TextNode, TextType
from htmlnode import LeafNode, ParentNode, HTMLNode

TEXT_DELIMITERS = [
  ("**", TextType.BOLD),
  ("*", TextType.ITALIC),
  ("`", TextType.CODE),
]


def text_node_to_html_node(text_node: TextNode) -> LeafNode:
  match text_node.text_type:
    case TextType.NORMAL:
      return LeafNode(text_node.text)
    case TextType.BOLD:
      return LeafNode(tag="b", value=text_node.text)
    case TextType.ITALIC:
      return LeafNode(tag="i", value=text_node.text)
    case TextType.CODE:
      return LeafNode(tag="code", value=text_node.text)
    case TextType.LINK:
      return LeafNode(tag="a", value=text_node.text, props={"href": text_node.url})
    case TextType.IMAGE:
      return LeafNode(tag="img", value="", props={"src": text_node.url, "alt": text_node.text})
    case _:
      raise Exception(f"text_type {text_node.text_type} is outside of TextType enum")


def extract_markdown_images(text):
  return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def extract_markdown_links(text):
  return re.findall(r"\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str,
                          text_type: TextType) -> list[TextNode]:
  out_list = []
  for node in old_nodes:
    if node.text_type == TextType.NORMAL:
      split_text = node.text.split(delimiter)
      if len(split_text) % 2 != 1:
        raise Exception(f"Invalid markdown format, unmatched delimiter {delimiter}")
      for i in range(len(split_text)):
        if split_text[i] == "":
          continue
        if i % 2 == 0:
          out_list.append(TextNode(split_text[i], TextType.NORMAL))
        else:
          out_list.append(TextNode(split_text[i], text_type))
    else:
      out_list.append(node)
  return out_list


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
  out_list = []
  for node in old_nodes:
    if node.text_type == TextType.NORMAL:
      image_links = extract_markdown_images(node.text)
      text = node.text
      for image_alt, image_link in image_links:
        pat = f"![{image_alt}]({image_link})"
        sections = text.split(pat, 1)
        if sections[0] == "":
          continue
        out_list.append(TextNode(sections[0], TextType.NORMAL))
        out_list.append(TextNode(image_alt, TextType.IMAGE, image_link))
        text = sections[-1]
      if len(text) > 0:
        out_list.append(TextNode(text, TextType.NORMAL))
    else:
      out_list.append(node)
  return out_list


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
  out_list = []
  for node in old_nodes:
    if node.text_type == TextType.NORMAL:
      image_links = extract_markdown_links(node.text)
      text = node.text
      for image_alt, image_link in image_links:
        pat = f"[{image_alt}]({image_link})"
        sections = text.split(pat, 1)
        if sections[0] == "":
          continue
        out_list.append(TextNode(sections[0], TextType.NORMAL))
        out_list.append(TextNode(image_alt, TextType.LINK, image_link))
        text = sections[-1]
      if len(text) > 0:
        out_list.append(TextNode(text, TextType.NORMAL))
    else:
      out_list.append(node)
  return out_list


def text_to_textnodes(text: str) -> list[TextNode]:
  nodes = [TextNode(text, TextType.NORMAL)]
  functions = [
    partial(split_nodes_delimiter, delimiter=delim, text_type=tt) for (delim, tt) in TEXT_DELIMITERS
  ]
  functions.extend([split_nodes_image, split_nodes_link])
  for f in functions:
    nodes = f(nodes)
  return nodes


def markdown_to_blocks(markdown: str) -> list[str]:
  return list(filter(lambda x: len(x) > 0, map(str.strip, markdown.split("\n\n"))))


def block_to_block_type(block: str) -> str:
  if re.match(r"^(#{1,6})\s.+$", block):
    return "heading"

  if block.startswith("```") and block.endswith("```"):
    return "code"

  if all(line.startswith(">") for line in block.splitlines()):
    return "quote"

  if all(re.match(r"^(\*|-) .+$", line) for line in block.splitlines()):
    return "unordered_list"

  lines = block.splitlines()
  if all(re.match(r"^\d+\. .+$", line) for line in lines):
    numbers = [int(line.split('.')[0]) for line in lines]
    if numbers == list(range(1, len(numbers) + 1)):
      return "ordered_list"

  # If none of the above conditions are met, it's a normal paragraph
  return "paragraph"


def text_to_children(text: str) -> Sequence[HTMLNode]:
  text_nodes = text_to_textnodes(text)
  html_nodes = [text_node_to_html_node(text_node) for text_node in text_nodes]
  return html_nodes


def markdown_to_html_node(markdown: str) -> HTMLNode:
  blocks = markdown_to_blocks(markdown)
  html_nodes = []
  for block in blocks:
    block_type = block_to_block_type(block)
    match block_type:
      case "heading":
        level = block.count("#")
        text = block[level + 1:]
        children = text_to_children(text)
        html_nodes.append(ParentNode(tag=f"h{level}", children=children))
      case "paragraph":
        text = " ".join(block.splitlines())
        children = text_to_children(text)
        html_nodes.append(ParentNode(tag="p", children=children))
      case "code":
        if not block.startswith("```") or not block.endswith("```"):
          raise ValueError("Invalid code block")
        text = block[4:-3]
        children = text_to_children(text)
        html_nodes.append(
          ParentNode(tag="pre", children=[ParentNode(tag="code", children=children)])
        )
      case "ordered_list":
        items = block.splitlines()
        items = [ParentNode("li", text_to_children(item[3:])) for item in items]
        html_nodes.append(ParentNode("ol", items))
      case "unordered_list":
        items = block.splitlines()
        items = [ParentNode("li", text_to_children(item[2:])) for item in items]
        html_nodes.append(ParentNode("ul", items))
      case "quote":
        lines = block.splitlines()
        new_lines = []
        for line in lines:
          if not line.startswith(">"):
            raise ValueError("Invalid quote block")
          new_lines.append(line.lstrip(">").strip())
        content = " ".join(new_lines)
        children = text_to_children(content)
        html_nodes.append(ParentNode("blockquote", children))
      case _:
        raise ValueError(f"Invalid block type {block_type}")

  return ParentNode("div", html_nodes)


def extract_title(markdown: str) -> str:
  lines = markdown.split('\n')
  for line in lines:
    line = line.strip()
    if line.startswith("# "):
      return line[2:].strip()  # Remove the '# ' and any leading/trailing whitespace

  raise ValueError("No H1 header found")
