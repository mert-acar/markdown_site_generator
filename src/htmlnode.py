from typing import Union, Sequence


class HTMLNode:
  def __init__(
    self,
    tag: Union[str, None] = None,
    value: Union[str, None] = None,
    children: Union[Sequence, None] = None,
    props: Union[dict, None] = None
  ) -> None:
    self.tag = tag
    self.value = value
    self.children = children
    self.props = props

  def __eq__(self, other: object) -> bool:
    return (
      self.tag == other.tag and self.value == other.value and self.children == other.children and
      self.props == other.props
    )

  def to_html(self):
    raise NotImplementedError("to_html method not implemented")

  def props_to_html(self) -> str:
    if self.props is not None:
      return "".join([f' {key}="{value}"' for key, value in self.props.items()])
    return ""

  def __repr__(self) -> str:
    return f"HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props})"


class LeafNode(HTMLNode):
  def __init__(
    self, value: str, tag: Union[str, None] = None, props: Union[dict, None] = None
  ) -> None:
    super().__init__(tag, value, None, props)

  def to_html(self) -> str:
    if self.value is None:
      raise ValueError("All leaf nodes must have a value.")

    if self.tag is None:
      return self.value

    return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

  def __repr__(self) -> str:
    return f"LeafNode({self.tag}, {self.value}, {self.props})"


class ParentNode(HTMLNode):
  def __init__(self, tag: str, children: Sequence[HTMLNode], props: Union[dict, None] = None) -> None:
    super().__init__(tag, None, children, props)

  def to_html(self):
    if self.tag is None:
      raise ValueError("All parent nodes must have a tag")

    if not self.children:
      raise ValueError("Parent nodes must have at least one child")

    return f"<{self.tag}{self.props_to_html()}>{''.join([child.to_html() for child in self.children])}</{self.tag}>"
